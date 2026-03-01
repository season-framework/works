# Admin 포탈 컴포넌트 API 라우팅 수정 (wiz.call 404 해결)

- **ID**: 011
- **날짜**: 2026-03-01
- **유형**: 버그 수정

## 작업 요약
4개 admin 포탈 컴포넌트(admin.user, admin.config, admin.project, admin.wiki)에서 `wiz.call()` 호출 시 404가 발생하던 근본 원인을 수정. WIZ에서 `wiz.call()`은 현재 앱의 api.py로 라우팅되는데, 모든 API 함수가 `page.admin/api.py`에만 존재하고 각 포탈 컴포넌트에는 api.py가 없어서 19개 함수 모두 404 실패. 각 컴포넌트에 api.py를 생성하고, 보안을 위해 admin 컨트롤러도 추가.

## 변경 파일 목록

### 신규 생성 — API 파일
- `portal/season/app/admin.user/api.py`: user_list, user_get, user_update, user_reset_password, user_delete, user_switch (6개 함수)
- `portal/season/app/admin.config/api.py`: config_load, config_update, smtp_test, template_list, template_read, template_update (6개 함수)
- `portal/works/app/admin.project/api.py`: project_list, project_update_status, project_delete, project_storage (4개 함수)
- `portal/wiki/app/admin.wiki/api.py`: wiki_list, wiki_access, wiki_delete (3개 함수)

### 신규 생성 — Admin 컨트롤러
- `portal/season/controller/admin.py`: wiz.controller("admin") 상속
- `portal/works/controller/admin.py`: wiz.controller("admin") 상속
- `portal/wiki/controller/admin.py`: wiz.controller("admin") 상속

### 수정 — app.json (controller 설정)
- `portal/season/app/admin.user/app.json`: controller "" → "admin"
- `portal/season/app/admin.config/app.json`: controller "" → "admin"
- `portal/works/app/admin.project/app.json`: controller "" → "admin"
- `portal/wiki/app/admin.wiki/app.json`: controller "" → "admin"

### 수정 — 기존 API 정리
- `src/app/page.admin/api.py`: 19개 함수 모두 포탈 컴포넌트로 이동 완료, 파일을 참조 주석으로 대체
