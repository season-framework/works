# 마이페이지 Notion 스타일 UI 리디자인 + 로그인/기기 UI

- **ID**: 018
- **날짜**: 2026-03-02
- **유형**: 기능 추가 + 리팩토링

## 작업 요약
마이페이지를 Notion 스타일로 전면 리디자인하고, 로그인 이력 테이블 + 활성 기기 관리(강제 로그아웃) UI를 구현했다.

## 변경 파일 목록

### src/app/page.mypage/view.pug (전면 재작성)
- 프로필 히어로: 80px 아바타, hover 카메라 오버레이
- 기본 정보: Notion property 스타일 (라벨-값 인라인, bg-transparent 입력)
- 비밀번호 변경: 접힘/펼침 토글 (chevron 아이콘)
- 활성 기기: 기기 카드 리스트, 현재 기기 뱃지, 강제 로그아웃 버튼
- 로그인 이력: CSS Grid 테이블, 방식/상태 뱃지, 페이지네이션
- Tailwind CSS, 최소 테두리, hover:bg-neutral-50

### src/app/page.mypage/view.ts (수정)
- `loadLoginHistory()`, `loadActiveSessions()`, `forceLogout()` 추가
- `togglePassword()`, `historyTotalPages`, `goHistoryPage()` 추가
- `methodLabel()`, `statusLabel()` 뱃지 헬퍼
