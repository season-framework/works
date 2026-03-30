# UI 개선 일괄 작업 (FN-0001~0007)

- **ID**: 001
- **날짜**: 2026-03-30
- **유형**: 기능 추가 + UI 개선

## 작업 요약
대시보드, 프로젝트 목록, 이슈보드 등 여러 영역에 걸친 7건의 UI 개선 작업을 일괄 수행. 프로젝트 즐겨찾기, 첨부파일 일괄 다운로드, 모달 크기 조정, 로딩 반투명화, 대시보드 이슈 모달, 내 계획 섹션 삭제를 포함.

## 변경 파일 목록

### FN-0001: 프로젝트 목록 즐겨찾기
- `src/app/page.explore.project/api.py` — `toggle_untrack()` 함수 추가
- `src/app/page.explore.project/view.ts` — `toggleUntrack()` 메서드 추가
- `src/app/page.explore.project/view.pug` — 별(★/☆) 아이콘 버튼 추가

### FN-0002/0003: 첨부파일 일괄 다운로드
- `src/portal/works/app/project.issueboard.issue/api.py` — `download_files_zip()` 함수 (zipfile 생성)
- `src/portal/works/app/project.issueboard.issue/view.ts` — `downloadFilesZip()` 메서드, messageEvent 바인딩
- `src/portal/works/app/project.issueboard.issue/view.pug` — 설명 첨부파일 헤더에 일괄 다운로드 버튼
- `src/portal/works/widget/message.body/view.pug` — 메시지별 일괄 다운로드 버튼 추가

### FN-0004: 이슈 모달 크기 조정
- `src/portal/works/app/project.issueboard.issue/view.scss` — `:host` 스타일 + `.modal-resize` CSS (resize: both)
- `src/portal/works/app/project.issueboard.issue/view.pug` — body div에 `modal-resize` 클래스 추가
- `src/portal/works/app/project.issueboard.issue/view.ts` — `containerClass()`에 마진(p-6, lg:p-10), backdrop(bg-black/[.5]) 추가

### FN-0005: 로딩 배경 반투명
- `src/app/layout.aside/view.pug` — `.bg-white` → `.bg-white/80.backdrop-blur-sm`

### FN-0006: 대시보드 이슈 클릭 → 모달
- `src/app/page.dashboard/view.ts` — `openIssue()`에 `item.id` fallback 추가
- `src/app/page.dashboard/view.pug` — 배정된/생성한 이슈 `routerLink` → `(click)="openIssue(item)"`

### FN-0007: 내 계획 섹션 삭제
- `src/app/page.dashboard/view.pug` — 내 계획 섹션 전체 삭제
- `src/app/page.dashboard/view.ts` — `plans` 변수, `displayPlanStatus()` 메서드 삭제
