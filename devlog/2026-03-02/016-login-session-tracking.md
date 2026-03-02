# 로그인 이력 기록 및 세션 추적 백엔드 로직 구현

- **ID**: 016
- **날짜**: 2026-03-02
- **유형**: 기능 추가

## 작업 요약
User-Agent 파싱 유틸, 세션 토큰 발급/추적, 로그인 이력 기록(SAML+비밀번호), 로그아웃 시 세션 비활성화, 강제 로그아웃 세션 차단 로직을 구현했다.

## 변경 파일 목록

### config/season.py (수정)
- `parse_user_agent()` — User-Agent → "Chrome 120 on Windows 10" 형태 변환
- `record_login_history()` — login_history 테이블에 기록
- `create_or_update_session_token()` — 세션 토큰 발급/갱신 + user_session 테이블 관리
- `deactivate_session()` — 현재 세션의 user_session 비활성화 (로그아웃 시 호출)
- `session_create()` — 세션 토큰 발급 로직 추가
- `auth_saml_acs()` — SAML 로그인 이력 기록 추가

### src/app/page.authenticate/api.py (수정)
- `login()` — 비밀번호 로그인 성공/실패 시 login_history 기록 추가

### src/portal/season/route/auth/controller.py (수정)
- 로그아웃 시 `deactivate_session()` 호출 추가

### src/controller/base.py (수정)
- 세션 토큰 유효성 검증 추가 (강제 로그아웃된 세션 차단)

### pip 패키지
- `user-agents` 패키지 설치
