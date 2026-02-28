# 사용자 관리 API 구현

- **ID**: 002
- **날짜**: 2026-03-01
- **유형**: 기능 추가

## 작업 요약
page.admin/api.py에 사용자 관리 CRUD API 6개 함수 구현. 기존 user 테이블과 ORM 패턴 활용하여 목록 조회(페이징/검색/필터), 상세 조회(참여 프로젝트 포함), 수정, 비밀번호 초기화, 논리 삭제, 사용자 전환 기능 제공.

## 변경 파일 목록

### dev 프로젝트
- `src/app/page.admin/api.py`: user_list, user_get, user_update, user_reset_password, user_delete, user_switch 6개 API 함수 구현

### main 프로젝트
- `src/app/page.admin/api.py`: dev와 동일 내용 적용
