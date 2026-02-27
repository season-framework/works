# 위키 상세 및 위키 컴포넌트 Notion 스타일 디자인 개편

- **ID**: 021
- **날짜**: 2026-02-28
- **유형**: 리팩토링

## 작업 요약
위키 관련 portal 컴포넌트 4개(`book.tree`, `book.content`, `book.info`, `book.access`)를 Notion 스타일로 전면 개편.
트리 네비게이션, 콘텐츠 에디터, 위키 정보 폼, 접근 제어 테이블 등 모든 영역의 색상을 neutral 계열로 통일하고 Tabler Icons로 교체.

## 변경 파일 목록

### Portal - Wiki 패키지
- `src/portal/wiki/app/book.tree/view.pug`: 전면 개편
  - `bg-blue-500` 헤더 → `bg-neutral-800` 다크 헤더
  - `bg-slate-50` → `bg-neutral-50`
  - Font Awesome → Tabler Icons (ti-download, ti-settings, ti-plus, ti-folder-plus, ti-chevron-down/right, ti-home, ti-file-text, ti-x, ti-check)
  - 트리 아이템: `hover:bg-blue-50` → `hover:bg-neutral-100 rounded-md`
  - 활성: `text-blue-500 bg-blue-50` → `bg-neutral-100 text-neutral-900 font-medium`

- `src/portal/wiki/app/book.content/view.pug`: 전면 개편
  - `border-gray-300` → `border-neutral-200`
  - `ff-eb` → `font-semibold`
  - `bg-slate-50` → `bg-neutral-50`
  - 탭 버튼: `rounded-2xl` → `rounded-lg`, `ff-b` → `font-medium`
  - 리비전/삭제 섹션: 깔끔한 카드 스타일
  - Font Awesome → Tabler Icons (ti-device-floppy, ti-circle-check, ti-trash)

- `src/portal/wiki/app/book.info/view.pug`: 전면 개편
  - `border-gray-300` → `border-neutral-200`
  - 입력 필드: underline → `rounded-md border` + focus ring 스타일
  - 공개범위 라디오: `has-[:checked]` → `peer-checked` ring pill 스타일
  - Font Awesome → Tabler Icons (ti-lock, ti-users, ti-lock-open)

- `src/portal/wiki/app/book.access/view.pug`: 전면 개편
  - `border-gray-300` → `border-neutral-200`
  - `bg-slate-50` → `bg-neutral-50`
  - `ff-b` → `font-medium`
  - "It's Me!" 뱃지: `bg-orange-500` → amber ring 뱃지
  - 삭제 버튼: `rounded-full bg-red-500` → `rounded-md bg-red-50 text-red-500`
  - Font Awesome → Tabler Icons (ti-x)
