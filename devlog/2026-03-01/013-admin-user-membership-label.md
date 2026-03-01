# 관리자 사용자 관리 등급 표기 추가

- **ID**: 013
- **날짜**: 2026-03-01
- **유형**: 기능 추가

## 작업 요약
관리자 사용자 관리 페이지에서 사용자 등급(membership)을 2단계(admin/일반)에서 4단계(관리자/내부사용자/외부사용자/손님)로 확장. 목록 테이블, 필터 드롭다운, 편집 화면 모두에 등급 표기를 추가.

## 변경 파일 목록

### view.ts
- `src/portal/season/app/admin.user/view.ts`: `membershipLabel()` 함수 추가 (admin→관리자, staff→내부사용자, user→외부사용자, guest→손님)

### view.pug
- `src/portal/season/app/admin.user/view.pug`:
  - 필터 드롭다운: admin/일반 → admin/staff/user/guest 4개 옵션
  - 목록 테이블 등급 열: 2색(admin vs 기타) → 3색(admin:빨강, staff:파랑, user/guest:회색) + membershipLabel() 사용
  - 편집 화면 등급 select: admin/일반 → admin/staff/user/guest 4개 옵션
