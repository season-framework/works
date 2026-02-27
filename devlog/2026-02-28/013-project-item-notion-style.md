# 프로젝트 상세 페이지 Notion 스타일 디자인 개편

- **ID**: 013
- **날짜**: 2026-02-28
- **유형**: 리팩토링

## 작업 요약
프로젝트 상세(page.project.item) 래퍼 페이지를 Notion 스타일로 개편. 탭별 컨텐츠 래퍼의 padding을 `px-6 py-4`로 통일하고, 방문자 접근 제한 UI를 Notion 스타일 빈 상태 패턴으로 재작성.

## 변경 파일 목록

### 프로젝트 상세 페이지 (src/app/page.project.item)
- **view.pug**: 래퍼 스타일 및 방문자 접근 제한 UI 변경
  - 래퍼 padding: `ml-6`/`mx-6` → `px-6 py-4` 통일
  - 방문자 UI: SVG 이미지 → `ti-lock` 아이콘, `border-neutral-200 rounded-lg`
  - 참가 버튼: `fa-person-running` → `ti-user-plus`, `rounded-md` 스타일
  - gray → neutral 색상 전환
