# 멘션 기능 + 읽음/안읽음 추적 + 알림함 통합 구현

- **ID**: 001
- **날짜**: 2026-03-05
- **유형**: 기능 추가

## 작업 요약
이슈보드 메시지에 @멘션 기능을 추가하고, 이슈 단위 읽음/안읽음 추적 시스템을 구현했다. 이슈보드 카드에 안읽음 인디케이터(파란 동그라미)를 표시하고, 대시보드에 안읽은 이슈 목록 카드와 알림함 모달을 추가했다.

## 변경 파일 목록

### DB 모델 (새로 생성)
- `src/portal/works/model/db/issueboard/issue/read.py` — 사용자별 이슈 읽음 상태 추적 테이블 (user_id, issue_id, last_read_message_id, is_read)
- `src/portal/works/model/db/issueboard/mention.py` — 멘션 기록 테이블 (message_id, issue_id, user_id, mentioned_user_id, is_read)

### Struct (새로 생성)
- `src/portal/works/model/struct/issueboard/mention.py` — 멘션 파싱(@사용자명), 멘션 레코드 생성/수정/읽음 처리
- `src/portal/works/model/struct/issueboard/read.py` — 읽음 상태 관리 (markRead, markUnreadForOthers, getUnreadMap, getUnreadIssues)

### Struct (수정)
- `src/portal/works/model/struct/issueboard.py` — Mention, Read Sub-Struct 등록
- `src/portal/works/model/struct/issueboard/message.py` — create/update에 멘션 처리 + 안읽음 상태 갱신 연동
- `src/portal/works/model/struct/dashboard.py` — unread_issues() 메서드 추가

### Frontend - 이슈 상세 (멘션 UI + 읽음 처리)
- `src/portal/works/app/project.issueboard.issue/api.py` — markRead(), members() API 추가
- `src/portal/works/app/project.issueboard.issue/view.ts` — @ 멘션 드롭다운 로직, CKEditor 키보드 인터셉트, markRead 호출
- `src/portal/works/app/project.issueboard.issue/view.pug` — 멘션 드롭다운 UI (멤버 목록, 아바타, 이름, 이메일)

### Frontend - 이슈보드 (안읽음 인디케이터)
- `src/portal/works/app/project.issueboard/api.py` — unreadMap() API 추가
- `src/portal/works/app/project.issueboard/view.ts` — unreadMap 상태 관리, loadUnreadMap() 메서드
- `src/portal/works/app/project.issueboard/view.pug` — 칸반/게시판 모드 unread 전달 + 게시판 파란 동그라미

### Frontend - 이슈 카드 위젯
- `src/portal/works/widget/widget.project.issueboard.issue/view.ts` — @Input() unread 추가
- `src/portal/works/widget/widget.project.issueboard.issue/view.pug` — 파란 동그라미 인디케이터

### Frontend - 대시보드
- `src/app/page.dashboard/api.py` — unread_issues() API 추가
- `src/app/page.dashboard/view.ts` — 안읽은 이슈 상태, 알림함 모달 로직, 페이지네이션
- `src/app/page.dashboard/view.pug` — 안읽은 이슈 카드 섹션 + 알림함 모달 UI

### 라이브러리
- `src/portal/works/libs/struct/display.ts` — markdown() 메서드에 @멘션 하이라이트 처리 추가
