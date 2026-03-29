# 캘린더 그룹 참가자(추상 그룹) 기능 구현

- **ID**: 001
- **날짜**: 2026-03-29
- **유형**: 기능 추가

## 작업 요약
캘린더 일정에 "프로젝트 전체" 등 추상 그룹 단위로 참가자를 등록할 수 있는 기능을 구현했다. DB 스키마 설계부터 Struct 비즈니스 로직, API, 프로젝트 캘린더·개인 캘린더·대시보드 UI까지 전체 레이어를 구현했다. 추가로 참가자 검색이 프로젝트 구성원만 반환하도록 수정했다.

## 변경 파일 목록

### DB Model (신규)
- `portal/works/model/db/calendar/attendee_group.py`: calendar_attendee_group 테이블 (id, event_id, project_id, group_type, group_id, created)

### Struct (수정)
- `portal/works/model/struct/calendar.py`: 그룹 참가자 CRUD 메서드 추가 (addGroupAttendee, removeGroupAttendee, getGroupAttendees, resolveGroupMembers). _attachExtras에 group_attendees/resolved_attendees 병합. create/update에 그룹 동기화 로직 추가.
- `portal/works/model/struct/my_calendar.py`: searchMyEvents에 group_type='project_all' 기반 프로젝트 전체 일정 통합 조회 로직 추가.

### API (수정)
- `portal/works/app/project.calendar/api.py`: members() 함수를 memberdb 직접 조회로 변경 (프로젝트 구성원만 반환). add_group_attendee(), remove_group_attendee() 함수 추가.

### UI (수정)
- `portal/works/app/project.calendar/view.ts`: eventForm에 group_attendees 필드 추가. toggleProjectAll, hasProjectAll, getGroupLabel, removeGroupFromForm 메서드 추가. filteredEvents에 그룹 참가자 필터 반영.
- `portal/works/app/project.calendar/view.pug`: 편집 모드에 "프로젝트 전체" 토글 버튼·그룹 칩 추가. 읽기 모드에 그룹 참가자 뱃지·resolved_attendees 표시. 캘린더 항목에 👥 아이콘 추가.
- `src/app/page.dashboard/view.pug`: 캘린더 상세에 그룹 참가자 뱃지 추가.
- `src/app/page.calendar/view.ts`: filteredEvents에 group_attendees 기반 필터 추가. hasEventGroupAll() 메서드 추가.
- `src/app/page.calendar/view.pug`: 캘린더 항목에 👥 아이콘 추가. 이벤트 상세 모달에 그룹 참가자 섹션 추가.
