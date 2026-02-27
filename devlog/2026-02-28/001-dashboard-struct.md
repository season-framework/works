# 대시보드 Struct 메서드 구현 (works 패키지)

- **ID**: 001
- **날짜**: 2026-02-28
- **유형**: 기능 추가

## 작업 요약
works 패키지 model/struct에 대시보드 전용 통합 조회 Struct(`dashboard.py`)를 추가했다. 현재 로그인 사용자 기준으로 내 프로젝트, 배정된 이슈 요약(상태별 카운트 + 최근 목록), 생성한 미완료 이슈, 최근 회의록, 진행중 계획을 집계하는 static method를 구현했다. 닫힌/untrack 프로젝트는 모든 조회에서 제외된다.

## 변경 파일 목록

### 신규
- `src/portal/works/model/struct/dashboard.py`: 대시보드 통합 조회 Struct (my_projects, my_issues_summary, my_created_issues, recent_meetings, my_plans, load)
