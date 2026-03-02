# 마이페이지 API — 로그인 이력 / 활성 기기 / 강제 로그아웃

- **ID**: 017
- **날짜**: 2026-03-02
- **유형**: 기능 추가

## 작업 요약
마이페이지 api.py에 `login_history()`, `active_sessions()`, `force_logout()` 3개 API 함수를 추가하고 클린 빌드를 수행했다.

## 변경 파일 목록

### src/app/page.mypage/api.py (수정)
- `login_history()` — 로그인 이력 페이징 조회 (fields: id, ip, device_name, login_method, status, created)
- `active_sessions()` — 활성 세션 목록 (is_current 동적 판별, datetime 직렬화)
- `force_logout()` — 세션 강제 종료 (본인 소유 검증, 현재 세션 보호)
