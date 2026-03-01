# season.py → DB(system_config) 설정 통합 마이그레이션

- **ID**: 001
- **날짜**: 2026-03-02
- **유형**: 리팩토링

## 작업 요약
season.py 파일 기반 설정을 DB(system_config 테이블) 우선 조회로 통합. config.py Config 모델에 DB_KEY_MAP과 __getattr__ 오버라이드를 추가하여, DB에 값이 있으면 DB를 사용하고 없으면 season.py를 fallback으로 사용하도록 변경. 전체 소스코드에서 wiz.config("season") 직접 호출을 config.py 경유로 통일하고, 관리자 설정 UI에 누락 항목을 추가함.

## 변경 파일 목록

### FN-0024: config.py DB 설정 통합
- `src/portal/season/model/config.py`: DB_KEY_MAP 추가, __getattr__/__getitem__/get() 오버라이드로 DB 우선 조회. site_url, saml_mode DEFAULT_VALUES 추가.

### FN-0025: smtp.py 모듈 로드 시점 문제 해결
- `src/portal/season/model/smtp.py`: 모듈 최상위 SMTP_* 상수 제거, send() 호출 시마다 config를 동적으로 읽도록 변경.

### FN-0026: wiz.config("season") 직접 호출 제거
- `src/portal/saml/model/struct.py`: wiz.config("season") → wiz.model("portal/season/config") 경유
- `src/portal/saml/model/struct/process.py`: wiz.config("season").get("saml_acs") → config.get("auth_saml_acs")
- `src/portal/wiki/route/book/controller.py`: wiz.config("season") → wiz.model("portal/season/config")
- `src/portal/season/app/admin.config/api.py`: smtp_test()에서 수동 fallback 코드 제거, config.py 경유로 단순화

### FN-0027: 관리자 설정 UI 누락 항목 추가
- `src/portal/season/app/admin.config/view.ts`: site에 PWA 상세 설정 7개, auth에 SAML 상세 설정 7개 추가
- `src/portal/season/app/admin.config/view.pug`: PWA 상세 설정(토글 섹션), 인증 경로 설정, SAML 상세 설정 UI 추가

### FN-0028: season.py 정리
- `config/season.py`: 주석으로 DB 관리 안내 추가, 값 설정과 함수 영역 구분 정리
