# 이슈보드 칸반/게시판 보기 모드 전환 구현

- **ID**: 028
- **날짜**: 2026-02-28
- **유형**: 기능 추가

## 작업 요약
이슈보드에 보기 모드 전환 기능 추가. 기존 칸반 보기와 새로운 게시판(리스트) 보기를 토글 버튼으로 전환. 플로팅 버튼은 우하단에 멤버 조회 버튼 옆에 배치. 게시판 보기에서 제목, 라벨, 상태, 우선순위, 진행률, 기간, 담당자, 수정일을 테이블로 표시하며 상태 필터, 정렬, 페이지네이션 지원.

## 변경 파일 목록

### API (백엔드)
- `src/portal/works/app/project.issueboard/api.py`: `loadAllIssues()` 함수 추가 — 전체 이슈를 라벨 정보 포함한 리스트로 반환. 상태 필터(active/closed/canceled), 정렬, 페이지네이션 지원

### UI (프론트엔드)  
- `src/portal/works/app/project.issueboard/view.pug`: 보기 모드별 조건부 렌더링 추가. 칸반/게시판 토글 버튼(플로팅, 우하단), 게시판 뷰 테이블(상태 탭, 정렬 헤더, 이슈 행, 페이지네이션)
- `src/portal/works/app/project.issueboard/view.ts`: `viewMode`, `boardData` 상태 추가. `toggleViewMode()`, `loadBoardData()`, `boardChangePage()`, `boardChangeStatus()`, `boardChangeSort()`, 상태/우선순위 레이블/색상 헬퍼 메서드 추가
- `src/portal/works/app/project.issueboard/view.scss`: 보기 모드 토글 버튼 스타일 추가
