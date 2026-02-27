# 이슈 상세(project.issueboard.issue) Notion 스타일 디자인 개편

- **ID**: 017
- **날짜**: 2026-02-28
- **유형**: 리팩토링

## 작업 요약
이슈 상세 모달/패널(`portal/works/app/project.issueboard.issue/view.pug`)을 Notion 스타일로 전면 개편.
labels을 `bg-slate-500 text-white ff-b` → `text-sm font-medium text-neutral-500`로, 모든 색상을 neutral 계열로, 아이콘을 Tabler Icons로 통일, 메시지 탭을 underline 방식으로, worker popup을 밝은 드롭다운으로 변경.

## 변경 파일 목록

### Portal - Works 패키지
- `src/portal/works/app/project.issueboard.issue/view.pug`: 전면 개편
  - `gray-*` / `slate-*` → `neutral-*` 색상 전환
  - `bg-slate-500 text-white ff-b` 라벨 → `text-sm font-medium text-neutral-500 w-28 shrink-0` 속성형 라벨
  - Font Awesome → Tabler Icons 전면 교체 (ti-x, ti-arrows-move, ti-check, ti-plus, ti-send 등)
  - 라디오 필 스타일: `border-neutral-200 rounded-md` + `peer-checked:border-blue-400 peer-checked:bg-blue-50 peer-checked:text-blue-600`
  - 작업자 팝업: 다크(bg-slate-900) → 밝은 드롭다운(bg-white border-neutral-200 rounded-lg shadow-lg)
  - 메시지 탭: filled 버튼 → underline 방식 (`border-b-2 border-neutral-900`)
  - 메시지 영역: `bg-indigo-50/50` → `bg-neutral-50/50`
  - 아바타: `bg-orange-400 border-orange-500` → `bg-blue-50 border-blue-200`
  - 알림 배너: `bg-gray-300` → `bg-blue-50 text-blue-600 border-blue-200`
  - TODO: group hover로 action 표시, 깔끔한 border-neutral-200 컨테이너
  - 입력 필드: `focus:ring-2 focus:ring-blue-500/20 focus:border-blue-400` 통일
