# 멤버 검색 제외 범위를 프로젝트 실제 멤버로 한정

- **ID**: 036
- **날짜**: 2026-02-28
- **유형**: 버그 수정

## 작업 요약
멤버 추가 시 검색 결과가 아예 나오지 않는 버그 수정. `members()` 메서드가 실제 프로젝트 멤버 외에 시스템 전체 사용자를 가상 guest로 포함하여 반환하므로, `getExcludeEmails()`가 전체 사용자 이메일을 exclude로 전달하여 검색 결과가 0건이 됨. `m.id != null` 조건으로 실제 프로젝트 멤버(memberdb에 등록된 항목)만 필터링하도록 수정.

## 변경 파일 목록

### 프론트엔드 (project.member/view.ts)
- `getExcludeEmails()`: `.filter((m: any) => m.id != null)` 조건 추가하여 memberdb에 등록된 실제 프로젝트 멤버만 exclude 대상으로 한정
