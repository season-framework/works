# 위키 탐색 페이지 Notion 스타일 디자인 개편

- **ID**: 009
- **날짜**: 2026-02-28
- **유형**: 리팩토링

## 작업 요약
위키 탐색(page.explore.wiki) 페이지를 Notion 스타일 디자인 가이드라인에 맞게 전면 개편하였다. gray/slate 계열 색상을 neutral로 전환, Font Awesome 아이콘을 Tabler Icons로 교체, 필터/카드/모달/빈상태 등 모든 UI를 통일된 디자인 시스템에 맞게 재작성하였다.

## 변경 파일 목록

### 위키 탐색 페이지 (src/app/page.explore.wiki)
- **view.pug**: 전면 재작성
  - 레이아웃: `max-w-6xl mx-auto px-8 py-8` 적용
  - 위키 카드: `border-neutral-200`, `hover:bg-neutral-50`, 아이콘+제목+업데이트일 구조
  - 필터 사이드바: ring 스타일 라디오 버튼, `has-[:checked]` blue 활성 스타일
  - 검색 입력: `border-neutral-200`, focus ring 패턴, Tabler search 아이콘
  - 빈 상태: `ti-book-off` 아이콘 + 텍스트 패턴 (SVG 이미지 제거)
  - 모달: `bg-black/50` 오버레이, `rounded-xl shadow-xl`, `ti-x` 닫기 버튼
  - 로딩: `animate-pulse` 스켈레톤 패턴
  - Font Awesome 제거, indigo → blue 전환
