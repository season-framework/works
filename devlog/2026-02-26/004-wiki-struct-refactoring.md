# wiki 패키지 Struct 패턴 리팩토링

- **ID**: 004
- **날짜**: 2026-02-26
- **유형**: 리팩토링

## 작업 요약
wiki 패키지의 model/book.py를 Struct 패턴으로 리팩토링하였다. Composite Struct 진입점(struct.py)을 생성하고, Book 클래스를 struct/book.py로 이동하였다. 기존 호출자 호환을 위해 model/book.py를 래퍼로 유지하였다.

## 변경 파일 목록
### 생성
- `src/portal/wiki/model/struct.py` — Composite Struct 진입점 (Struct 싱글톤, db() 헬퍼, book 프로퍼티)
- `src/portal/wiki/model/struct/book.py` — Book Aggregate Root (기존 book.py에서 이동, 클래스명 Model→Book, Model = Book)

### 수정
- `src/portal/wiki/model/book.py` — 전체 코드 → 3줄 backward-compat 래퍼 (`Model = wiz.model("portal/wiki/struct/book")`)
