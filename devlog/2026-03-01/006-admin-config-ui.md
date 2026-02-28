# 시스템 설정 UI 컴포넌트 구현 (admin.config)

- **ID**: 006
- **날짜**: 2026-03-01
- **유형**: 기능 추가

## 작업 요약
portal/season/app/admin.config 패키지 앱 생성. 사이트 설정(PWA)/SMTP 설정/이메일 템플릿/인증 설정(SAML 토글)/스토리지 설정 5개 탭 UI. page.admin의 config 섹션에 wiz-portal-season-admin-config 컴포넌트 연결.

## 변경 파일 목록

### dev/main 프로젝트 (동일)
- `portal/season/app/admin.config/app.json`: 패키지 앱 설정 (신규)
- `portal/season/app/admin.config/view.ts`: 5개 탭 전환 및 설정 CRUD 로직 (신규)
- `portal/season/app/admin.config/view.pug`: 사이트/SMTP/템플릿/인증/스토리지 탭별 UI (신규)
- `src/app/page.admin/view.pug`: config 섹션 placeholder → wiz-portal-season-admin-config 연결
