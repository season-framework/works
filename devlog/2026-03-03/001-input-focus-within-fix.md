# 아이콘 포함 Input 포커스 영역 전수조사 및 수정

- **ID**: 001
- **날짜**: 2026-03-03
- **유형**: 버그 수정

## 작업 요약
아이콘이 포함된 검색 Input 컴포넌트에서 포커스 시 시각적 피드백(ring/border)이 실제 text input 요소에만 적용되고, 아이콘을 포함한 전체 컨테이너에는 적용되지 않는 문제를 전수조사하여 수정. JS 기반 `(focus)/(blur)` 토글 패턴도 CSS `focus-within`으로 통일.

## 변경 파일 목록

### 유형 B: input 자체 focus 스타일 → 컨테이너 focus-within 이동 (3건)

| 파일 | 변경 내용 |
|------|-----------|
| `src/app/page.issues/view.pug` | `div.relative`에 `border`, `focus-within:ring-2/border-blue-400` 추가, input에서 border/ring 제거 |
| `src/app/page.explore.project/view.pug` | 동일 패턴 적용 |
| `src/app/page.explore.wiki/view.pug` | 동일 패턴 적용 |

### 유형 A: JS (focus)/(blur) 토글 → CSS focus-within 교체 (5건)

| 파일 | 변경 내용 |
|------|-----------|
| `src/app/component.nav.aside/view.pug` | `[class.border-blue-400]` + `(focus)/(blur)` 제거, `focus-within:border-blue-400` 추가 |
| `src/portal/season/app/admin.user/view.pug` | 동일 패턴 적용 |
| `src/portal/works/app/admin.project/view.pug` | 동일 패턴 적용 |
| `src/portal/wiki/app/admin.wiki/view.pug` | 동일 패턴 적용 |
| `src/portal/works/app/project.issueboard/view.pug` | 게시판 모드 검색 input, 동일 패턴 적용 |

### 수정 불필요 확인 (2건)

| 파일 | 사유 |
|------|------|
| `src/portal/works/app/project.issueboard/view.pug` (L241 이슈검색) | 이미 `focus-within:border-neutral-500` 적용 완료 |
| `src/portal/works/app/project.issueboard/view.pug` (L210 멤버검색) | 다크 배경 input, 의도적으로 ring 없음 |
