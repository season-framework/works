# 대시보드 활동 통계 차트 UI 구현

- **ID**: 003
- **날짜**: 2026-03-12
- **유형**: 기능 추가

## 작업 요약
대시보드 상단의 대기/진행/완료 3개 숫자 카드를 CSS/Tailwind 기반 3종 시각화(이슈 상태 비례 세그먼트 바, 프로젝트별 수평 바 차트, 14일 세로 미니 바 차트)로 교체하였다.

## 변경 파일 목록
### App (page.dashboard)
- `src/app/page.dashboard/view.ts` — `issuesByProject`, `activityTrend`, `maxProjectIssueCount`, `maxTrendCount` 상태 변수 추가, `load()`에서 데이터 할당, `trendDayLabel()` 메서드 추가
- `src/app/page.dashboard/view.pug` — grid-cols-3 숫자 카드 제거, grid-cols-1 md:grid-cols-3 활동 통계 카드 3종(세그먼트 바, 수평 바, 세로 미니 바) 추가, 빈 상태 처리 포함
