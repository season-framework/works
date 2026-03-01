# 캘린더 기능 고도화 (카테고리/참가자/드래그앤드롭/공통 캘린더)

- **ID**: 003
- **날짜**: 2026-03-02
- **유형**: 기능 추가

## 작업 요약
프로젝트 캘린더에 카테고리 관리, 참가자(attendee) 관리, 드래그앤드롭 일정 이동, ESC 키 모달 닫기, "내 일정만 보기" 필터 사이드바를 추가했다. 또한 전체 프로젝트의 일정을 통합 조회하는 공통 캘린더 페이지(/calendar)를 신규 생성했다.

## 변경 파일 목록

### DB Model (신규)
- `src/portal/works/model/db/calendar/attendee.py` — 참가자 테이블 (works_calendar_attendee)
- `src/portal/works/model/db/calendar/category.py` — 카테고리 테이블 (works_calendar_category)

### DB Model (수정)
- `src/portal/works/model/db/calendar.py` — category_id 컬럼 추가

### Struct (수정/신규)
- `src/portal/works/model/struct/calendar.py` — 전면 재작성: 카테고리 CRUD, 참가자 CRUD, move(), _attachExtras()
- `src/portal/works/model/struct/my_calendar.py` — 신규: MyCalendar 크로스 프로젝트 캘린더 struct

### Portal App — project.calendar
- `src/portal/works/app/project.calendar/api.py` — 13개 API 함수 (기존 5 + 신규 8)
- `src/portal/works/app/project.calendar/view.ts` — ESC 핸들러, 드래그앤드롭, 카테고리 사이드바, 참가자 관리
- `src/portal/works/app/project.calendar/view.pug` — Flex 레이아웃(캘린더+사이드바), 모달에 카테고리/참가자 UI

### Page — 공통 캘린더
- `src/app/page.calendar/app.json` — 신규 페이지 (viewuri: /calendar, controller: user)
- `src/app/page.calendar/view.ts` — 프로젝트/카테고리 트리 필터, 드래그앤드롭
- `src/app/page.calendar/view.pug` — 프로젝트별 카테고리 토글 사이드바
- `src/app/page.calendar/api.py` — my_calendar struct 기반 API
- `src/app/page.calendar/view.scss` — 호스트 스타일

### Navigation
- `src/app/component.nav.aside/view.pug` — 이슈모음 아래에 캘린더 메뉴 링크 추가

### MySQL
- CREATE TABLE works_calendar_attendee
- CREATE TABLE works_calendar_category
- ALTER TABLE works_calendar ADD category_id VARCHAR(32)
