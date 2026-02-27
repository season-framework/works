# 관리자 페이지 Notion 스타일 디자인 개편

- **ID**: 012
- **날짜**: 2026-02-28
- **유형**: 리팩토링

## 작업 요약
관리자(page.admin) 래퍼 페이지를 Notion 스타일로 개편. bg-gray-50 배경 제거, 레이아웃을 max-w-5xl/px-8/py-8로 통일, hr 구분선을 space-y-8 간격으로 대체.

## 변경 파일 목록

### 관리자 페이지 (src/app/page.admin)
- **view.pug**: 래퍼 스타일 변경
  - 배경: `bg-gray-50` → 제거 (상위 bg-white 활용)
  - 레이아웃: `max-w-5xl mx-auto px-8 py-8`
  - 구분: `hr.my-3` → `space-y-8`
  - 스크롤: `h-full overflow-y-auto` 래퍼 추가
