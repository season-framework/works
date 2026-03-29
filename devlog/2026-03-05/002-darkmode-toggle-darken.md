# 다크모드 토글 버튼 어둡게 조정

- **ID**: 002
- **날짜**: 2026-03-05
- **유형**: 버그 수정

## 작업 요약
다크모드 상태에서 라이트/다크 전환 토글 버튼이 밝은 회색으로 표시되어 주변 어두운 UI와 이질감을 유발하던 문제를 수정. 토글 트랙, 썸(thumb) 색상을 더 어둡게 변경하여 다크모드 사이드바에 자연스럽게 통합.

## 변경 파일 목록

### 스타일 수정
- `src/app/component.nav.aside/view.scss`
  - `[data-theme="dark"]` 블록: track `#27272a→#18181b`, thumb `#3f3f46→#2a2a30`, shadow opacity `0.3→0.4`, active text `#fafafa→#e4e4e7`
