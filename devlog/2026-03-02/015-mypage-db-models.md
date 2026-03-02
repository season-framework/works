# 마이페이지 로그인 이력 / 활성 기기 DB 모델 생성

- **ID**: 015
- **날짜**: 2026-03-02
- **유형**: 기능 추가

## 작업 요약
마이페이지 로그인 이력·활성 기기 관리 기능을 위한 DB 모델 2종(`login_history`, `user_session`)을 생성하고 MySQL 테이블을 직접 생성했다.

## 변경 파일 목록

### DB Model (신규)
- `src/model/db/login_history.py` — 로그인 이력 테이블 스키마 (user_id, email, ip, user_agent, device_name, login_method, status, created)
- `src/model/db/user_session.py` — 세션 추적 테이블 스키마 (user_id, ip, user_agent, device_name, is_active, created, last_active)

### MySQL DDL
- `login_history` 테이블 생성 (인덱스: user_id, created)
- `user_session` 테이블 생성 (인덱스: user_id, is_active)
