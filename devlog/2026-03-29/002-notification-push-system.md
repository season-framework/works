# 통합 알림 시스템 및 PWA Push 알림 구현

- **ID**: 002
- **날짜**: 2026-03-29
- **유형**: 기능 추가

## 작업 요약
통합 알림(Notification) 시스템과 PWA Web Push 알림 인프라를 구현했다. 캘린더 일정 CRUD 시 참가자에게 자동 알림이 생성되며, 알림함 페이지를 통합 UI로 개편하고, 사이드바 벨 아이콘에 미읽음 뱃지를 추가했다. Web Push를 통해 브라우저가 닫혀도 알림을 수신할 수 있다.

## 변경 파일 목록

### 신규 생성 — DB Model
- `src/portal/works/model/db/notification.py` — 통합 알림 테이블 (works_notification)
- `src/portal/works/model/db/push_subscription.py` — Push 구독 테이블 (works_push_subscription)

### 신규 생성 — Struct
- `src/portal/works/model/struct/notification.py` — 알림 CRUD (create, create_bulk, list, unread_count, mark_read, mark_all_read, delete_old)
- `src/portal/works/model/struct/push.py` — Push 발송/구독 관리 (subscribe, unsubscribe, send, send_bulk)

### 신규 생성 — Config
- `config/push.py` — VAPID 키 쌍 및 claims email

### 신규 생성 — Service Worker
- `config/pwa/sw.js` — Push 이벤트 핸들러, notificationclick 핸들러, install/activate 라이프사이클

### 수정 — Calendar Struct
- `src/portal/works/model/struct/calendar.py` — create/update/delete에 알림 생성 로직 추가 (_notifyCalendar, _getProjectTitle, _collectAttendeeUserIds 헬퍼)

### 수정 — 알림함 페이지
- `src/app/page.notification/api.py` — Notification Struct 기반으로 전면 재작성 (list, unread_count, mark_read, mark_all_read)
- `src/app/page.notification/view.ts` — 3탭(전체/이슈/캘린더), markRead, markAllRead 구현
- `src/app/page.notification/view.pug` — 통합 알림 UI (타입별 아이콘/뱃지/색상)

### 수정 — 사이드바
- `src/app/component.nav.aside/api.py` — unread_count, push_subscribe, push_unsubscribe 엔드포인트 추가
- `src/app/component.nav.aside/view.ts` — OnDestroy, 30초 polling, unreadCount 변수
- `src/app/component.nav.aside/view.pug` — 벨 아이콘에 빨간 미읽음 뱃지

### 수정 — PWA/빌드
- `src/angular/index.pug` — SW 등록 후 자동 Push 구독 로직 (VAPID 키 인라인)
- `src/portal/season/route/pwa.manifest/controller.py` — manifest에 id, scope 필드 추가

### 삭제
- `src/portal/season/route/push/` — 신규 라우트는 서버 재시작 없이 등록 불가하여 삭제, component.nav.aside API로 대체
