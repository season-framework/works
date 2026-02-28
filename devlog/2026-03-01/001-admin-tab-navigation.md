# page.admin 탭/섹션 기반 네비게이션 리팩토링

- **ID**: 001
- **날짜**: 2026-03-01
- **유형**: 리팩토링

## 작업 요약
기존 SAML 컴포넌트만 나열하던 page.admin을 좌측 네비게이션 + 우측 콘텐츠 영역의 탭/섹션 기반 관리 대시보드로 리팩토링. viewuri를 `/admin/:section?/:subsection?`으로 변경하고 WizRoute.segment 기반 메뉴 라우팅 구현.

## 변경 파일 목록

### dev 프로젝트
- `src/app/page.admin/app.json`: viewuri `/admin/**` → `/admin/:section?/:subsection?` 변경
- `src/app/page.admin/view.pug`: 좌측 네비게이션(사용자/프로젝트/위키/SAML/시스템설정) + 우측 콘텐츠 영역(*ngIf 분기) 구조로 전면 리팩토링
- `src/app/page.admin/view.ts`: menus 배열, currentSection/currentSubsection 상태, WizRoute.segment 기반 라우팅, navigate() 메서드 구현

### main 프로젝트
- 위 3개 파일 동일 수정 적용
