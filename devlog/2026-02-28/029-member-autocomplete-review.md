# 멤버 자동완성 드롭다운 리뷰 반영

- **ID**: 029
- **날짜**: 2026-02-28
- **유형**: 버그 수정

## 작업 요약
멤버 자동완성 드롭다운 리뷰 4건 반영: 포커스 시 상위 20개 즉시 표시, 화면 좌우폭 적절한 크기로 제한(max-w-3xl) 및 우측 정렬, 멤버 추가 영역 vertical-top 정렬.

## 변경 파일 목록

### API
- `src/portal/works/app/project.member/api.py`: 빈 키워드 시 즉시 반환 대신 전체 사용자 상위 20개 조회하여 반환하도록 수정

### UI
- `src/portal/works/app/project.member/view.ts`: `onSearchFocus()`를 포커스 시 결과가 없으면 바로 API 호출하도록 변경
- `src/portal/works/app/project.member/view.pug`: 전체 컨테이너에 `max-w-3xl ml-auto` 추가 (우측 정렬+폭 제한), 멤버 추가 영역 `items-end` → `items-start` (vertical-top 정렬), 검색결과 없음 조건에서 키워드 길이 제약 제거
