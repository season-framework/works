# 메인 캘린더 사이드바 개편 및 필터 기능 추가

- **ID**: 005
- **날짜**: 2026-03-02
- **유형**: 기능 추가

## 작업 요약
메인 캘린더(`page.calendar`) 사이드바와 헤더를 전면 개편. 카테고리 하위 트리 제거 → 프로젝트 일괄 체크박스로 단순화. 진행중 프로젝트만 기본 표시 + 종료 프로젝트 토글, 전체 체크/해제, 내 일정만 보기 기능 추가.

## 변경 파일 목록

### 백엔드
- `src/portal/works/model/struct/my_calendar.py`: `myProjects()`에서 프로젝트 `status` 필드 포함 반환
- `src/app/page.calendar/api.py`: `my_projects()`에서 `user_id`를 data에 포함하여 반환 (`dict(projects=result, user_id=user_id)`)

### 프론트엔드 — view.ts
- `categoryFilters`, `expandedProjects` 상태 제거
- `showClosedProjects`, `myOnly`, `currentUserId` 상태 추가
- `toggleProjectExpand()`, `toggleCategory()` 제거
- `displayProjects` getter: 종료 프로젝트 필터링
- `allProjectsChecked` getter, `toggleAllProjects()`: 전체 선택/해제
- `toggleShowClosed()`: 종료 프로젝트 토글
- `toggleMyOnly()`: 내 일정만 토글
- `filteredEvents`: 카테고리 필터 제거, `myOnly` 필터 추가 (작성자 또는 참가자)

### 프론트엔드 — view.pug
- 헤더: 오른쪽에 "내 일정만" 토글 버튼 추가
- 사이드바: 폴더 아이콘/화살표/카테고리 하위 트리 제거 → 프로젝트 체크박스+이름 단순 리스트
- 사이드바 헤더: 전체 선택/해제 체크박스 추가
- 사이드바 하단: "종료된 프로젝트 포함" 체크박스 추가
