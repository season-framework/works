# 프로젝트 탐색 페이지 Notion 스타일 디자인 개편

- **ID**: 008
- **날짜**: 2026-02-28
- **유형**: 리팩토링

## 작업 요약
프로젝트 탐색(page.explore.project) 페이지를 Notion 스타일 디자인 가이드라인에 맞게 전면 개편하였다. gray 계열 색상을 neutral 계열로 전환하고, Font Awesome 아이콘을 Tabler Icons로 교체하며, 카드/필터/모달/빈상태 등 모든 UI 요소를 통일된 디자인 시스템에 맞게 재작성하였다.

## 변경 파일 목록

### 프로젝트 탐색 페이지 (src/app/page.explore.project)
- **view.pug**: 전면 재작성
  - 레이아웃: `max-w-6xl mx-auto px-8 py-8` 적용
  - 프로젝트 카드: `border-neutral-200`, `hover:bg-neutral-50`, 좌측 아이콘+정보 구조
  - 필터 사이드바: ring 스타일 라디오 버튼, `has-[:checked]` 활성 스타일 (blue)
  - 검색 입력: `border-neutral-200`, `focus:ring-2 focus:ring-blue-500/20` 패턴
  - 빈 상태: Tabler `ti-folder-off` 아이콘 + 텍스트 패턴 (SVG 이미지 제거)
  - 모달: `bg-black/50` 오버레이, `rounded-xl shadow-xl`, `ti-x` 닫기 버튼
  - 로딩: `animate-pulse` 스켈레톤 패턴
  - Font Awesome → Tabler Icons 전환 (`fa-person-running` → `ti-plus`, `fa-xmark` → `ti-x`)
