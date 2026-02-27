# 공통 컴포넌트(pagination) Notion 스타일 디자인 개편

- **ID**: 022
- **날짜**: 2026-02-28
- **유형**: 리팩토링

## 작업 요약
pagination 공통 컴포넌트를 Notion 스타일로 개편. spinner와 dot은 이미 호환 상태여서 변경 불필요.

## 변경 파일 목록

### Source - App
- `src/app/component.pagination/view.pug`: Notion 스타일로 개편
  - `bg-gray-200` → `bg-neutral-100`
  - `text-gray-500` → `text-neutral-500`
  - `hover:bg-gray-300` → `hover:bg-neutral-200`
  - `rounded-full` → `rounded-md`
  - active: `bg-blue-500 text-white` → `bg-neutral-800 text-white`
  - Font Awesome → Tabler Icons (ti-chevrons-left/right, ti-chevron-left/right)
  - `focus:ring` 제거 → `transition-colors` 추가

### 변경 불필요
- `src/app/component.spinner/view.pug`: 이미 Tabler SVG 사용, animate-spin 유지
- `src/app/component.dot/view.pug`: 동적 color 사용, 스타일 변경 불필요
