# 사이드메뉴 사용자 영역 UI 개선

- **ID**: 009
- **날짜**: 2026-03-06
- **유형**: 기능 추가

## 작업 요약
사이드바 상단 사용자 영역을 재설계. 프로필 아바타 아이콘 추가, 알림/관리자 버튼과 마이페이지/로그아웃 버튼을 시각적으로 분리하여 세련된 UI로 개선.

## 변경 파일 목록

### Source App
- `src/app/component.nav.aside/view.pug` — 사용자 영역 전체 재구성: 아바타 아이콘(ti-user-circle) 추가, 알림·관리자 pill 그룹과 마이페이지·로그아웃 pill 그룹을 분리된 둥근 카드 형태로 배치
- `src/app/component.nav.aside/view.scss` — `.nav-action-active` 클래스 추가 (활성 상태 blue-50 배경 + blue-600 텍스트), 다크모드 오버라이드 추가
