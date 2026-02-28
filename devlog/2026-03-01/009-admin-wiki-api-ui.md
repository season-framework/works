# 위키 전체 관리 API 및 UI 구현 (admin.wiki)

- **ID**: 009
- **날짜**: 2026-03-01
- **유형**: 기능 추가

## 작업 요약
page.admin/api.py에 위키 관리 API 3개 함수(wiki_list, wiki_access, wiki_delete) 추가. portal/wiki/app/admin.wiki 패키지 앱 생성하여 위키 목록(제목/namespace/공개범위/접근 권한 수/페이지 수) + 검색/필터 + 접근 권한 상세 조회 + 관리자 전용 삭제 기능 구현. page.admin의 wiki 섹션에 연결.

## 변경 파일 목록

### dev/main 프로젝트 (동일)
- `src/app/page.admin/api.py`: 위키 관리 API 3개 함수 추가 (wiki_list, wiki_access, wiki_delete)
- `portal/wiki/app/admin.wiki/app.json`: 패키지 앱 설정 (신규)
- `portal/wiki/app/admin.wiki/view.ts`: 위키 목록/검색/접근 권한 조회/삭제 로직 (신규)
- `portal/wiki/app/admin.wiki/view.pug`: 위키 테이블 UI + 접근 권한 상세 뷰 (신규)
- `src/app/page.admin/view.pug`: wiki 섹션 placeholder → wiz-portal-wiki-admin-wiki 연결
