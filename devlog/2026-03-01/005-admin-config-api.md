# 시스템 설정 API 구현 (page.admin/api.py)

- **ID**: 005
- **날짜**: 2026-03-01
- **유형**: 기능 추가

## 작업 요약
page.admin/api.py에 시스템 설정 관련 API 6개 함수 추가. config_load(카테고리별 설정 로드), config_update(배치 업데이트, password 마스킹 유지), smtp_test(테스트 이메일 발송), template_list/read/update(이메일 템플릿 CRUD). SystemConfig Resolver 활용 + 기존 config fallback.

## 변경 파일 목록

### dev/main 프로젝트 (동일)
- `src/app/page.admin/api.py`: 시스템 설정 API 6개 함수 추가 (config_load, config_update, smtp_test, template_list, template_read, template_update)
