# Modal Alert 취소 버튼 텍스트 수정

- **ID**: 012
- **날짜**: 2026-03-01
- **유형**: 버그 수정

## 작업 요약
Modal alert 컴포넌트에서 cancel 속성에 `true`(boolean)가 전달될 때 버튼 텍스트에 "true"가 그대로 표시되는 문제를 수정. alert.ts 기본값을 `cancel: '취소'`로 변경하고, cancel 미지정이거나 부적절한 값을 사용하는 호출부 14곳을 전수조사하여 수정.

## 변경 파일 목록

### 핵심 수정 — alert 기본값
- `src/portal/season/libs/alert.ts`: `cancel: true` → `cancel: '취소'`

### 알림용 alert (cancel: false 추가) — 6곳
- `src/portal/season/app/admin.config/view.ts`: 6개 alert.show 호출에 `cancel: false` 추가
- `src/portal/season/app/admin.user/view.ts`: 2개 alert.show 호출에 `cancel: false` 추가
- `src/portal/works/app/admin.project/view.ts`: 1개 alert.show 호출에 `cancel: false` 추가

### cancel 텍스트 한국어화 — 2곳
- `src/portal/works/app/project.member/view.ts`: `cancel: "cancel"` → `cancel: "취소"`
- `src/app/component.nav.aside/view.ts`: `cancel: "cancel"` → `cancel: "취소"`, `action: "logout"` → `action: "로그아웃"`, `title: "Logout"` → `title: "로그아웃"`

### action 텍스트 한국어화 — 1곳
- `src/angular/app/app.component.ts`: `action: "close"` → `action: "닫기"` (error/success 헬퍼 2곳)
