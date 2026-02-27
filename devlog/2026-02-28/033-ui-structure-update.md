# UI 구조 일부 수정 (드라이브/이슈보드 게시판 모드)

- **ID**: 033
- **날짜**: 2026-02-28
- **유형**: 기능 추가

## 작업 요약
드라이브 상단 액션 버튼에 gap-2 마진 추가. 이슈보드 게시판 모드를 전면 개편하여 라벨 서브헤더, 시작일/종료일 컬럼 분리, 담당자 축약 표시, 요청자 컬럼 추가, 수정일 제거, 칸반 라벨 순서 기반 고정 정렬 적용.

## 변경 파일 목록

### 드라이브 (project.drive/view.pug)
- 헤더 flex 컨테이너에 `gap-2` 추가하여 액션 버튼 간 간격 확보

### 이슈보드 API (project.issueboard/api.py)
- `loadAllIssues()`: 라벨 칸반 순서(mode, order) 기반 정렬 도입
- 정렬 순서: 라벨 순서 ASC → 마감일(planend) ASC (nulls last) → 시작일(planstart) DESC (nulls last)
- `functools.cmp_to_key` 사용한 커스텀 비교 정렬
- Python 측 페이지네이션으로 전환 (전체 조회 → 정렬 → 슬라이싱)
- 프론트엔드 sort/order 파라미터 제거 (고정 정렬)

### 이슈보드 프론트엔드 (project.issueboard/view.ts)
- `boardData`에서 `sort`, `order` 프로퍼티 제거
- `loadBoardData()`: API 호출 시 sort/order 제거, 응답 데이터에 라벨 서브헤더 행 삽입 (`_type: 'header'`)
- `boardChangeSort()` 메서드 삭제

### 이슈보드 템플릿 (project.issueboard/view.pug)
- 컬럼 제거: 라벨, 기간, 수정일
- 컬럼 추가: 시작일, 종료일, 요청자
- 라벨 서브헤더: 회색 배경(`bg-neutral-100`)으로 그룹 구분 표시
- 담당자: 첫 번째 담당자만 표시 + "외 n명" 축약
- 요청자: `project.member.map[row.user_id].name` 참조
- 제목/우선순위 컬럼에서 클릭 정렬 핸들러 제거
