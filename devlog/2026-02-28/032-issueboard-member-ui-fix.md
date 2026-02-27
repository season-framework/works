# 이슈보드 멤버조회/구성원 UI 수정

- **ID**: 032
- **날짜**: 2026-02-28
- **유형**: 버그 수정

## 작업 요약
이슈보드 멤버조회 팝업의 하단 화살표를 왼쪽에서 오른쪽으로 이동. 구성원 화면의 `ml-auto`를 제거하여 왼쪽 정렬로 변경. 추가 버튼에 투명 라벨을 추가하여 인풋 높이와 정렬.

## 변경 파일 목록

### 이슈보드 (project.issueboard/view.pug)
- 멤버조회 팝업 하단 화살표: `ml-3` → `flex justify-end pr-5`로 감싸서 오른쪽 정렬

### 구성원 (project.member/view.pug)
- 외부 컨테이너: `max-w-3xl ml-auto` → `max-w-3xl` (왼쪽 정렬)
- 추가 버튼: `div` → `div(class="flex flex-col")` + 투명 라벨 추가로 인풋과 높이 맞춤
