# works 패키지 Struct 패턴 리팩토링

- **ID**: 003
- **날짜**: 2026-02-26
- **유형**: 리팩토링

## 작업 요약
works 패키지의 model/project.py를 Struct 패턴으로 리팩토링하였다. Composite Struct 진입점(struct.py)을 생성하고, Project 클래스를 struct/project.py로 이동하였다. 기존 호출자 호환을 위해 model/project.py를 래퍼로 유지하였다.

## 변경 파일 목록
### 생성
- `src/portal/works/model/struct.py` — Composite Struct 진입점 (Struct 싱글톤, db() 헬퍼, project 프로퍼티)
- `src/portal/works/model/struct/project.py` — Project Aggregate Root (기존 project.py에서 이동, Model = Project)

### 수정
- `src/portal/works/model/project.py` — 전체 코드 → 3줄 backward-compat 래퍼 (`Model = wiz.model("portal/works/struct/project")`)
