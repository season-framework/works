# 회의록(project.meeting) Notion 스타일 디자인 개편

- **ID**: 018
- **날짜**: 2026-02-28
- **유형**: 리팩토링

## 작업 요약
회의록 컴포넌트(`portal/works/app/project.meeting/view.pug`)를 Notion 스타일로 개편.
좌측 목록 패널과 우측 편집 영역의 색상을 neutral 계열로 통일, Font Awesome → Tabler Icons 교체, 깔끔한 빈 상태 UI, 미니멀 버튼/첨부파일 스타일 적용.

## 변경 파일 목록

### Portal - Works 패키지
- `src/portal/works/app/project.meeting/view.pug`: 전면 개편
  - `gray-*` / `slate-*` / `indigo-*` → `neutral-*` 색상 전환
  - Font Awesome → Tabler Icons (ti-plus, ti-search, ti-notes, ti-upload, ti-trash, ti-file-check, ti-device-floppy, ti-download, ti-x)
  - SVG 검색 아이콘 → `ti ti-search`
  - 목록: `hover:bg-slate-100` → `hover:bg-neutral-50`, 선택 `bg-indigo-50` → `bg-neutral-100`
  - `ff-b` → `font-medium`
  - 빈 상태: 이미지 → `ti-notes` 아이콘 + 텍스트
  - 버튼: 배경색 버튼 → ring/neutral 스타일 + blue 프라이머리
  - 첨부파일: `bg-gray-200` → `bg-neutral-100 rounded-md` 깔끔한 칩
  - 에디터 상단: `border-blue-500` → `border-neutral-200`
