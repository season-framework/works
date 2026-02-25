# wiz.response 에러 처리 표준화

- **ID**: 005
- **날짜**: 2026-02-26
- **유형**: 버그 수정

## 작업 요약
wiz.response.status()를 try/except 안에서 호출하는 안티패턴을 전면 제거하고, .get() 호출 후 None 체크가 누락된 부분을 보강하였다. 특히 namespace 중복 체크에서 `Excpetion` 오타로 인한 NameError가 항상 except로 빠져 정상 동작하지 않던 버그 3건도 수정하였다.

## 변경 파일 목록

### try/except 안티패턴 제거 + None 체크 추가
- `src/portal/works/route/project/controller.py` — 전체 리라이트: 모든 try/except 제거, project None 가드 추가, Excpetion 오타 수정
- `src/portal/wiki/route/book/controller.py` — 전체 리라이트: 동일 패턴 수정
- `src/app/page.explore.project/api.py` — namespace 체크 try/except 제거, create/delete/update에 None 가드 추가

### try/except 안티패턴 제거 + None 체크 추가 (upload 핸들러)
- `src/portal/works/route/file.workspace/controller.py` — upload의 try/except 제거, project None 가드 추가
- `src/portal/wiki/route/wiki.workspace/controller.py` — upload의 try/except 제거, book None 가드 추가

### None 체크 추가
- `src/app/page.mypage/api.py` — session(), change_password()에서 db.get() 후 None 체크 추가
- `src/app/page.wikidownload/api.py` — bookModel.get() 후 None 체크 추가, content 접근 시 try/except → 안전한 dict 접근으로 변경
- `src/portal/works/app/project.issueboard/api.py` — 모듈 레벨 projectModel.get() 후 None 가드 추가
- `src/portal/works/app/project.issueboard.issue/api.py` — 동일
- `src/portal/works/app/project.wiki/api.py` — 동일
- `src/portal/works/app/project.meeting/api.py` — 동일

### 핵심 변경 패턴

#### Before (안티패턴)
```python
try:
    result = struct.do_something()
    wiz.response.status(200, result)  # ResponseException이 except로 잡힘
except Exception as e:
    wiz.response.status(400, str(e))  # 항상 여기로 옴
```

#### After (올바른 패턴)
```python
result = struct.do_something()
wiz.response.status(200, result)
```

#### Before (None 체크 누락)
```python
project = projectModel.get(pid)
# project이 None이면 아래에서 AttributeError 발생
project.member.list()
```

#### After (None 가드)
```python
project = projectModel.get(pid)
if project is None:
    wiz.response.status(404, message="프로젝트를 찾을 수 없습니다")
project.member.list()
```
