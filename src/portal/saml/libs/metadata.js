/**
 * IdP(Identity Provider)의 EntityDescriptor를 파싱하여 주요 정보를 추출합니다.
 * @param {Element} idp - EntityDescriptor XML DOM Element.
 * @param {Object} namespaces - XML 네임스페이스 맵.
 * @returns {Object} - 파싱된 IdP 정보 객체.
 */
export const parseIdpEntityDescriptor = (idp, namespaces) => {
    // XML 네임스페이스 정의
    const md = namespaces["urn:oasis:names:tc:SAML:2.0:metadata"];
    const ds = namespaces["http://www.w3.org/2000/09/xmldsig#"];

    // 파싱 결과를 저장할 객체 초기화
    const obj = {
        entityID: idp.getAttribute("entityID"),
        cert: [],       // 인증서 정보
        sso: [],        // SingleSignOnService 엔드포인트
        sls: [],        // SingleLogoutService 엔드포인트
        nameIDFormats: [], // 지원하는 NameID 포맷
        org: {},        // 기관 정보
        contact: {},    // 연락처 정보
    };

    // 1. 인증서 정보 (KeyDescriptor) 파싱
    const certs = idp.getElementsByTagName(`${md}:KeyDescriptor`);
    Array.from(certs).forEach(cert => {
        const use = cert.getAttribute("use"); // "signing" 또는 "encryption"
        const x509CertElement = cert.getElementsByTagName(`${ds}:X509Certificate`)[0];
        if (x509CertElement) {
            obj.cert.push({ use, text: x509CertElement.textContent.trim() });
        }
    });

    // 2. SingleSignOnService 정보 파싱 (IdP의 핵심)
    const ssoServices = idp.getElementsByTagName(`${md}:SingleSignOnService`);
    Array.from(ssoServices).forEach(it => {
        const binding = it.getAttribute("Binding");
        const location = it.getAttribute("Location");
        obj.sso.push({ binding, location });
    });

    // 3. SingleLogoutService 정보 파싱
    const slsServices = idp.getElementsByTagName(`${md}:SingleLogoutService`);
    Array.from(slsServices).forEach(it => {
        const binding = it.getAttribute("Binding");
        const location = it.getAttribute("Location");
        obj.sls.push({ binding, location });
    });
    
    // 4. NameIDFormat 정보 파싱
    const nameIDFormats = idp.getElementsByTagName(`${md}:NameIDFormat`);
    Array.from(nameIDFormats).forEach(it => {
        if (it.textContent) {
            obj.nameIDFormats.push(it.textContent.trim());
        }
    });

    // 5. 기관 정보 (Organization) 파싱
    const org = idp.getElementsByTagName(`${md}:Organization`)[0];
    if (org) {
        Array.from(org.children).forEach(it => {
            const tagName = it.tagName.split(":")[1];
            obj.org[tagName] = it.textContent;
        });
    }

    // 6. 연락처 정보 (ContactPerson) 파싱
    const contact = idp.getElementsByTagName(`${md}:ContactPerson`)[0];
    if (contact) {
        Array.from(contact.children).forEach(it => {
            const tagName = it.tagName.split(":")[1];
            obj.contact[tagName] = it.textContent;
        });
    }

    return obj;
};

/**
 * IdP 메타데이터 XML 문자열을 파싱합니다.
 * @param {string} metadata - IdP 메타데이터 XML 원문.
 * @returns {Object} - 파싱된 IdP 정보 객체.
 * @throws {Error} - 메타데이터 형식이 유효하지 않을 경우 예외 발생.
 */
export const parseIdpMetadata = (metadata) => {
    const parser = new DOMParser();
    const doc = parser.parseFromString(metadata, "application/xml");
    const root = doc.firstElementChild;

    // 루트 엘리먼트가 EntityDescriptor 인지 확인
    if (!root || !root.tagName.endsWith("EntityDescriptor")) {
        // 에러 파싱 확인
        const parseError = doc.getElementsByTagName("parsererror");
        if (parseError.length > 0) {
            throw new Error(`XML Parsing Error: ${parseError[0].textContent}`);
        }
        throw new Error("Invalid Metadata: Missing EntityDescriptor root element.");
    }

    // 1. 네임스페이스 추출
    const namespaces = {};
    Array.from(root.attributes).forEach(attr => {
        if (attr.name.startsWith("xmlns:")) {
            const ns = attr.name.slice("xmlns:".length);
            namespaces[attr.value] = ns;
        }
    });
    
    // urn:oasis:names:tc:SAML:2.0:metadata 네임스페이스가 없는 경우 기본값 'md' 할당
    if (!namespaces["urn:oasis:names:tc:SAML:2.0:metadata"]) {
        namespaces["urn:oasis:names:tc:SAML:2.0:metadata"] = 'md';
    }
    // http://www.w3.org/2000/09/xmldsig# 네임스페이스가 없는 경우 기본값 'ds' 할당
    if (!namespaces["http://www.w3.org/2000/09/xmldsig#"]) {
        namespaces["http://www.w3.org/2000/09/xmldsig#"] = 'ds';
    }

    // 2. EntityDescriptor 파싱
    return parseIdpEntityDescriptor(root, namespaces);
};


/**
 * 파싱된 IdP 메타데이터 객체의 유효성을 검증합니다.
 * @param {Object} idpData - parseIdpMetadata 함수로 파싱된 객체.
 * @returns {{isValid: boolean, errors: string[]}} - 유효성 검증 결과와 에러 메시지 배열.
 */
export const validateIdpMetadata = (metadata) => {
    const idpData = parseIdpMetadata(metadata);
    const errors = [];

    // 1. entityID 존재 여부 확인
    if (!idpData.entityID || typeof idpData.entityID !== 'string') {
        errors.push("EntityID is missing or invalid.");
    }

    // 2. 최소 1개 이상의 SingleSignOnService(SSO) 엔드포인트 존재 여부 확인
    if (!idpData.sso || idpData.sso.length === 0) {
        errors.push("At least one SingleSignOnService (SSO) endpoint is required.");
    } else {
        // 각 SSO 엔드포인트의 Location 유효성(URL 형식) 확인
        idpData.sso.forEach((endpoint, index) => {
            try {
                new URL(endpoint.location);
            } catch (e) {
                errors.push(`SSO endpoint #${index} has an invalid Location URL: ${endpoint.location}`);
            }
        });
    }

    // 3. 최소 1개 이상의 서명용(signing) 인증서 존재 여부 확인
    const signingCert = idpData.cert.find(c => c.use === 'signing');
    if (!signingCert || !signingCert.text) {
        errors.push("At least one certificate for 'signing' is required.");
    }

    return errors;
};
