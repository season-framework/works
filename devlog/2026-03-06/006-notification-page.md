# 알림함 독립 페이지 + 사이드메뉴 아이콘

- **ID**: 006
- **날짜**: 2026-03-06
- **유형**: 기능 추가

## 작업 요약
알림함을 대시보드 모달에서 독립 페이지(`/notification`)로 분리. 사이드바 마이페이지/로그아웃 영역에 벨 아이콘 버튼 추가. 대시보드에서 모달 코드 제거하고 "전체보기"를 routerLink로 변경. 알림함 페이지는 "관련된 전체 이슈"/"멘션된 이슈" 탭 구분, 읽음/안읽음 시각 구분, 페이지네이션 지원.

## 변경 파일 목록
### 신규 생성
- `src/app/page.notification/app.json` — 앱 설정 (viewuri: /notification, controller: user, layout: layout.aside)
- `src/app/page.notification/view.ts` — 알림함 로직 (탭 전환, 페이지네이션, 이슈 네비게이션)
- `src/app/page.notification/view.pug` — 알림함 UI (탭/목록/페이지네이션)
- `src/app/page.notification/view.scss` — :host 스타일
- `src/app/page.notification/api.py` — all_issues, mentioned_issues API (users 정보 포함)

### 수정
- `src/app/component.nav.aside/view.pug` — 마이페이지/로그아웃 사이에 벨 아이콘 버튼 추가
- `src/app/page.dashboard/view.pug` — 알림함 모달 제거, "전체보기"를 routerLink="/notification"으로 변경
- `src/app/page.dashboard/view.ts` — 알림함 모달 관련 변수/메서드 제거 (showNotificationInbox, notificationItems 등)
