# 프로젝트 드라이브(project.drive) Notion 스타일 디자인 개편

- **ID**: 020
- **날짜**: 2026-02-28
- **유형**: 리팩토링

## 작업 요약
프로젝트 드라이브 컴포넌트(`portal/works/app/project.drive/view.pug`)를 Notion 스타일로 전면 개편.
파일 트리, 파일 테이블, 이슈파일/회의록파일/사진 탭 등 모든 영역의 색상을 neutral로 통일하고 Tabler Icons 교체.

## 변경 파일 목록

### Portal - Works 패키지
- `src/portal/works/app/project.drive/view.pug`: 전면 개편 (215줄)
  - `gray-*` / `slate-*` → `neutral-*` 전환
  - Font Awesome → Tabler Icons (ti-cloud, ti-trash, ti-upload, ti-folder-plus, ti-download, ti-x, ti-check, ti-cursor-text, ti-folder, ti-cloud-off)
  - 헤더: `bg-slate-50` → `bg-neutral-50`, `ff-eb` → `font-semibold`, 아이콘 추가
  - 트리 사이드바: `bg-gray-100` → `bg-neutral-50`, hover → `hover:bg-neutral-100 rounded-md`
  - 탭: 텍스트 색 기반 활성 상태 (`text-blue-600 font-medium bg-white`)
  - 테이블: `bg-slate-50` → `bg-neutral-50`, hover `bg-slate-200` → `hover:bg-neutral-50`
  - `ff-b` → `font-medium`
  - 빈 상태: 이미지 → `ti-cloud-off` 아이콘
  - 업로드 상태바: shadow-lg + 둥근 프로그레스바
  - 사진 탭: group-hover overlay, 다운로드 버튼 개선
  - 선택 체크: `bg-blue-lt` → `bg-blue-50`, checkbox ring 스타일
