# SAML SSO 설정 오류 수정

- **ID**: 010
- **날짜**: 2026-03-02
- **유형**: 버그 수정

## 작업 요약
`/saml/login` 호출 시 `struct.py`의 `config()` 메서드에서 `saml_config`이 `None`이 되어 `stdClass(None)` → `TypeError: 'NoneType' object is not iterable` 에러가 발생하는 문제를 수정했다. DB `system_config`에서 `saml_mode`가 `"config"`으로 반환되면 season.py에서 `saml` dict를 찾는데, season.py에 `saml` dict가 정의되어 있지 않아 `None`이 반환되는 것이 원인이었다.

## 변경 파일 목록

### portal/saml/model/struct.py
1. **`config()` 메서드 방어 코드 추가**:
   - `saml_mode` 기본값을 `"config"` → `"db"`로 변경 (season.py와 일치)
   - config 모드에서 설정을 찾지 못하면 자동으로 DB fallback 수행
   - `saml_config`이 `None`인 경우 명확한 에러 메시지 출력
2. **`config_from_db()` 에러 핸들링 강화**:
   - DB 조회 실패 시 명확한 에러 메시지 (`SAML SP 설정 DB 조회 실패`)
   - DB에 설정이 비어있으면 명시적 에러 메시지 출력
3. **ACS/SLS 엔드포인트 기본값 수정**:
   - `/auth/saml/acs` → `/saml/acs` (실제 SAML Route 경로와 일치)
   - `/auth/saml/acs` → `/saml/sls` (SLS 경로 수정)
