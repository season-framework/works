# 프로젝트 멤버 컴포넌트 Notion 스타일 디자인 개편

- **ID**: 015
- **날짜**: 2026-02-28
- **유형**: 리팩토링

## 작업 요약
portal/works/app/project.member 컴포넌트를 Notion 스타일로 전면 개편. Notion 스타일 테이블, ring 뱃지, neutral 색상 체계 적용.

## 변경 파일 목록

### portal/works/app/project.member
- **view.pug**: 전면 재작성
  - 카드: `rounded-2xl border-gray-300` → `rounded-lg border-neutral-200`
  - 테이블: `bg-slate-50` → `bg-neutral-50`, `divide-neutral-100`
  - 입력/셀렉트: `border-neutral-200 rounded-md` + focus ring
  - It's Me 뱃지: `bg-orange-500` → amber ring 스타일
  - 삭제: `bg-red-500 rounded-full` → `ti-x` 아이콘 + hover red
