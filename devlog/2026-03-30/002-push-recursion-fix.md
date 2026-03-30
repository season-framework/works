# Push 알림 서버 전송 실패(RecursionError) 수정

- **ID**: 002
- **날짜**: 2026-03-30
- **유형**: 버그 수정

## 작업 요약
WIZ 서버 내에서 pywebpush 호출 시 `maximum recursion depth exceeded` 에러로 Push 알림이 전혀 전송되지 않던 문제를 수정했다. gevent monkey-patching이 WIZ의 `exec()` 실행 환경과 결합될 때 `ssl.SSLContext.minimum_version` setter에서 무한 재귀가 발생하는 것이 근본 원인이었다. webpush 호출을 별도 subprocess에서 실행하도록 변경하여 gevent-patched SSL 환경을 우회했다.

## 근본 원인 분석
- **증상**: WIZ 서버 API에서 `Push.send()` 호출 시 `RecursionError: maximum recursion depth exceeded`
- **위치**: `ssl.py:545 SSLContext.minimum_version` setter → `super(SSLContext, SSLContext).minimum_version.__set__(self, value)` 무한 재귀
- **원인**: gevent `monkey.patch_all()`이 `ssl.SSLContext`를 패치하면서 `super()` 해결이 다시 패치된 클래스로 돌아감. 커맨드라인에서는 재현 불가(WIZ `exec()` 컴파일러 환경 특유 문제).
- **해결**: webpush 호출을 `subprocess.run()`으로 분리하여 패치되지 않은 새 Python 프로세스에서 실행

## 변경 파일 목록

### Push Struct (핵심 수정)
- `src/portal/works/model/struct/push.py`
  - `_send_webpush_subprocess()` 헬퍼 함수 추가: subprocess로 webpush 실행
  - `PUSH_WORKER_SCRIPT` 상수: subprocess에서 실행할 Python 스크립트
  - `send()` 메서드: 직접 `webpush()` 호출 → `_send_webpush_subprocess()` 호출로 변경
  - stdin으로 JSON 데이터 전달 (보안: 커맨드 인젝션 방지)
  - 불필요한 traceback 디버그 로깅 제거

### 디버그 코드 정리
- `src/app/component.nav.aside/api.py`
  - `push_test()` 임시 디버그 엔드포인트 제거
