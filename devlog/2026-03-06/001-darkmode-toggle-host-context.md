# 다크모드 토글 :host-context 셀렉터 수정

- **ID**: 001
- **날짜**: 2026-03-06
- **유형**: 버그 수정

## 작업 요약
다크모드에서 토글 버튼이 여전히 밝은 색상으로 표시되던 문제 수정. Angular ViewEncapsulation으로 인해 컴포넌트 SCSS에서 `[data-theme="dark"]` 셀렉터가 외부 `<html>` 요소의 속성을 참조하지 못하는 것이 원인. `:host-context([data-theme="dark"])` 셀렉터로 변경하여 상위 DOM 요소 속성을 정상 참조하도록 수정.

## 변경 파일 목록

### Source App
- `src/app/component.nav.aside/view.scss`: `[data-theme="dark"]` → `:host-context([data-theme="dark"])` 변경
