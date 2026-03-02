# 다크모드 상태/강조 색상 글로벌 오버라이드 확장

- **ID**: 004
- **날짜**: 2026-03-03
- **유형**: 기능 추가

## 작업 요약
color.scss의 `[data-theme="dark"]` 블록에 미커버된 상태별 색상(emerald/green/red/amber/purple) 오버라이드를 추가. `divide-neutral-100`, `bg-neutral-50/50`, hover:bg-red-* 등도 포함하여 이슈보드·이슈모음·칸반카드의 상태 배지/행 색상이 다크모드에서 적절한 톤으로 표시되도록 개선.

## 변경 파일 목록

### 스타일
- `src/portal/season/styles/content/color.scss`: 다크모드 오버라이드 약 50줄 추가
  - Green/Emerald: bg-emerald-50, bg-green-50, bg-green-50/50, text-emerald/green-600/700, ring-green-200
  - Red: bg-red-50, bg-red-100, text-red-500/600/700, ring-red-200, hover:bg-red-*
  - Amber: bg-amber-50, text-amber-600/700, ring-amber-200
  - Purple: bg-purple-50, text-purple-600/700, ring-purple-200
  - Neutral: bg-neutral-50/50, divide-neutral-100
  - 모든 항목에 `!` important prefix 변형도 함께 추가
