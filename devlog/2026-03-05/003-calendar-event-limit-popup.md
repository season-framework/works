# 캘린더 이벤트 3개 제한 + 더보기 팝업

- **ID**: 003
- **날짜**: 2026-03-05
- **유형**: 기능 추가

## 작업 요약
캘린더 일별 셀에서 이벤트를 최대 3개까지만 표시하고, 초과 시 "+N건 더보기" 링크를 표시. 클릭 시 해당 날짜의 전체 일정을 팝업으로 보여주는 기능 구현. 메인 캘린더, 프로젝트 캘린더, 대시보드 미니 캘린더 3곳 모두 적용.

## 변경 파일 목록

### 메인 캘린더 (page.calendar)
- `src/app/page.calendar/view.pug` — 이벤트 영역 3개 제한 (`*ngIf="ei < 3"`), "+N건 더보기" 링크, day popup overlay 추가
- `src/app/page.calendar/view.ts` — `dayPopup` 상태 추가, `openDayPopup()`/`closeDayPopup()` 메서드, `onEscKey()` 업데이트

### 프로젝트 캘린더 (project.calendar, portal/works)
- `src/portal/works/app/project.calendar/view.pug` — 동일 3개 제한 패턴, 드래그 지원 유지, day popup overlay 추가
- `src/portal/works/app/project.calendar/view.ts` — `dayPopup` 상태/메서드 추가, 카테고리/드래그 등 기존 기능 보존

### 대시보드 미니 캘린더 (page.dashboard)
- `src/app/page.dashboard/view.pug` — 이벤트 도트 3개 제한, "+N건" 텍스트 추가 (selectDate 트리거)
