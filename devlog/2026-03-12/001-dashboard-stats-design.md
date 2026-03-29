# 대시보드 활동 통계 지표 설계 및 구성 확정

- **ID**: 001
- **날짜**: 2026-03-12
- **유형**: 기능 추가

## 작업 요약
대시보드 상단 대기/진행/완료 3개 요약 카드를 제거하고, CSS/Tailwind 기반 시각화 3종(이슈 상태 분포·프로젝트별 이슈 비중·최근 2주 활동 추이)으로 교체하는 설계를 확정하였다.

## 확정된 활동 통계 3종

### 1. 이슈 상태 분포 (Segmented Bar)
- **데이터**: 기존 `my_issues_summary()` → counts {open, work, finish}
- **시각화**: 비례 세그먼트 바 (전체 너비를 상태 비율로 분할) + 범례
- **클릭**: `/issues`
- **빈 상태**: "배정된 이슈가 없습니다"

### 2. 프로젝트별 이슈 분포 (Horizontal Bars)
- **데이터**: 신규 `issues_by_project()` — 프로젝트별 배정 이슈 수 상위 5개
- **시각화**: 수평 바 차트 (CSS width%)
- **클릭**: 각 바 → `/project/{namespace}/issueboard`
- **빈 상태**: "배정된 이슈가 없습니다"

### 3. 최근 2주 활동 추이 (Vertical Mini Bars)
- **데이터**: 신규 `activity_trend()` — 14일간 일별 이슈 업데이트 건수
- **시각화**: 세로 미니 바 14개 (CSS height%) + 오늘 강조
- **클릭**: 없음
- **빈 상태**: "최근 2주간 활동이 없습니다"

### 공통 사항
- **제외 기준**: 기존 `_excluded_project_ids()` (status=close + untrack) 동일 적용
- **레이아웃**: grid-cols-1 md:grid-cols-3, 모바일 스택
- **차트 라이브러리**: 미사용 (CSS/Tailwind 전용)
