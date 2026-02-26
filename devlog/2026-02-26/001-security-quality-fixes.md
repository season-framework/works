# FN-0002~0025 보안/버그/성능/코드품질 전수 수정

- **ID**: 001
- **날짜**: 2026-02-26
- **유형**: 버그 수정 / 보안 강화 / 성능 개선 / 코드 품질

## 작업 요약
todo.md에 정의된 24건의 보안/버그/성능/코드품질 작업(FN-20260226-0002~0025)을 전수 수정.
CRITICAL(권한 우회, Path Traversal), HIGH(인증 누락, Null 체크), MEDIUM(리소스 누수, N+1 쿼리, XSS), LOW(a11y, 하드코딩 URL, Model 네이밍) 카테고리 포함.

## 변경 파일 목록

### CRITICAL/보안 (FN-0002~0004)
- `src/route/switch/controller.py` — role 검사 `not in 'admin'` → `!= 'admin'`, 불필요한 membership 강제설정 제거
- `src/portal/works/route/project/controller.py` — safe_path() 함수 추가, 모든 drive 액션에 경로 검증 적용
- `src/app/page.explore.project/api.py` — Excpetion 오타 수정 (try/except 제거 → 직접 if 체크)
- `src/portal/wiki/route/book/controller.py` — Excpetion 오타 수정

### HIGH/보안 (FN-0005~0011)
- `src/portal/works/route/file.workspace/controller.py` — wiz.response anti-pattern 수정, 세션 캐시 인증 제거
- `src/portal/wiki/route/wiki.workspace/controller.py` — 동일 수정
- `src/app/page.mypage/api.py` — 화이트리스트 패턴 적용, 미사용 Tool 클래스 제거
- `src/portal/works/app/project.issueboard/socket.py` — _auth() 인증 함수 추가
- `src/portal/works/app/project.meeting/socket.py` — _auth() 인증 함수 추가
- `src/portal/works/app/project.issueboard/api.py`, `project.issueboard.issue/api.py`, `project.meeting/api.py`, `project.wiki/api.py` — project null 체크 추가

### HIGH/성능 (FN-0010)
- `src/app/page.project.item/view.ts` — ngDoCheck → Router.events NavigationEnd 구독
- `src/app/page.wiki.item/view.ts` — 동일 수정

### MEDIUM/코드품질 (FN-0012~0013)
- `src/portal/season/model/orm.py` — bare except → 구체적 예외 타입 (AttributeError)
- `src/portal/works/model/project.py` — bare except → (KeyError, TypeError), Exception
- `src/portal/works/model/struct/issueboard/worker.py` — bare except → Exception
- `src/portal/wiki/model/struct/revision.py` — bare except → Exception
- `src/portal/wiki/model/book.py` — bare except → Exception
- `src/portal/works/model/struct/issueboard/issue.py` — bare except → (AttributeError, TypeError)
- `src/portal/works/route/project/controller.py` — if→elif 체인 변환
- `src/portal/wiki/route/book/controller.py` — if→elif 체인 변환

### MEDIUM/리소스 (FN-0016)
- `src/portal/works/route/file.workspace/controller.py` — Image.open() with 문
- `src/portal/wiki/route/wiki.workspace/controller.py` — Image.open() with 문
- `src/portal/works/route/project/controller.py` — ZipFile with 문, shutil.remove → os.remove

### MEDIUM/UI+TS (FN-0017~0019)
- `src/app/page.explore.project/view.pug` — hover:bg-blug-600 오타 수정, img XSS→[ngStyle]
- `src/app/layout.aside/view.pug` — z-50 중복 제거
- `src/app/page.explore.wiki/view.pug` — img XSS→[ngStyle]
- `src/app/page.issues/view.pug` — img XSS→[ngStyle]
- `src/app/page.authenticate/view.ts` — URLSearchParams 전환
- `src/app/page.issues/view.ts` — sort return 0 수정
- `src/app/page.mypage/view.ts` — await 추가
- `src/app/component.pagination/view.ts` — Math 프로퍼티 선언
- `src/app/page.admin/view.ts` — import 경로 @wiz/libs 통일

### MEDIUM/성능 (FN-0020)
- `src/portal/works/model/struct/member.py` — N+1 user info → 배치 조회
- `src/portal/wiki/model/struct/revision.py` — N+1 user info → 배치 조회
- `src/portal/works/model/struct/issueboard/message.py` — N+1 reply → 배치 조회
- `src/portal/works/model/struct/issueboard/label.py` — N+1 close/cancel count → 배치 Counter

### LOW (FN-0021~0025)
- `src/app/page.explore.project/view.pug` — alt, aria-label 추가
- `src/app/page.explore.wiki/view.pug` — alt, aria-label 추가
- `src/app/page.issues/view.pug` — aria-label 추가
- `src/app/page.mypage/view.pug` — [ngStyle] 전환 + aria-label
- `src/app/page.wikidownload/view.ts` — auth.allow() 주석 복원
- `config/season.py` — site_url 설정 추가
- `src/portal/wiki/route/book/controller.py` — 하드코딩 URL → config site_url 참조
- `src/portal/works/model/project.py` — untracks() @staticmethod 추가
- `src/portal/wiki/model/struct/access.py` — type→access_type 파라미터, isinstance() 사용
- `src/app/component.nav.aside/api.py` — portal/modules 미존재 참조 방어 처리
