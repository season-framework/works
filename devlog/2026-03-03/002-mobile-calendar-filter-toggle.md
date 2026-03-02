# 모바일 캘린더 프로젝트 필터 반응형 토글 처리

- **ID**: 002
- **날짜**: 2026-03-03
- **유형**: 버그 수정

## 작업 요약
모바일에서 캘린더 화면의 프로젝트 필터/카테고리 사이드바가 화면을 차지하여 캘린더가 보이지 않는 문제 수정. 모바일에서는 사이드바를 기본 숨김 처리하고, 헤더의 토글 버튼으로 오버레이 형태로 표시/숨김 전환하도록 구현.

## 변경 파일 목록

### 메인 캘린더 (`src/app/page.calendar/`)

| 파일 | 변경 내용 |
|------|-----------|
| `view.scss` | `.filter-sidebar` 미디어쿼리 추가 (모바일에서 fixed 포지셔닝, `.mobile-hidden` 숨김) |
| `view.pug` | 헤더에 `sm:hidden` 필터 토글 버튼 추가, 사이드바에 `filter-sidebar` 클래스 및 `[class.mobile-hidden]` 바인딩, 모바일 오버레이 배경 div 추가 |
| `view.ts` | `showFilterSidebar: boolean = false` 프로퍼티 추가 |

### 프로젝트 내 캘린더 (`src/portal/works/app/project.calendar/`)

| 파일 | 변경 내용 |
|------|-----------|
| `view.scss` | 동일 `.filter-sidebar` 미디어쿼리 추가 |
| `view.pug` | 헤더에 `sm:hidden` 카테고리 토글 버튼 추가, 사이드바에 반응형 처리, 모바일 오버레이 배경 추가 |
| `view.ts` | `showFilterSidebar: boolean = false` 프로퍼티 추가 |
