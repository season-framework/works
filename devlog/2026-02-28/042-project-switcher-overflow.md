# 프로젝트 스위칭 드롭다운 오버플로우 클리핑 수정

- **ID**: 042
- **날짜**: 2026-02-28
- **유형**: 버그 수정

## 작업 요약
프로젝트 스위칭 드롭다운 패널이 사이드바 영역을 넘어갈 때 잘리는 현상 수정. 사이드바 루트 div의 `overflow-y-auto`가 CSS 클리핑 컨텍스트를 생성하여 `absolute` 포지셔닝된 드롭다운(w-[320px])이 사이드바(w-[260px]) 밖으로 나갈 때 클리핑되는 문제를 `position: fixed`로 변경하여 해결.

## 변경 파일 목록

### dev 프로젝트
- `src/app/component.nav.aside/view.pug`: 드롭다운 패널 `absolute bottom-full` → `fixed` + `[ngStyle]="projectSwitcher.panelStyle"` 변경
- `src/app/component.nav.aside/view.ts`: `projectSwitcher` 상태에 `panelStyle` 추가. `toggleProjectSwitcher()`에서 트리거 버튼의 `getBoundingClientRect()`로 fixed 좌표 계산

### main 프로젝트
- `src/app/component.nav.aside/view.pug`: dev와 동일 수정
- `src/app/component.nav.aside/view.ts`: dev와 동일 수정
