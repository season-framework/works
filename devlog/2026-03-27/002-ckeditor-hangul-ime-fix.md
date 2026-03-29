# CKEditor 한글 입력 자음/모음 분리 버그 수정

- **ID**: 002
- **날짜**: 2026-03-27
- **유형**: 버그 수정

## 작업 요약
이슈 상세 페이지의 CKEditor 댓글 입력 영역에서 한글 입력 시 자음/모음이 분리되는 버그를 수정했다. CKEditor의 `change:data` 이벤트가 한글 IME 조합 중에도 발생하여 멘션(@) 감지 로직이 조합을 간섭하는 것이 원인이었다. `compositionstart`/`compositionend` 이벤트를 활용하여 IME 조합 중에는 멘션 감지를 스킵하도록 처리했다.

## 변경 파일 목록

### Package App
- `src/portal/works/app/project.issueboard.issue/view.ts`
  - `isComposing` 플래그 필드 추가
  - CKEditor editable DOM 요소에 `compositionstart`/`compositionend` 이벤트 리스너 추가
  - `change:data` 핸들러에서 `isComposing` 체크 추가 (조합 중 스킵)
  - `compositionend` 시 `setTimeout`으로 지연 호출하여 조합 완료 후 멘션 감지 수행
