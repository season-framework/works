# 이슈보드 게시판 보기 공지/일정 탭 및 검색 기능 추가

- **ID**: 037
- **날짜**: 2026-02-28
- **유형**: 기능 추가

## 작업 요약
이슈보드 게시판 보기에 '공지/알림', '일정' 상태 필터 탭을 추가하고, 우측 상단에 제목 검색 패널을 구현. 기존 '진행중' 필터에서 noti/event 상태를 분리하여 별도 탭으로 제공. 검색은 Enter 키 또는 X 버튼으로 초기화 가능.

## 변경 파일 목록

### 프론트엔드 템플릿 (project.issueboard/view.pug)
- 상태 필터 탭에 '공지/알림'(noti), '일정'(event) 버튼 추가
- 총 건수 오른쪽에 검색 입력 패널 추가 (아이콘, 입력, 클리어 버튼)

### 프론트엔드 로직 (project.issueboard/view.ts)
- `boardData`에 `keyword`, `searchFocused` 속성 추가
- `loadBoardData()`에 keyword 파라미터 전달
- `boardSearch()`, `boardClearSearch()` 메서드 추가

### 백엔드 API (project.issueboard/api.py)
- `loadAllIssues()`: `active` 필터에서 noti/event 제거, `noti`/`event` 개별 status_filter 추가
- `keyword` 파라미터로 제목 필터링 기능 추가 (대소문자 무시)
