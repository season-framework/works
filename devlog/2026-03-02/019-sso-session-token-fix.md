# SSO 로그인 시 활성 기기 미등록 수정

- **ID**: 019
- **날짜**: 2026-03-02
- **유형**: 버그 수정

## 작업 요약
SSO(SAML) 로그인 흐름에서 `create_or_update_session_token()`이 호출되지 않아 `user_session` 테이블에 레코드가 생성되지 않는 버그 수정. `auth_saml_acs()` 함수 마지막에 세션 토큰 발급 호출을 추가.

## 변경 파일 목록
### Config
- `config/season.py`: `auth_saml_acs()` 함수 끝에 `create_or_update_session_token(wiz, user_id)` 호출 추가
