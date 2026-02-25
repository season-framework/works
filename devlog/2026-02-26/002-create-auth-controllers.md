# user.py / admin.py 인증 컨트롤러 생성 및 페이지 할당

- **ID**: 002
- **날짜**: 2026-02-26
- **유형**: 기능 추가

## 작업 요약
인증이 필요한 페이지를 위한 `user.py` 컨트롤러와 관리자 전용 `admin.py` 컨트롤러를 생성하였다. base → user → admin 상속 체인을 구성하고, 로그인이 필요한 7개 페이지에 `user` 컨트롤러를 할당하였다.

## 변경 파일 목록
### 생성
- `src/controller/user.py` — 세션 id 미존재 시 /authenticate로 리다이렉트
- `src/controller/admin.py` — user 상속 후 membership admin/superadmin 검증

### 수정 (controller: "base" → "user")
- `src/app/page.explore.project/app.json`
- `src/app/page.explore.wiki/app.json`
- `src/app/page.issues/app.json`
- `src/app/page.mypage/app.json`
- `src/app/page.project.item/app.json`
- `src/app/page.wiki.item/app.json`
- `src/app/page.wikidownload/app.json`
