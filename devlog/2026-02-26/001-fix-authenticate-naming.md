# App 네이밍 규칙 수정: page.page.authenticate → page.authenticate

- **ID**: 001
- **날짜**: 2026-02-26
- **유형**: 리팩토링

## 작업 요약
`page.page.authenticate` 앱의 폴더명이 네이밍 규칙(page.page.* 중복 접두사 금지)을 위반하고 있어 `page.authenticate`로 이름을 변경하였다. 새 앱을 생성하고 기존 파일을 복사한 뒤 app.json의 id/namespace/title을 수정하였다.

## 변경 파일 목록
### 삭제
- `src/app/page.page.authenticate/` — 기존 앱 폴더 삭제

### 생성
- `src/app/page.authenticate/app.json` — id: `page.authenticate`, namespace: `authenticate`
- `src/app/page.authenticate/view.ts` — 기존 코드 이관
- `src/app/page.authenticate/view.pug` — 기존 코드 이관
- `src/app/page.authenticate/view.scss` — 기존 코드 이관
- `src/app/page.authenticate/api.py` — 기존 코드 이관
