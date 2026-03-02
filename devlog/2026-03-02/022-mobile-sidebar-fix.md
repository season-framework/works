# 모바일 사이드 메뉴 동작 안함 수정

- **ID**: 022
- **날짜**: 2026-03-02
- **유형**: 버그 수정

## 작업 요약
모바일에서 햄버거 버튼 클릭 시 사이드 메뉴가 열리지 않는 문제를 수정했다. 두 `nav` 요소에 `max-sm:h-0`이 항상 적용되어 `[ngbCollapse]`가 expanded 상태가 되어도 높이가 0으로 유지되는 것이 원인이었다.

## 변경 파일 목록

### component.nav.aside/view.pug
- `max-sm:h-0` 제거 (두 nav 요소 모두)
- `[ngbCollapse]="service.navbar.isMenuCollapsed"` → `[ngClass]="{'mobile-nav-collapsed': service.navbar.isMenuCollapsed}"` 교체
- `transition-all duration-300` 불필요 클래스 제거

### component.nav.aside/view.scss
- `@media (max-width: 639px)` 미디어 쿼리로 `.mobile-nav-collapsed` 클래스 추가
- 모바일에서만 `display: none` 적용, 데스크탑에서는 항상 메뉴 표시
