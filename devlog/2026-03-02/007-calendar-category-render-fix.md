# 프로젝트 캘린더 카테고리 편집 즉시 반영 수정 + 인스트럭션 9.11 등록

- **ID**: 007
- **날짜**: 2026-03-02
- **유형**: 버그 수정

## 작업 요약
프로젝트 캘린더에서 카테고리 편집(변경) 버튼 클릭 시 UI가 즉시 반영되지 않던 문제 수정. `startEditCategory()`와 `cancelEditCategory()`에서 상태 변경 후 `service.render()` 호출 누락이 원인. 이 패턴을 코어 인스트럭션(섹션 9.11)에 트러블슈팅 항목으로 등록.

## 변경 파일 목록

### Portal App (project.calendar)
- `src/portal/works/app/project.calendar/view.ts`: `startEditCategory()`, `cancelEditCategory()` → async 변환 + `await this.service.render()` 추가

### 코어 인스트럭션
- `.github/copilot-instructions.md`: 섹션 9.11 "이벤트 핸들러에서 service.render() 누락 시 UI 미갱신" 추가
