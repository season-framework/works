# 프로젝트 위키(project.wiki) Notion 스타일 디자인 개편

- **ID**: 019
- **날짜**: 2026-02-28
- **유형**: 리팩토링

## 작업 요약
프로젝트 위키 컴포넌트(`portal/works/app/project.wiki/view.pug`)를 Notion 스타일로 개편.
위키 카드 목록, 모달(위키 연결/새 위키 생성), 스켈레톤 로딩, 빈 상태 등 모든 영역의 색상을 neutral 계열로 통일하고 아이콘을 Tabler Icons로 교체.

## 변경 파일 목록

### Portal - Works 패키지
- `src/portal/works/app/project.wiki/view.pug`: 전면 개편
  - `gray-*` / `slate-*` → `neutral-*` 전환
  - 스켈레톤: `bg-gray-300` → `bg-neutral-200 animate-pulse`
  - 빈 상태: 이미지 → `ti-book-off` 아이콘
  - 카드: `hover:text-blue-500 hover:border-blue-500` → `hover:bg-neutral-50 hover:border-neutral-300`
  - `ff-b` → `font-medium`
  - 모달: `bg-gray-500 bg-opacity-75` → `bg-black/50`, `rounded-lg` → `rounded-xl`, `bg-slate-50` → `bg-neutral-50`
  - Font Awesome → Tabler Icons (ti-x, ti-plus, ti-arrow-right)
  - 입력 필드: focus ring 스타일 추가
  - 선택된 위키: `border-blue-600 bg-blue-50` → `border-blue-500 bg-blue-50 ring-1 ring-blue-200`
