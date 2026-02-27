# 이슈보드 보기모드 토글 리뷰 반영

- **ID**: 030
- **날짜**: 2026-02-28
- **유형**: 버그 수정

## 작업 요약
이슈보드 보기모드 토글 버튼 리뷰 반영: 토글 색상을 반전(활성=밝은 텍스트, 비활성=어두운 텍스트), 토글/멤버조회 버튼 높이·여백·테마 통일(h-9, 동일 패딩, border-neutral-700).

## 변경 파일 목록

### UI
- `src/portal/works/app/project.issueboard/view.pug`: 토글 활성 스타일 `bg-white text-neutral-900` → `text-white`로 변경, 비활성 `text-neutral-400` → `text-neutral-500 hover:text-neutral-300`, 토글/멤버조회 버튼 모두 `h-9` 고정 높이, 동일한 `px-3.5` 패딩, `py-2` 제거 후 flex center 정렬로 통일
