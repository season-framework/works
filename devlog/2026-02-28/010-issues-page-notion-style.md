# 이슈모음 페이지 Notion 스타일 디자인 개편

- **ID**: 010
- **날짜**: 2026-02-28
- **유형**: 리팩토링

## 작업 요약
이슈모음(page.issues) 페이지를 Notion 스타일 디자인 가이드라인에 맞게 전면 개편하였다. 2패널 레이아웃(좌측 이슈 리스트 + 우측 상세)은 유지하면서 색상 체계를 neutral로 전환, 카테고리 탭을 밑줄 스타일로 변경, 이슈 상태 뱃지를 ring 스타일로 통일, Font Awesome 아이콘을 Tabler Icons로 교체하였다.

## 변경 파일 목록

### 이슈모음 페이지 (src/app/page.issues)
- **view.pug**: 전면 재작성
  - 검색 바: `border-neutral-200`, focus ring, Tabler `ti-search`/`ti-refresh` 아이콘
  - 카테고리 탭: 기존 blue fill → 밑줄 스타일 (`border-b-2 border-blue-600`)
  - 이슈 아이템: `hover:bg-neutral-50`, `border-neutral-100` 구분선
  - 선택 아이템: `!bg-blue-50/60 border-l-2 !border-l-blue-500`
  - 뱃지: `rounded-full ring-1 ring-inset` 스타일로 통일
  - 로딩: `animate-pulse` 스켈레톤 패턴
  - Font Awesome (`fa-rotate-right`, `fa-solid`) → Tabler Icons 전환

- **view.ts**: displayColor, displayStatus 메서드 업데이트
  - displayColor: gray → neutral, emerald → green 톤 변경
  - displayStatus: slate/lime/red → neutral/blue/green/red ring 스타일로 변경
  - finish 상태를 red에서 green으로 의미 교정
