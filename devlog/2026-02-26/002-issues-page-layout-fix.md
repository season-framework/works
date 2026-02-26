# 이슈모음(/issues) 페이지 레이아웃 깨짐 수정

- **ID**: 002
- **날짜**: 2026-02-26
- **유형**: 버그 수정

## 작업 요약
이슈모음(`/issues`) 페이지의 레이아웃이 깨지는 문제 수정. Angular 컴포넌트 호스트 요소에 `:host` 스타일이 없어 `h-full`이 resolve되지 않고, flex 자식에 `min-h-0`가 빠져 overflow-auto가 동작하지 않는 것이 원인.

## 변경 파일 목록

### 신규 파일
- `src/app/page.issues/view.scss` — `:host { display: block; height: 100%; }` 추가. Angular 라우터 컴포넌트 호스트 요소가 inline 렌더링되어 자식의 `h-full`이 동작하지 않는 문제 해결.

### 수정 파일
- `src/app/page.issues/view.pug`
  - 좌측 패널: `min-h-0` 추가 (flex-col 컨테이너의 overflow 정상 동작)
  - `#issuelist`: `h-full` 제거 + `min-h-0` 추가 (flex-1만으로 크기 결정, overflow-auto 정상 동작)
  - 우측 패널: `min-w-0` 추가 (flex-1 자식의 content overflow 방지)
