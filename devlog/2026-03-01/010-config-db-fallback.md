# Config DB 통합 및 기존 설정 파일 Fallback 연결

- **ID**: 010
- **날짜**: 2026-03-01
- **유형**: 기능 추가

## 작업 요약
기존 config 파일 기반 설정 모델 3개(season, works, wiki)에 SystemConfig DB 오버라이드 레이어 적용. DB 값 존재 시 DB 우선, 미존재 시 파일 config 사용 (Zero-migration). 대상 설정: pwa_title, pwa_display, site_url, smtp_host/port/sender/password, auth_saml_use, works_path, wiki_path (총 10개).

## 변경 파일 목록

### dev/main 프로젝트 (동일)
- `portal/season/model/config.py`: SystemConfig 오버라이드 추가 (site 3개, smtp 4개, auth 1개 = 8개)
- `portal/works/model/config.py`: SystemConfig 오버라이드 추가 (storage.works_path → STORAGE_PATH)
- `portal/wiki/model/config.py`: SystemConfig 오버라이드 추가 (storage.wiki_path → STORAGE_PATH)
