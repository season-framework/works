# 프로젝트 전체 관리 UI 컴포넌트 구현 (admin.project)

- **ID**: 008
- **날짜**: 2026-03-01
- **유형**: 기능 추가

## 작업 요약
portal/works/app/admin.project 패키지 앱 생성. 전체 프로젝트 목록 테이블(이름/namespace/상태/공개범위/멤버 수/최근 수정) + 검색/필터 + 상태 변경 드롭다운 + 스토리지 조회 + 관리자 전용 삭제. page.admin의 project 섹션에 연결.

## 변경 파일 목록

### dev/main 프로젝트 (동일)
- `portal/works/app/admin.project/app.json`: 패키지 앱 설정 (신규)
- `portal/works/app/admin.project/view.ts`: 프로젝트 목록/검색/상태변경/삭제/스토리지 로직 (신규)
- `portal/works/app/admin.project/view.pug`: 프로젝트 테이블 UI + 필터 + 페이지네이션 (신규)
- `src/app/page.admin/view.pug`: project 섹션 placeholder → wiz-portal-works-admin-project 연결
