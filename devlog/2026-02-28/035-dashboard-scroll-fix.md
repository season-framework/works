# 대시보드 화면 전체 스크롤 버그 수정

- **ID**: 035
- **날짜**: 2026-02-28
- **유형**: 버그 수정

## 작업 요약
대시보드 화면에서 스크롤이 끝까지 가지 않고 콘텐츠가 잘리는 문제 수정. `:host`의 `display: flex`가 기본 row 방향이고 `overflow: hidden`이 설정되어 내부 스크롤이 정상 작동하지 않았음. `flex-direction: column` 추가 및 `overflow: hidden` 제거, 자식 div에 `flex-1 min-h-0` 패턴 적용.

## 변경 파일 목록

### 스타일 (page.dashboard/view.scss)
- `:host`: `flex-direction: column` 추가, `overflow: hidden` 제거

### 템플릿 (page.dashboard/view.pug)
- 루트 div: `h-full overflow-y-auto` → `flex-1 min-h-0 overflow-y-auto` (표준 fill-and-scroll 패턴)
