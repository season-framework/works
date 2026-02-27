# 사이드바 및 레이아웃 Notion 스타일 디자인 개편

- **ID**: 006
- **날짜**: 2026-02-28
- **유형**: 리팩토링

## 작업 요약
사이드바(component.nav.aside)와 레이아웃(layout.aside)을 Notion 스타일 디자인 가이드라인에 맞게 전면 개편. 컬러를 gray → neutral 계열로 전환하고, 메뉴 아이템을 rounded-md hover 패턴으로 변경. Font Awesome 아이콘을 Tabler Icons로 교체.

## 변경 파일 목록

### 사이드바 (component.nav.aside)
- `src/app/component.nav.aside/view.pug` — 전면 재작성
  - 배경: `bg-white` → `bg-neutral-50`, 보더: `border-gray-300` → `border-neutral-200`
  - 메뉴 아이템: blue hover/active → neutral rounded-md 스타일 (`hover:bg-neutral-200/60`, 활성 `bg-neutral-200/60 font-medium text-neutral-900`)
  - 좌측 border-l 활성 표시 제거 → 배경색 + font-weight로 변경
  - 아이콘 교체: `ti-dashboard` → `ti-layout-dashboard`, `ti-brand-asana` → `ti-folder`, `ti-brand-wechat` → `ti-message-circle`
  - Font Awesome `fa-star` → Tabler `ti-star` / `ti-star-filled`
  - 사용자 정보: 이름/이메일 분리, 환영 메시지 제거
  - 사이드바 너비: 288px → 260px
- `src/app/component.nav.aside/view.scss` — 불필요한 SCSS 정리

### 레이아웃 (layout.aside)
- `src/app/layout.aside/view.pug` — Notion 스타일 적용
  - 콘텐츠 배경: `bg-[#f6f7fb]` → `bg-white`
  - 사이드바 토글 버튼: `bg-slate-200` → `bg-neutral-200`, FA → Tabler chevron 아이콘
  - 토글 위치: `left-[272px]` → `left-[244px]` (260px 사이드바에 맞춤)
