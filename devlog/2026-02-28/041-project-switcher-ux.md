# 프로젝트 스위칭 드롭다운 UX 개선

- **ID**: 041
- **날짜**: 2026-02-28
- **유형**: 기능 추가

## 작업 요약
프로젝트 스위칭 드롭다운에 키보드 화살표(↑↓) 네비게이션과 Enter 선택 기능 추가. 축약명을 메인 텍스트로 표시하고 아래에 회색 프로젝트명 표시. 드롭다운 가로 폭(320px)과 세로 높이(max-h-80) 확대.

## 변경 파일 목록

### 사이드바 컴포넌트 (dev, main 동일 적용)
- `src/app/component.nav.aside/view.ts`: `highlightIndex` 상태 추가. `onSwitcherKeydown()` 메서드로 ArrowUp/Down/Enter/Escape 처리. `onSwitcherInput()`으로 검색 시 하이라이트 리셋. `scrollToHighlighted()`로 스크롤 추적. `filteredProjects()`에 short 필드 검색 추가.
- `src/app/component.nav.aside/view.pug`: 드롭다운 패널 너비 `w-[320px]`, 목록 높이 `max-h-80`, 검색 입력 높이 `h-8`로 확대. 항목에 `mouseenter` 하이라이트, `bg-blue-50` 활성 표시. 축약명(`p.short`) 메인 표시 + 프로젝트명(`p.title`) 하위 회색 텍스트 표시.
