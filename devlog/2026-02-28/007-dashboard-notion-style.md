# 대시보드 Notion 스타일 디자인 개편

- **ID**: 007
- **날짜**: 2026-02-28
- **유형**: 리팩토링

## 작업 요약
대시보드 페이지(page.dashboard)를 Notion 스타일 디자인 가이드라인에 맞게 개편. gray → neutral 컬러 전환, 뱃지를 ring 스타일로 변경, 빈 상태 패턴 적용, 아이콘 교체.

## 변경 파일 목록

### 대시보드
- `src/app/page.dashboard/view.pug` — 전면 재작성
  - 배경: `bg-gray-50` 제거 → `bg-white` (레이아웃 배경)
  - 컨테이너: `max-w-6xl mx-auto px-8 py-8`
  - 카드 헤더: `bg-gray-50 border-gray-100` → `border-neutral-200`, 패딩 `px-5 py-4`
  - 호버: `hover:bg-blue-50` 등 컬러 호버 → `hover:bg-neutral-50`
  - 아이콘: `ti-brand-asana` → `ti-folder`, `ti-brand-wechat` → `ti-message-circle`, `ti-pencil` → `ti-edit`
  - 이슈 카운트: `lime-600`/`emerald-600` → `blue-600`/`green-600`
  - 뱃지: `class` 속성에 `rounded-full px-2 py-0.5 ring-1 ring-inset` 추가
  - 빈 상태: 아이콘 + 텍스트 패턴으로 개선
  - 로딩: `animate-pulse` Tailwind 클래스 사용
- `src/app/page.dashboard/view.ts` — 뱃지 스타일 업데이트
  - displayStatus: 기존 `bg-slate-100 text-gray-500` → `bg-neutral-100 text-neutral-500 ring-neutral-200` 등 ring 스타일
  - displayRole: 동일 패턴으로 ring 스타일 적용
  - displayPlanStatus: 동일 패턴으로 ring 스타일 적용
