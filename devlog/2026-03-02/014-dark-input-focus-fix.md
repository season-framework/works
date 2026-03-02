# 다크 배경 Input 포커스 스타일 개선

- **ID**: 014
- **날짜**: 2026-03-02
- **유형**: 버그 수정

## 작업 요약
이슈보드 플로팅 버튼 영역의 다크 배경(`bg-neutral-900/800`) input 요소에 포커스 시 ring이 아이콘 영역과 겹치거나 대비가 약한 문제를 수정. 멤버 검색 input의 focus:ring 제거, 이슈 검색 컨테이너에 focus-within:border-neutral-500 추가.

## 변경 파일 목록

### Portal App (works/project.issueboard)
- `view.pug` L210: 멤버 검색 input에서 `focus:ring-1 focus:ring-neutral-600` 제거, `focus:outline-none`만 유지
- `view.pug` L240: 이슈 검색 컨테이너 div에 `transition-colors focus-within:border-neutral-500` 추가하여 포커스 시 border 밝아지도록 피드백 처리
