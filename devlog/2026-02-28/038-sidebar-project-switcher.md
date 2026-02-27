# 사이드 메뉴 프로젝트 스위칭 드롭다운 추가

- **ID**: 038
- **날짜**: 2026-02-28
- **유형**: 기능 추가

## 작업 요약
사이드 메뉴 하단에 '프로젝트 이동' 드롭다운을 추가하여, 현재 사용자가 참여 중인 전체 프로젝트 목록에서 검색·선택하여 즉시 해당 프로젝트로 이동(스위칭)할 수 있도록 구현. 기존 레거시 코드(portal/modules)를 제거하고 Dashboard.my_projects() 재사용.

## 변경 파일 목록

### 백엔드 API (component.nav.aside/api.py)
- 레거시 load_menu/request_count 코드 제거
- `my_projects()` 엔드포인트 추가: Dashboard.my_projects() 호출하여 참여 프로젝트 목록 반환

### 프론트엔드 로직 (component.nav.aside/view.ts)
- `projectSwitcher` 상태 객체 추가 (open, projects, keyword)
- `loadMyProjects()`: API 호출로 프로젝트 목록 로드
- `toggleProjectSwitcher()`: 드롭다운 토글
- `filteredProjects()`: 키워드 기반 프로젝트 필터링
- `switchProject()`: 선택한 프로젝트로 이동
- `clickout()` 수정: 외부 클릭 시 드롭다운 닫기

### 프론트엔드 템플릿 (component.nav.aside/view.pug)
- 사이드바 하단에 `project-switcher-container` 영역 추가
- 위로 열리는 드롭다운 패널 (검색 입력 + 프로젝트 목록 max-h-52 스크롤)
- 현재 프로젝트 하이라이트 표시
- '프로젝트 이동' 트리거 버튼
