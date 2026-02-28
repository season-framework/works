# 사용자 관리 UI 컴포넌트 구현

- **ID**: 003
- **날짜**: 2026-03-01
- **유형**: 기능 추가

## 작업 요약
portal/season/app/admin.user 패키지 앱을 생성하여 사용자 관리 UI 구현. 목록 화면(테이블+검색+필터+페이지네이션)과 상세/편집 화면(프로필 편집 폼+참여 프로젝트 목록+비밀번호 초기화+사용자 전환+삭제) 제공. page.admin의 user 섹션에 `wiz-portal-season-admin-user` 컴포넌트 연결.

## 변경 파일 목록

### dev 프로젝트
- `portal/season/app/admin.user/app.json`: 패키지 앱 생성 (신규)
- `portal/season/app/admin.user/view.pug`: 목록+상세 화면 UI (신규)
- `portal/season/app/admin.user/view.ts`: API 호출, 검색/필터/페이지네이션, CRUD 로직 (신규)
- `src/app/page.admin/view.pug`: user 섹션에 wiz-portal-season-admin-user 컴포넌트 배치

### main 프로젝트
- 위 4개 파일 동일 적용
