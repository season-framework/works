# 대시보드 크로스 프로젝트 캘린더 위젯 추가

- **ID**: 012
- **날짜**: 2026-03-02
- **유형**: 기능 추가

## 작업 요약
대시보드(`page.dashboard`)에 전체 프로젝트에서 사용자와 관련된 일정을 표시하는 월간 캘린더 위젯을 추가했다. 기존 `MyCalendar.searchMyEvents()` 백엔드를 활용하여 작성자이거나 참가자인 일정을 크로스 프로젝트로 월별 조회한다.

## 변경 파일 목록

### src/app/page.dashboard/api.py
- `MyCalendar` 모델 import 추가
- `my_calendar()` API 함수 추가 — year/month 파라미터로 월별 일정 조회

### src/app/page.dashboard/view.ts
- 캘린더 상태 변수 추가 (`calYear`, `calMonth`, `calEvents`, `calWeeks`, `calSelectedDate` 등)
- `loadCalendar()` — API 호출 및 그리드 생성
- `buildCalendarGrid()` — 월간 달력 그리드 구성 (이전 달 빈칸, 오늘 하이라이트, 이벤트 매칭)
- `calPrev()`, `calNext()`, `calToday()` — 월 이동 및 오늘 복귀
- `selectDate()` — 날짜 클릭 시 해당 일 일정 상세 표시
- `calEventColor()`, `calFormatDateRange()` — 이벤트 색상 및 날짜 포맷 유틸리티

### src/app/page.dashboard/view.pug
- 이슈 요약 카운트 아래에 "내 일정" 전체 너비 섹션 추가
- 월 이동 네비게이션 (이전/다음/오늘)
- 7열 캘린더 그리드 (요일 헤더 + 날짜 셀)
- 날짜 셀에 이벤트 도트 (최대 3개 + 더보기 카운트)
- 날짜 클릭 시 하단에 일정 상세 리스트 (프로젝트명, 카테고리, 시간 범위 표시)
- 일정 클릭 시 해당 프로젝트 캘린더 페이지로 이동
