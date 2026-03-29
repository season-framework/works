# 알림함 이슈 클릭 시 이슈카드 팝업 표시

- **ID**: 011
- **날짜**: 2026-03-06
- **유형**: 버그 수정 / 기능 추가

## 작업 요약
알림함에서 이슈 클릭 시 `service.href()`로 페이지 이동하면 라우트 패턴 불일치로 메인 페이지로 리다이렉트되는 문제 수정. 이슈보드의 이슈카드 팝업 패턴(`wiz-portal-works-project-issueboard-issue` 컴포넌트)을 활용하여 알림함 내에서 직접 이슈카드를 모달로 표시하도록 변경.

## 변경 파일 목록

### TypeScript (page.notification/view.ts)
- `Project` 서비스 임포트 및 의존성 주입 추가
- `issue` 객체 추가: `{ id, modal, event }` 구조
- `openIssue(item)` 메서드 추가: `project.init(namespace)` 후 이슈카드 모달 활성화
- 기존 `navigateToIssue()` 제거

### Template (page.notification/view.pug)
- 아이템 클릭 핸들러를 `navigateToIssue(item)` → `openIssue(item)`으로 변경
- 하단에 `wiz-portal-works-project-issueboard-issue` 컴포넌트 추가 (모달 표시)
