# 멤버 검색 기존 멤버 제외 버그 수정

- **ID**: 034
- **날짜**: 2026-02-28
- **유형**: 버그 수정

## 작업 요약
멤버 추가 검색 시 기존 멤버가 여전히 표시되던 버그 수정. 원인은 `getExcludeEmails()`에서 `m.user`(user ID)를 사용했으나 API는 `email` 필드로 필터링하여 ID/email 불일치 발생. `m.meta?.email`로 변경하여 해결.

## 변경 파일 목록

### 프론트엔드 (project.member/view.ts)
- `getExcludeEmails()`: `m.user` → `m.meta?.email`로 변경. member DB의 `user` 필드는 user ID를 저장하므로, 이메일 기반 필터링을 위해 `meta.email` 참조 필요.
