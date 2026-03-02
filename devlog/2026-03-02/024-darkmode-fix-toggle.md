# 다크모드 동작 안함 수정 및 토글 UI 개선

- **ID**: 024
- **날짜**: 2026-03-02
- **유형**: 버그 수정 + 기능 개선

## 작업 요약
다크모드 전환 시 로고만 변경되고 나머지 테마가 적용되지 않던 문제를 수정했다. 근본 원인은 `styles.scss`에 `@import "portal/season/core"` 누락으로 `color.scss`의 `[data-theme="dark"]` 셀렉터가 최종 번들 CSS에 포함되지 않았던 것이다. 임포트 추가 후 82건의 다크모드 스타일이 번들에 포함되었다. 추가로 테마 전환 UI를 단순 버튼에서 세그먼트 컨트롤(칸반/게시판 스타일 토글 스위치)로 변경했다.

## 변경 파일 목록

### 수정된 프로젝트 설정
- `src/angular/styles/styles.scss` — `@import "portal/season/core"` 추가 (works, wiki 앞에 배치). 이것이 핵심 수정으로, color.scss의 다크모드 CSS 변수 오버라이드를 번들에 포함시킴

### 수정된 소스 파일
- `component.nav.aside/view.pug` — 테마 전환 버튼을 세그먼트 컨트롤(`.theme-toggle-track` + `.theme-toggle-thumb` + `.theme-toggle-option`) 토글 스위치로 변경
- `component.nav.aside/view.scss` — `.theme-toggle-*` 스타일 추가 (슬라이딩 thumb 애니메이션, 다크모드 오버라이드 포함)
