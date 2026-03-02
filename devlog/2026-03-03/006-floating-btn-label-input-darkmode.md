# 이슈보드 플로팅 버튼 / 라벨 입력 다크모드 수정

- **ID**: 006
- **날짜**: 2026-03-03
- **유형**: 버그 수정

## 작업 요약
다크모드에서 이슈보드 하단 플로팅 버튼(bg-neutral-900)이 배경에 묻히는 문제와 칸반 라벨 입력의 배경색이 글로벌 form input 오버라이드에 의해 강제 변경되는 문제를 수정. bg-neutral-900을 `#0c0c0e`→`#1e1e26`으로 밝게 조정하고, `input.bg-inherit`/`input.bg-transparent` 예외 규칙을 추가.

## 변경 파일 목록

### 스타일
- `src/portal/season/styles/content/color.scss`:
  - `bg-neutral-900`: `#0c0c0e` → `#1e1e26` (배경과 대비 확보)
  - `bg-neutral-900.text-white`: 동일 수정
  - `input.bg-inherit` / `input.bg-transparent`: 글로벌 form input bg 오버라이드 예외 처리
