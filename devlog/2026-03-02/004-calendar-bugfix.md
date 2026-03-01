# 캘린더 기능 버그 3건 수정

- **ID**: 004
- **날짜**: 2026-03-02
- **유형**: 버그 수정

## 작업 요약
캘린더 기능에서 발견된 3개 버그를 수정: (1) page.calendar API 500 에러 — 존재하지 않는 `portal/works/struct` 모델 import 제거, (2) 카테고리 hover 시 레이아웃 시프트 — `hidden/flex` 토글을 `opacity` 전환으로 변경, (3) 참가자 UX 개선 — `user_name` 플랫 필드 추가, 모달 overflow 수정, 포커스 시 멤버 목록 표시.

## 변경 파일 목록

### API 500 에러 수정 (FN-20260302-0008)
- `src/app/page.calendar/api.py`: `struct = wiz.model("portal/works/struct")` → `Project = wiz.model("portal/works/project")` 변경, `move()` 함수에서 `Project.get()` 직접 호출

### 카테고리 hover 시프트 수정 (FN-20260302-0009)
- `src/portal/works/app/project.calendar/view.pug`: 편집/삭제 버튼 컨테이너 `hidden group-hover:flex` → `opacity-0 group-hover:opacity-100 pointer-events-none group-hover:pointer-events-auto` 변경

### 참가자 UX 개선 (FN-20260302-0010)
- `src/portal/works/model/struct/calendar.py`: `_attachExtras()`에서 `a['user_name'] = user.get('name', '')` 플랫 필드 추가
- `src/portal/works/app/project.calendar/view.pug`: 모달 컨테이너 `overflow-hidden` 제거
- `src/portal/works/app/project.calendar/view.ts`: `filteredMembers` getter — 검색어 비어있을 때 빈 배열 대신 전체 멤버(미선택 분) 최대 5명 반환
