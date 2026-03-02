# SSO 로그인 후 세션 미생성 버그 수정

- **ID**: 011
- **날짜**: 2026-03-02
- **유형**: 버그 수정

## 작업 요약
SSO(SAML) 로그인 후 사용자 정보가 로딩되지 않는 문제를 수정했다. `config/season.py`에서 ACS 콜백 함수명이 `saml_acs`로 정의되어 있었으나, `portal/season/model/config.py`의 `DEFAULT_VALUES`에서는 `auth_saml_acs` 키로 조회하여 키 불일치로 함수가 `None`으로 반환되었다. 이로 인해 SAML 원시 속성이 그대로 세션에 저장되어 `id` 필드가 없어 인증 실패(401)가 발생했다.

## 변경 파일 목록

### config/season.py
- `saml_acs` 함수명을 `auth_saml_acs`로 변경하여 Config DEFAULT_VALUES 키 네이밍과 일치시킴
