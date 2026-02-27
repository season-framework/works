# 이슈보드 컴포넌트 Notion 스타일 디자인 개편

- **ID**: 016
- **날짜**: 2026-02-28
- **유형**: 리팩토링

## 작업 요약
portal/works/app/project.issueboard 칸반 보드를 Notion 스타일로 전면 개편.

## 변경 파일 목록

### portal/works/app/project.issueboard
- **view.pug**: 전면 재작성
  - 컬럼 border: `border-gray-300` → `border-neutral-200`
  - 헤더: `bg-neutral-50/50`, `text-sm font-semibold text-neutral-800`
  - 액션 버튼: `bg-gray-500` → neutral 아이콘 호버 (`hover:bg-neutral-200`)
  - FA → Tabler: `fa-up-right-and-down-left-from-center` → `ti-arrows-maximize`, `fa-xmark` → `ti-x`, `fa-plus` → `ti-plus`, `fa-up-down-left-right` → `ti-grip-vertical`
  - 빈 상태: SVG → `ti-layout-kanban` 아이콘
  - 카드: `rounded-2xl` → `rounded-lg`
  - 멤버 조회: `bg-slate-900` → `bg-neutral-900`, input `bg-neutral-800`
  - 스크롤 화살표: neutral 색상 + rounded
