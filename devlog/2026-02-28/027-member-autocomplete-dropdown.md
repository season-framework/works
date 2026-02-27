# 프로젝트 멤버 추가 자동완성 드롭다운 구현

- **ID**: 027
- **날짜**: 2026-02-28
- **유형**: 기능 추가

## 작업 요약
프로젝트 구성원 관리 화면에서 멤버 추가 시 단순 이메일 텍스트 입력 대신 사용자 검색 자동완성 드롭다운으로 변경. DB의 membership 필드를 기준으로 내부 사용자(admin/staff)와 외부 사용자(guest/user)를 구분하여 그룹별로 표시.

## 변경 파일 목록

### API (백엔드)
- `src/portal/works/app/project.member/api.py`: 신규 작성. `search()` 함수 — keyword 파라미터로 name/email 검색, membership 기준 내부/외부 분류하여 반환

### UI (프론트엔드)
- `src/portal/works/app/project.member/view.pug`: 이메일 입력 필드를 자동완성 검색 입력으로 교체. 드롭다운에 내부/외부 그룹 헤더, 사용자 아바타·이름·이메일·멤버십 배지 표시. 선택된 사용자 칩 표시. 키보드 네비게이션 지원.
- `src/portal/works/app/project.member/view.ts`: 자동완성 로직 추가 — 300ms 디바운스 검색, 키보드 네비게이션(↑↓/Enter/Esc), 사용자 선택/해제, 외부 클릭 시 닫기, OnDestroy 정리
- `src/portal/works/app/project.member/view.scss`: 드롭다운 스크롤바 커스텀 스타일 추가
