# 드라이브 tree API driveItem 미정의 오류 수정

- **ID**: 026
- **날짜**: 2026-02-28
- **유형**: 버그 수정

## 작업 요약
`/api/works/project/{id}/drive/tree` API 호출 시 `NameError: name 'driveItem' is not defined` 오류 발생. `driveItem` 함수가 파일 하단(268행)에 정의되어 있었으나, `exec()` 실행 특성상 `drive/tree` 액션(108행)에서 호출 시점에 아직 정의되지 않음. 함수를 `safe_path` 바로 뒤, `if action ==` 분기 전으로 이동하여 해결.

## 변경 파일 목록

### 수정 파일
- `src/portal/works/route/project/controller.py` — `driveItem()` 함수를 파일 하단에서 `safe_path()` 직후(30행)로 이동. 하단의 중복 정의 제거.
