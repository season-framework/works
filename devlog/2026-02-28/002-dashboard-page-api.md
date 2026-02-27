# 대시보드 페이지 생성 및 API 구현

- **ID**: 002
- **날짜**: 2026-02-28
- **유형**: 기능 추가

## 작업 요약
`page.dashboard` 앱을 생성하고 (viewuri: `/dashboard`, layout: `layout.aside`, controller: `user`), api.py에 Dashboard Struct의 `load()` 메서드를 호출하는 `load()` 함수를 구현했다. app.json에서 불필요한 input을 제거하고 category를 정리했다.

## 변경 파일 목록

### 신규
- `src/app/page.dashboard/app.json`: 대시보드 페이지 앱 설정
- `src/app/page.dashboard/api.py`: Dashboard Struct 호출하여 데이터 반환
- `src/app/page.dashboard/view.pug`: 빈 템플릿 (FN-0029에서 구현 예정)
- `src/app/page.dashboard/view.ts`: 빈 컴포넌트 (FN-0029에서 구현 예정)
