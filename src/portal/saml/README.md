# SAML SP 연동용 모듈

## Packages

```
# ubuntu package
apt install -y libssl-dev
apt install -y pkg-config libxml2-dev libxmlsec1-dev libxmlsec1-openssl
apt install -y xmlsec1

# python package
pip install pysaml2
```

## SAML 설정

- 설정 방법은 두 가지(config/db) 지원
    - `server/config`의 `season.py`에 `saml_mode = "db"` 와 같이 추가할 것.
    - 기본값은 "config"으로, DB를 참고하지 않고 `season.py`에서 가져오는 것임.

### 공통

- 인증서는 아래 스크립트를 참고하여 생성할 것.
```shell
openssl req -x509 -newkey rsa:4096 -keyout sp.private.key -out sp.public.crt -sha256 -days 3650 -nodes -subj "/C=SJ/ST=SJ/L=SJ/O=Season/OU=DEV/CN=Season"
```
- 아래 saml_acs 함수를 season.py에 추가할 것.
    - 서비스에 맞게 커스텀하여 사용

```python
def saml_acs(wiz, userinfo):
    orm = wiz.model("portal/season/orm")
    db = orm.use("user")
    email = userinfo.get("mail", userinfo.get("email"))
    if email is None:
        wiz.response.status(400, error="mail or email attribute is required.")
    
    fields = "id,email,membership,name,mobile,status,created,last_access"
    info = db.get(email=email, fields=fields)

    if info is None: # new user
        try:
            membership = "staff" if email.split("@")[1] == "season.co.kr" else "guest"
        except: membership = "guest"
        name = userinfo.get("displayName", None)
        if name is None:
            name = userinfo.get("sn", "") + userinfo.get("givenName", "")
        db.insert(dict(
            email=email, 
            membership=membership,
            name=name, 
            mobile=userinfo.get("mobile", ""),
            status="active",
            created=datetime.datetime.now(),
            last_access=datetime.datetime.now()
        ))
    else: # exists user
        db.update(dict(last_access=datetime.datetime.now()), email=email)
    
    user = db.get(email=email, fields=fields)
    # email = user['email']
    user_id = user['id']

    worksdb = orm.use("member", module="works")
    worksdb.update(dict(user=user_id), user=email)
    wikidb = orm.use("access", module="wiki")
    wikidb.update(dict(key=user_id), key=email, type="user")

    return user
```

### mode: config

- `season.py`에 아래 예시와 같이 추가

```python
saml = dict(
    entityID="https://works.nanoha.kr/sp/python",
    name="Works DEV",
    description="Works DEV",
    AuthnRequestSigned=False,
    WantAssertionsSigned=True,
    NameIDFormat=["urn:oasis:names:tc:SAML:2.0:nameid-format:transient"],
    required_attributes=[
        "urn:oid:0.9.2342.19200300.100.1.3", # mail
        "urn:oid:2.5.4.4", # Surname, 성
        "urn:oid:2.5.4.42", # Forename, 이름
        "urn:oid:2.16.840.1.113730.3.1.241", # Display Name, 이름
    ],
    optional_attributes=[],
    public_key="sp.public.crt",
    private_key="sp.private.key",
    contact={
        "name": "권태욱",
        "email": "kwon3286@season.co.kr",
        "type": "administrator"
    },
    org={
        "name": "season_swdev_center",
        "display_name": "SEASON SW개발센터",
        "url": "https://git.nanoha.kr"
    },
)
```

### mode: db

- app > "SP 설정 관리" 컴포넌트 참고
- Public Key/Private Key의 경우, 파일 경로를 작성해야 함.
    - 이 때, 상대경로로 작성 시 기본 경로는 `server/config`에서 `saml` 디렉토리임. (없으면 생성 필요)

## IdP 연동 관리

- app > "IdP 연동 관리" 컴포넌트 참고

## saml config

- `config/season.py`에 추가
- 값들은 알아서 바꿔서 사용할 것

```python
saml = dict(
    entityID="https://works.nanoha.kr/sp/python",
    name="Works DEV",
    description="Works DEV",
    required_attributes=[
        "urn:oid:0.9.2342.19200300.100.1.3", # mail
        "urn:oid:2.5.4.4", # Surname, 성
        "urn:oid:2.5.4.42", # Forename, 이름
        "urn:oid:2.16.840.1.113730.3.1.241", # Display Name, 이름
    ],
    optional_attributes=[],
    public_key="sp.public.crt", # /부터 시작하지 않을 시 [wiz project root]/saml의 상대경로
    private_key="sp.private.key", # /부터 시작하지 않을 시 [wiz project root]/saml의 상대경로
    contact={
        "name": "권태욱",
        "email": "kwon3286@season.co.kr",
        "type": "administrator"
    },
    org={
        "name": "season_swdev_center",
        "display_name": "SEASON SW개발센터",
        "url": "https://git.nanoha.kr"
    },
)

def saml_acs(wiz, userinfo):
    orm = wiz.model("portal/season/orm")
    db = orm.use("user")
    email = userinfo.get("mail", userinfo.get("email"))
    if email is None:
        wiz.response.status(400, error="mail or email attribute is required.")
    
    fields = "id,email,membership,name,mobile,status,created,last_access"
    info = db.get(email=email, fields=fields)

    if info is None: # new user
        try:
            membership = "staff" if email.split("@")[1] == "season.co.kr" else "guest"
        except: membership = "guest"
        name = userinfo.get("displayName", None)
        if name is None:
            name = userinfo.get("sn", "") + userinfo.get("givenName", "")
        db.insert(dict(
            email=email, 
            membership=membership,
            name=name, 
            mobile=userinfo.get("mobile", ""),
            status="active",
            created=datetime.datetime.now(),
            last_access=datetime.datetime.now()
        ))
    else: # exists user
        db.update(dict(last_access=datetime.datetime.now()), email=email)
    
    user = db.get(email=email, fields=fields)
    # email = user['email']
    user_id = user['id']

    worksdb = orm.use("member", module="works")
    worksdb.update(dict(user=user_id), user=email)
    wikidb = orm.use("access", module="wiki")
    wikidb.update(dict(key=user_id), key=email, type="user")

    return user

```

## Create IdP Table in DB

```sql
create table saml_idp
(
    id varchar(32) not null primary key,
    `key` varchar(64) not null,
    `use` tinyint(1) default 1 not null,
    xml_content longtext default '' not null,
    created        timestamp  default current_timestamp() null,
    updated        timestamp  default current_timestamp() not null,
    constraint `key` unique (`key`)
)
    collate = utf8mb4_unicode_ci;

create or replace table saml_sp_config
(
    id           varchar(32)                            not null,
    `key`        varchar(64)                            not null,
    `use`        tinyint(1) default 1                   not null,
    `value`  longtext   default ''                  not null,
    primary key (id)
)
    collate = utf8mb4_unicode_ci;
```
