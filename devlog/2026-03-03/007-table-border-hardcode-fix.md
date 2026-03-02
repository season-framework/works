# 테이블 border 하드코딩 수정 및 전수 점검

- **ID**: 007
- **날짜**: 2026-03-03
- **유형**: 버그 수정

## 작업 요약
`border-black` 하드코딩을 `border-neutral-200`으로 변경하고 9개 테이블 파일을 전수 점검. `divide-neutral-100`은 FN-0004에서 글로벌 오버라이드 완료로 추가 수정 불필요. 잔여 하드코딩 border 색상(#dee2e6, border-black)은 CKEditor·SCSS 외에는 없음 확인.

## 변경 파일 목록

### Pug 수정
- `src/portal/saml/app/sp.config/view.pug`: `border-black` → `border-neutral-200`, `divide-y` → `divide-y divide-neutral-200`
- `src/portal/saml/app/mgmt.idp/view.pug`: `hover:border-black` → `hover:border-neutral-900`

### 전수 점검 결과 (수정 불필요)
- project.member, project.drive, project.info, book.access, admin.wiki, admin.project, admin.user: 모두 `divide-neutral-100` 사용 → FN-0004 글로벌 오버라이드로 커버됨
