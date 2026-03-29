# 대시보드 여백 축소 — 정보 밀도 개선

- **ID**: 005
- **날짜**: 2026-03-06
- **유형**: UI 개선

## 작업 요약
대시보드 전체 여백(padding, margin, gap)을 축소하여 한 화면에 표시되는 정보량을 증가시킴. 컨테이너 px-8→px-5, 헤더 mb-8→mb-4, 섹션 간격 mb-4→mb-3, 카드 헤더 py-4→py-2.5, 아이템 행 py-3→py-2, 빈 상태 py-12→py-8 등 전반적 축소.

## 변경 파일 목록
### 프론트엔드 (Source)
- `src/app/page.dashboard/view.pug` — 전체 여백 체계 축소 (타이틀 text-2xl→text-lg, 아이콘 18px→16px, padding/margin/gap 전반 축소)
