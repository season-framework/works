# 대시보드 활동 통계 백엔드 집계 추가

- **ID**: 002
- **날짜**: 2026-03-12
- **유형**: 기능 추가

## 작업 요약
dashboard.py에 `issues_by_project()`(프로젝트별 배정 이슈 상위 5개)과 `activity_trend()`(최근 14일 일별 활동 건수) 메서드를 추가하고, `load()` 응답에 포함시켰다.

## 변경 파일 목록
### Portal Model
- `src/portal/works/model/struct/dashboard.py` — `issues_by_project()`, `activity_trend()` 추가, `load()` 응답 확장
