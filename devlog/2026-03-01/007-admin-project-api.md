# 프로젝트 전체 관리 API 구현 (page.admin/api.py)

- **ID**: 007
- **날짜**: 2026-03-01
- **유형**: 기능 추가

## 작업 요약
page.admin/api.py에 프로젝트 관리 API 4개 함수 추가. project_list(전체 프로젝트 조회, 멤버 수 포함), project_update_status(draft/open/close 강제 변경), project_delete(관리자 전용 삭제, draft 제한 없음), project_storage(프로젝트별 디스크 사용량 조회).

## 변경 파일 목록

### dev/main 프로젝트 (동일)
- `src/app/page.admin/api.py`: 프로젝트 관리 API 4개 함수 추가 (project_list, project_update_status, project_delete, project_storage)
