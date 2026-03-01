# 프로젝트 캘린더 카테고리/모달 UI 개선

- **ID**: 008
- **날짜**: 2026-03-02
- **유형**: 기능 추가

## 작업 요약
프로젝트 캘린더 UI 4건 개선: (1) 카테고리 색상 편집 기능 추가 (2) 카테고리 생성 시 색상 선택을 input[type=color]에서 16색 프리셋 팔레트로 변경 (3) 일정 생성/편집 모달에서 색상 선택 제거 (카테고리 색상 사용) (4) 참가자 드롭다운이 모달 영역을 넘어가는 오버플로우 수정 (상향 전환)

## 변경 파일 목록

### Portal App (project.calendar)
- `src/portal/works/app/project.calendar/view.ts`:
  - `editingCategoryColor` 상태 변수 추가
  - `colors` 배열 8색 → 16색 확장
  - `startEditCategory()`: 편집 시 기존 색상 로드
  - `saveEditCategory()`: 색상 변경 데이터 전송 추가
  - `addCategory()`: 생성 후 기본 색상으로 리셋
- `src/portal/works/app/project.calendar/view.pug`:
  - 카테고리 추가 영역: input[type=color] → 색상 스와치 그리드
  - 카테고리 편집 모드: 이름 입력 아래 색상 스와치 행 추가
  - 일정 모달: "색상" 섹션 전체 제거
  - 참가자 드롭다운: `top-full mt-1` → `bottom-full mb-1` (상향 오픈)
  - 모달 컨테이너: `flex flex-col max-h-[85vh]` + body `flex-1 min-h-0 overflow-y-auto`
