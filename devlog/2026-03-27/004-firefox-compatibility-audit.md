# Firefox 브라우저 호환성 감사 및 스크롤바 CSS 수정

- **ID**: 004
- **날짜**: 2026-03-27
- **유형**: 버그 수정

## 작업 요약
Firefox 브라우저 호환성을 전수 감사하여, 스크롤바 CSS 미지원 문제를 발견·수정하였다. 나머지 항목(벤더 접두사, IME/키보드 이벤트, 드래그 앤 드롭, Flexbox, CSS gap)은 이미 호환성이 확보되어 있어 추가 수정이 불필요하였다.

## 감사 항목 및 결과

| 항목 | 결과 | 상세 |
|------|------|------|
| 스크롤바 CSS | **수정** | `::-webkit-scrollbar` 전용 → 표준 `scrollbar-width`/`scrollbar-color` 추가 |
| CSS 벤더 접두사 | 이상 없음 | 모든 `-webkit-` 속성에 표준 프로퍼티 병기됨 |
| IME/키보드 이벤트 | 이상 없음 | Angular `(keyup.enter)`/`(keydown.enter)` 크로스 브라우저 호환 |
| 드래그 앤 드롭 | 이상 없음 | 모든 `dragover` 핸들러에 `preventDefault()` 적용됨 |
| Flexbox 렌더링 | 이상 없음 | Tailwind `truncate` 클래스가 `overflow: hidden` 포함하여 min-width 문제 해소 |
| CSS gap | 이상 없음 | Tailwind 생성 클래스, Firefox 63+(2018) 이후 지원 |

## 변경 파일 목록

### 스크롤바 표준 CSS 추가
- `src/angular/styles/styles.scss` — 전역 `scrollbar-width: thin; scrollbar-color` 추가
- `src/portal/season/styles/core.scss` — CSS 변수 기반 표준 스크롤바 속성 추가
- `src/portal/season/styles/content/color.scss` — 다크모드 `scrollbar-color` 추가
- `src/portal/works/app/project.member/view.scss` — autocomplete-dropdown 스크롤바 추가
- `src/app/page.authenticate/view.scss` — 인증 페이지 스크롤바 추가
