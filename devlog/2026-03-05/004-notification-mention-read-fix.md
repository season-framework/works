# 대시보드 알림함 + 멘션 범위 + 읽음 갱신 수정

- **ID**: 004
- **날짜**: 2026-03-05
- **유형**: 버그 수정

## 작업 요약
3가지 이슈 수정: (1) 대시보드 알림함이 렌더링되지 않던 문제 — 클린 빌드로 `unread_issues` API 함수 등록, (2) 멘션 드롭다운에 전체 사용자가 표시되던 문제 — `members()` API에서 memberdb 레코드가 있는 실제 프로젝트 멤버만 반환하도록 필터링, (3) 이슈 상세에서 돌아올 때 안읽음 인디케이터가 갱신되지 않던 문제 — `openIssue()`에서 `issue.event.hide` 콜백으로 `loadUnreadMap()` 호출 추가.

## 변경 파일 목록

### 멘션 범위 수정
- `src/portal/works/app/project.issueboard.issue/api.py`
  - `members()` 함수: `m.get('id')` 체크 추가로 memberdb 레코드가 있는 실제 프로젝트 멤버만 반환 (동적 추가된 비멤버 제외)

### 읽음 상태 즉시 갱신
- `src/portal/works/app/project.issueboard/view.ts`
  - `openIssue()`: `issue.event.hide` 콜백 추가 — 이슈 모달 닫힐 때 `loadUnreadMap()` + `service.render()` 호출

### 알림함
- 클린 빌드 수행 (`clean: true`) — 신규 `unread_issues` API 함수 등록
