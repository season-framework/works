# 프로젝트 정보 컴포넌트 Notion 스타일 디자인 개편

- **ID**: 014
- **날짜**: 2026-02-28
- **유형**: 리팩토링

## 작업 요약
포털 works 패키지의 프로젝트 정보(project.info) 컴포넌트를 Notion 스타일로 전면 개편. 카드/입력/라디오/토글/테이블 등 모든 UI 요소 통일.

## 변경 파일 목록

### portal/works/app/project.info
- **view.pug**: 전면 재작성
  - 카드: `rounded-xl border-gray-300` → `rounded-lg border-neutral-200`
  - 입력: underline 스타일 → `border border-neutral-200 rounded-md` + focus ring
  - 라벨: `text-xs font-medium text-neutral-500 uppercase tracking-wider`
  - 라디오(상태/공개범위): FA 아이콘 → Tabler, `ring-1 ring-neutral-200` pill 스타일
  - 토글: `bg-gray-200` → `bg-neutral-200`, `bg-blue-700` → `bg-blue-600`
  - 테이블: `bg-slate-50` → `bg-neutral-50`, `divide-x divide-neutral-200`
  - 버튼: `rounded-full` → `rounded-md`, FA `fa-floppy-disk` → Tabler `ti-device-floppy`
  - 삭제 버튼: `bg-red-500` → `bg-red-50 text-red-600 ring-1 ring-red-200`
  - 추가 버튼: `bg-gray-500` → `bg-neutral-100 text-neutral-500`
