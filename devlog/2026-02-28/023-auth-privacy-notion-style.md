# 인증·기타 페이지 Notion 스타일 디자인 개편

- **ID**: 023
- **날짜**: 2026-02-28
- **유형**: 리팩토링

## 작업 요약
page.authenticate, page.privacy 페이지를 Notion 스타일 디자인 가이드라인에 맞춰 개편. gray→neutral 전환, shadow 제거, 입력 필드 focus ring 패턴 적용, FA 아이콘→Tabler 교체. page.wikidownload는 CKEditor 최소 래퍼(3줄)로 변경 불필요.

## 변경 파일 목록

### page.authenticate/view.pug
- `max-w-[600px]` → `max-w-[520px]`, `rounded-md` → `rounded-xl`, `border border-neutral-200` 추가
- 입력 필드: 인라인 스타일 → `rounded-md border border-neutral-200 focus:border-neutral-400 focus:ring-1 focus:ring-neutral-400` 통일
- 버튼: `border-black bg-black hover:text-gray-700 hover:bg-blue-50` → `bg-neutral-900 hover:bg-neutral-800 text-sm font-medium`
- 링크: `text-gray-500` → `text-neutral-500 hover:text-neutral-700`
- `fa-solid.fa-check-circle` → `ti.ti-circle-check`
- 회원가입 폼: 각 필드 label+input 쌍으로 `space-y-4` 레이아웃, disabled 필드 `bg-neutral-50`

### page.privacy/view.pug
- `shadow-lg` 제거 → `border border-neutral-200`
- `bg-opacity-60` 유지, `text-gray-800` → `text-neutral-800`
- `border-gray-300` → `border-neutral-200`
- 본문 텍스트 `text-sm text-neutral-600`, 헤딩 `text-lg font-bold text-neutral-900`
- `space-y-1` 추가로 리스트 간격 정리
