# 마이페이지 Notion 스타일 디자인 개편

- **ID**: 011
- **날짜**: 2026-02-28
- **유형**: 리팩토링

## 작업 요약
마이페이지(page.mypage)를 Notion 스타일 디자인 가이드라인에 맞게 전면 개편하였다. 테이블형 폼 레이아웃을 neutral 색상 체계의 카드 UI로 변환, 입력 필드에 focus ring 패턴 적용, 버튼 스타일 통일.

## 변경 파일 목록

### 마이페이지 (src/app/page.mypage)
- **view.pug**: 전면 재작성
  - 레이아웃: `max-w-3xl mx-auto px-8 py-8`
  - 카드: `border-neutral-200 rounded-lg`, 헤더 `px-5 py-4 border-b`
  - 라벨: `bg-neutral-50 text-neutral-500 font-medium` (기존 `bg-blue-50`)
  - 입력 필드: `border-neutral-200`, `focus:ring-2 focus:ring-blue-500/20`
  - 버튼: 프라이머리 `bg-blue-500 rounded-md`, 세컨더리 `bg-neutral-600`
  - 푸터: `bg-neutral-50 border-t border-neutral-100`
  - gray → neutral 전환, rounded-xl → rounded-md 버튼
