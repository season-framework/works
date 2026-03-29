# 이슈보드 안읽은 이슈 필터 토글 버튼 추가

- **ID**: 012
- **날짜**: 2026-03-06
- **유형**: 기능 추가

## 작업 요약
이슈보드 플로팅 영역 하단 검색 입력란 옆에 "안읽음" 토글 버튼을 추가하여, 안읽은 이슈만 필터링할 수 있도록 구현. 칸반 모드는 클라이언트 사이드 필터(onProcessIssue), 게시판 모드는 서버 사이드 필터(loadAllIssues API)로 처리.

## 변경 파일 목록

### TypeScript (portal/works/app/project.issueboard/view.ts)
- `showUnreadOnly: boolean = false` 상태 변수 추가
- `toggleUnreadOnly()` 메서드 추가: 토글 시 게시판 모드는 1페이지부터 재로드
- `onProcessIssue()`: 칸반 모드에서 `unreadMap` 기반 안읽은 이슈 필터 조건 추가
- `loadBoardData()`: `unread_only` 파라미터를 API 호출에 전달

### Template (portal/works/app/project.issueboard/view.pug)
- 검색 입력란 영역을 flex 래퍼로 감싸고 오른쪽에 "안읽음" 토글 버튼 추가
- 활성 시 파란색 border + 텍스트, 비활성 시 중립 스타일
- 불릿 도트 아이콘 + 데스크탑에서 "안읽음" 텍스트 표시

### API (portal/works/app/project.issueboard/api.py)
- `loadAllIssues()` 함수에 `unread_only` 파라미터 추가
- `unread_only=true` 시 `getUnreadMap()`으로 안읽은 이슈만 필터링 (페이지네이션 전 적용)
