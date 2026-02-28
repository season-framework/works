# 사이드 메뉴 프로젝트 스위칭 라우팅 개선

- **ID**: 040
- **날짜**: 2026-02-28
- **유형**: 버그 수정

## 작업 요약
프로젝트 스위칭 시 Angular 라우팅 이벤트가 감지되지 않아 화면이 전환되지 않는 문제와, 항상 info 페이지로 이동하던 동작을 개선. 프로젝트 변경 시 re-init 처리하고, 현재 보고 있는 메뉴를 유지하되 대상 프로젝트에 해당 메뉴가 없으면 메인 메뉴로 폴백.

## 변경 파일 목록

### 프로젝트 페이지 라우팅 (dev, main 동일 적용)
- `src/app/page.project.item/view.ts`: NavigationEnd 핸들러에 프로젝트 ID 변경 감지 로직 추가. `isMenuAvailable()`, `getDefaultMenu()` 헬퍼 메서드 추가. 프로젝트 변경 시 project.init() 재호출 및 메뉴 사용 가능 여부 체크.

### 사이드바 스위칭 로직 (dev, main 동일 적용)
- `src/app/component.nav.aside/view.ts`: `switchProject()` 메서드에서 현재 보고 있는 메뉴(WizRoute.segment.menu)를 유지하여 이동하도록 변경. 프로젝트 페이지가 아닌 경우 기본 경로로 이동.
