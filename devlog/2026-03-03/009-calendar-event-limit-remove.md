# 캘린더 이벤트 3개 제한 제거 — 모든 이벤트 표시

- **ID**: 009
- **날짜**: 2026-03-03
- **유형**: 버그 수정

## 작업 요약
캘린더 일별 셀에서 이벤트가 3개를 초과하면 `+N건`으로만 표시되어 나머지 내역이 보이지 않는 문제 수정. 3개 제한 조건(`*ngIf="ei < 3"`)과 `+N건` 블록(`*ngIf="ei === 3"`)을 제거하고, overflow-y-auto 스크롤 처리로 모든 이벤트가 표시되도록 변경.

## 변경 파일 목록

### 메인 캘린더 페이지
- `src/app/page.calendar/view.pug`: `ei < 3` / `ei === 3` 조건 제거, 이벤트 컨테이너에 `overflow-y-auto` + `max-height: 80px` 추가

### 프로젝트 캘린더 (works 패키지)
- `src/portal/works/app/project.calendar/view.pug`: 동일 패턴 수정 (`ei < 3` / `ei === 3` 제거, overflow 스크롤 추가)

### 대시보드 미니 캘린더
- `src/app/page.dashboard/view.pug`: `ei < 3` / `cell.events.length > 3` 조건 제거, `overflow-hidden` → `overflow-y-auto` + `max-height: 60px`로 변경
