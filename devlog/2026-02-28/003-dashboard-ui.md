# 대시보드 UI 구현 (view.ts / view.pug)

- **ID**: 003
- **날짜**: 2026-02-28
- **유형**: 기능 추가

## 작업 요약
대시보드 페이지의 view.ts에 Service 초기화 + API 호출 + 각 섹션 데이터 바인딩 로직을 구현하고, view.pug에 Tailwind CSS 기반 카드형 대시보드 레이아웃을 구성했다. 이슈 요약 카운트(대기/진행/완료), 내 프로젝트 목록, 배정된 이슈, 내가 생성한 이슈, 최근 회의록, 내 계획 섹션을 반응형 2열/1열 그리드로 배치했다.

## 변경 파일 목록

### 수정
- `src/app/page.dashboard/view.ts`: Service/Project 주입, load() API 호출, 날짜/상태/역할 표시 헬퍼 함수 구현
- `src/app/page.dashboard/view.pug`: 대시보드 전체 UI (이슈 카운트, 프로젝트, 이슈, 회의록, 계획 섹션)

### 신규
- `src/app/page.dashboard/view.scss`: 호스트 컴포넌트 스타일
