# 멘션 배지 CSS 클래스 방식 전환

- **ID**: 004
- **날짜**: 2026-03-06
- **유형**: 버그 수정

## 작업 요약
Angular의 `[innerHTML]` 바인딩은 DomSanitizer가 인라인 `style` 속성을 자동 제거하여 멘션 배지 스타일이 미적용되던 문제를 해결. 인라인 스타일 대신 CSS 클래스(`wiz-mention`)를 사용하도록 변경하고, `::ng-deep`으로 동적 삽입 콘텐츠에 스타일 적용.

## 변경 파일 목록
### 프론트엔드 (Portal Works)
- `src/portal/works/libs/struct/display.ts` — `markdown()` 메서드: 인라인 `style` → `class="wiz-mention"` 변경
- `src/portal/works/widget/message.body/view.scss` — `:host ::ng-deep .wiz-mention` 스타일 정의 추가
