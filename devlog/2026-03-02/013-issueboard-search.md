# 이슈보드 검색 기능 추가

- **ID**: 013
- **날짜**: 2026-03-02
- **유형**: 기능 추가

## 작업 요약
프로젝트 세부 페이지 이슈보드에 이슈 검색 기능을 추가. 플로팅 버튼 영역 아래에 검색 입력란을 배치하여 칸반/게시판 모드 모두에서 동일하게 이슈 제목 기반 검색이 가능하도록 구현.

## 변경 파일 목록

### Portal App (works/project.issueboard)
- `view.ts`: `searchKeyword` 변수 추가, `onSearchKeyword()` / `clearSearchKeyword()` 메서드 추가, `onProcessIssue()`에 검색어 필터링 로직 추가, `toggleViewMode()`에서 검색어 동기화, `boardSearch()` / `boardClearSearch()`에서 `searchKeyword` 양방향 동기화
- `view.pug`: 플로팅 버튼 그룹 아래에 검색 input UI 추가 (다크 배경, 동일 너비, X 클리어 버튼)
