# 모바일 전체 페이지 전수조사 및 반응형 수정

- **ID**: 008
- **날짜**: 2026-03-06
- **유형**: UI 개선

## 작업 요약
전체 39개 페이지/컴포넌트 모바일 반응형 감사 수행. Critical 5건, Warning 7건 발견 및 수정. 관리자 사이드바 모바일 전환, 테이블 가로 스크롤, 프로젝트 정보 패널 너비, 이슈보드 필터 줄바꿈, 프라이버시 패딩, PWA 설정 그리드, 칸반 컬럼 너비 등 수정.

## 변경 파일 목록
### Critical 수정
- `src/app/page.admin/view.pug` — flex→max-sm:flex-col, 사이드바 max-sm:w-full, nav 가로 배치, 콘텐츠 패딩 반응형
- `src/portal/works/app/admin.project/view.pug` — 테이블 overflow-hidden→overflow-x-auto, min-w-[700px]
- `src/portal/season/app/admin.user/view.pug` — 테이블 overflow-hidden→overflow-x-auto, min-w-[600px]
- `src/portal/works/app/project.info/view.pug` — w-96→w-96 max-sm:w-full
- `src/portal/works/app/project.issueboard/view.pug` — 필터 버튼 flex-wrap, 검색 영역 ml-auto→max-sm:w-full

### Warning 수정
- `src/app/page.privacy/view.pug` — px-8→px-4 sm:px-8, h-[600px]→max-sm:h-[400px]
- `src/portal/season/app/admin.config/view.pug` — PWA 색상 grid-cols-2→grid-cols-1 sm:grid-cols-2
- `src/portal/works/app/project.issueboard/view.pug` — 칸반 컬럼 w-[320px]→max-sm:w-[85vw]
