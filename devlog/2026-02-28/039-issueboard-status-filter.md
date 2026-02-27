# 이슈보드 진행 상태별 모아보기 필터 추가

- **ID**: 039
- **날짜**: 2026-02-28
- **유형**: 기능 추가

## 작업 요약
이슈보드 하단 플로팅 버튼 영역의 맨 왼쪽에 상태별 모아보기 필터 드롭다운을 추가. 필터 항목: 전체, 공지, 일정, 예정(기존 '시작 전' 명칭 변경), 진행, 완료. 칸반 모드에서는 `onProcessIssue()` 프론트 필터로 적용, 게시판 모드에서는 API boardData.status와 연동. 외부 클릭 시 드롭다운 자동 닫기.

## 변경 파일 목록

### 프론트엔드 로직 (project.issueboard/view.ts)
- `statusFilter`, `statusFilterOpen`, `statusFilterOptions` 상태 추가
- `toggleStatusFilter()`, `setStatusFilter()`, `statusFilterLabel()` 메서드 추가
- `onProcessIssue()` 수정: statusFilter 적용
- `statusLabel()` 수정: open→'예정'으로 명칭 변경
- `toggleViewMode()` 수정: 모드 전환 시 statusFilter 반영
- `@HostListener('document:click')` 추가: 외부 클릭 시 드롭다운 닫기

### 프론트엔드 템플릿 (project.issueboard/view.pug)
- 플로팅 버튼 그룹 맨 왼쪽에 상태 필터 버튼 + 위로 열리는 드롭다운 패널 추가
- 선택된 상태 하이라이트 표시
