# 메인 캘린더 로딩 해제 안됨 버그 수정

- **ID**: 006
- **날짜**: 2026-03-02
- **유형**: 버그 수정

## 작업 요약
메인 캘린더(`page.calendar`) 새로고침 시 전체 화면 로딩 오버레이가 사라지지 않는 버그 수정. `service.init()` 내부의 `loading.show()` 호출 이후 `loading.hide()`가 호출되지 않아 발생.

## 변경 파일 목록

### page.calendar
- `src/app/page.calendar/view.ts` — `ngOnInit()`에 `this.service.auth.allow()` 호출 추가 (내부에서 `loading.hide()` 처리), try/catch로 에러 시에도 로딩 해제 보장
