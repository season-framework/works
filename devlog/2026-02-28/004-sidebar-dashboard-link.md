# 사이드바 메뉴에 대시보드 링크 추가 및 빌드

- **ID**: 004
- **날짜**: 2026-02-28
- **유형**: 기능 추가

## 작업 요약
component.nav.aside의 view.pug에 대시보드 메뉴 항목을 이슈모음 위(최상단)에 추가했다. `ti-dashboard` 아이콘과 `routerLinkActive`를 통한 활성 상태 하이라이트를 적용했다. 빌드(clean: false) 완료.

## 변경 파일 목록

### 수정
- `src/app/component.nav.aside/view.pug`: 대시보드 메뉴 항목 추가 (이슈모음 위 최상단 위치)
