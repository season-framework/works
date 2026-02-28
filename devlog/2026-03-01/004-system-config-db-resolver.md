# system_config DB 모델 및 SystemConfig Resolver 구현

- **ID**: 004
- **날짜**: 2026-03-01
- **유형**: 기능 추가

## 작업 요약
system_config 테이블 DB 모델과 SystemConfig Resolver 모델을 구현. DB 기반 설정 관리를 위한 캐시(TTL 60초) + Fallback 패턴, 타입 캐스팅(string/int/bool/json/password), password 마스킹 기능 제공.

## 변경 파일 목록

### dev 프로젝트
- `src/model/db/system_config.py`: system_config 테이블 DB 모델 정의 (신규)
- `portal/season/model/system_config.py`: SystemConfig Resolver (get/set/list/delete + 캐시 + 타입 변환) (신규)

### main 프로젝트
- 위 2개 파일 동일 적용
