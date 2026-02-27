# 멤버 검색 시 기존 멤버 제외

- **ID**: 031
- **날짜**: 2026-02-28
- **유형**: 기능 추가

## 작업 요약
멤버 자동완성 검색 시 이미 프로젝트에 추가된 멤버는 검색 결과에서 제외되도록 수정. API에 `exclude` 파라미터를 추가하고, 프론트엔드에서 기존 멤버 이메일 목록을 전달.

## 변경 파일 목록

### API (api.py)
- `search()`: `exclude` 쿼리 파라미터 추가, 쉼표 구분 이메일 목록을 파싱하여 `~Model.email.in_(exclude_list)` 조건으로 검색 결과에서 제외

### 프론트엔드 (view.ts)
- `getExcludeEmails()`: 신규 메서드 — `project.member.list()`에서 기존 멤버 이메일 목록을 쉼표 구분 문자열로 반환
- `searchUsers()`: API 호출 시 `exclude` 파라미터 전달
