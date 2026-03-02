# CKEditor 다크모드 테마 적용

- **ID**: 005
- **날짜**: 2026-03-03
- **유형**: 기능 추가

## 작업 요약
CKEditor 전체에 다크모드를 적용. ckeditor.scss에 `[data-theme="dark"]` 블록을 추가하여 toolbar, editable area, content(h2 border, hr, table, code, pre), dropdown/panel, placeholder 등 모든 CKEditor 내부 UI를 다크 테마로 오버라이드. core.scss에는 works 패키지 특화 wrapper(noborder/works) 다크모드 추가.

## 변경 파일 목록

### 스타일
- `src/portal/season/styles/content/ckeditor.scss`: `[data-theme="dark"]` 블록 추가 (~110줄)
  - .ck-toolbar: bg #161619, border #28282f
  - .ck-editor__editable: bg #111113, text #dddde3
  - .ck-content: h2 border, hr, a, blockquote, code, pre, table 다크 색상
  - .ck-dropdown__panel, .ck-list: 다크 배경
  - .ck-placeholder: 다크 placeholder 색상
- `src/portal/works/styles/core.scss`: `[data-theme="dark"]` 래퍼 블록 추가
  - .ck-editor-noborder: 투명 배경 (부모 배경 투과)
  - .ck-editor-works: 다크 editable 배경
