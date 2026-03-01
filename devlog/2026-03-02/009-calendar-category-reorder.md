# 프로젝트 캘린더 카테고리 드래그앤드롭 순서 변경 기능

- **ID**: 009
- **날짜**: 2026-03-02
- **유형**: 기능 추가

## 작업 요약
프로젝트 캘린더 사이드바에서 카테고리 순서를 드래그앤드롭으로 변경할 수 있는 기능 구현. DB의 기존 `sort_order` 필드를 활용하여 백엔드 벌크 업데이트 API와 프론트엔드 드래그앤드롭 UI를 추가.

## 변경 파일 목록

### Struct (calendar.py)
- `src/portal/works/model/struct/calendar.py`: `reorderCategories(order_list)` 메서드 추가 — 프로젝트 소속 검증 + sort_order 벌크 업데이트

### Portal App (project.calendar)
- `src/portal/works/app/project.calendar/api.py`: `reorder_categories()` 함수 추가 — order_list JSON 파싱 → struct 호출
- `src/portal/works/app/project.calendar/view.ts`: 카테고리 드래그 상태 변수(`draggedCategory`, `dragOverCategoryId`) + 핸들러(`onCategoryDragStart`, `onCategoryDragOver`, `onCategoryDrop`, `onCategoryDragEnd`) 추가
- `src/portal/works/app/project.calendar/view.pug`: 카테고리 항목에 `draggable` + 드래그 이벤트 바인딩, 드래그 핸들 아이콘(`ti-grip-vertical`), 드래그 오버 시 파란색 하이라이트
