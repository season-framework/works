# 프로젝트 드라이브 다운로드/업로드 404 버그 수정

- **ID**: 001
- **날짜**: 2026-03-27
- **유형**: 버그 수정

## 작업 요약
프로젝트 드라이브에서 파일 다운로드 시 404 에러가 발생하는 버그를 수정했다. 프론트엔드에서 `drive/download/{filepath}` 형태로 URL을 생성하는데, 백엔드 Route의 `action` 분기가 정확 일치(`==`)로 되어 있어 매칭되지 않았다. `drive/upload`도 동일한 패턴이므로 함께 수정했다.

## 변경 파일 목록

### Route
- `src/portal/works/route/project/controller.py`
  - `elif action == "drive/upload":` → `elif action.startswith("drive/upload"):`
  - `elif action == "drive/download":` → `elif action.startswith("drive/download"):`
