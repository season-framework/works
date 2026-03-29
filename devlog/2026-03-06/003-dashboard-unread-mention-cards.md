# 대시보드 안읽은 이슈/멘션 카드 표시 및 알림함 탭 기능

- **ID**: 003
- **날짜**: 2026-03-06
- **유형**: 기능 추가 + 버그 수정

## 작업 요약
대시보드 안읽은 이슈 섹션이 데이터 없을 때 완전히 숨겨지던 문제 수정 — 항상 표시되도록 변경 (빈 상태 메시지 포함). 멘션 이슈에 "멘션" 배지(amber색) 추가. 알림함 모달에 "관련된 전체 이슈"/"멘션된 이슈" 탭 분리 구현. 읽은 이슈는 회색 반투명으로 시각 구분. 백엔드에 `all_related_issues`, `mentioned_issues` 조회 메서드 추가.

## 변경 파일 목록

### Source App
- `src/app/page.dashboard/view.pug`: 안읽은 이슈 섹션 상시 표시, 멘션 배지, 알림함 모달 탭 UI 추가, 읽음/안읽음 시각 구분
- `src/app/page.dashboard/view.ts`: `notificationTab` 상태 추가, `switchNotificationTab()` 메서드, `loadNotificationPage()` 탭별 API 분기
- `src/app/page.dashboard/api.py`: `all_issues()`, `mentioned_issues()` 엔드포인트 추가

### Portal Package (works) Model
- `src/portal/works/model/struct/dashboard.py`: `is_mentioned` 플래그 추가, `all_related_issues()`, `mentioned_issues()` 정적 메서드 추가
