# 프로젝트 캘린더 기능 구현

- **ID**: 002
- **날짜**: 2026-03-02
- **유형**: 기능 추가

## 작업 요약
프로젝트에 캘린더(일정 관리) 기능을 추가. DB 모델, Struct, Portal App, 프론트엔드 UI, 사이드바 메뉴 통합, 활성화/비활성화 토글까지 전체 구현 완료.

## 변경 파일 목록

### DB 모델 (신규)
- `src/portal/works/model/db/calendar.py` — Peewee 캘린더 이벤트 테이블 (works_calendar). 12개 컬럼: id, project_id, user_id, title, description, start, end, all_day, color, status, created, updated

### Struct (신규)
- `src/portal/works/model/struct/calendar.py` — Calendar Sub-Struct. CRUD 메서드(search/get/create/update/delete), 월별 범위 쿼리, 접근 권한 체크, soft delete

### Aggregate Root (수정)
- `src/portal/works/model/project.py` — Calendar Sub-Struct import 및 `self.calendar` 등록

### Portal App (신규)
- `src/portal/works/app/project.calendar/app.json` — 앱 메타데이터 (mode: portal, controller: base, category: project)
- `src/portal/works/app/project.calendar/api.py` — 5개 API 함수 (search, read, create, update, delete)
- `src/portal/works/app/project.calendar/view.ts` — 캘린더 UI 로직 (월별 그리드, 이벤트 CRUD, 모달, 색상 선택)
- `src/portal/works/app/project.calendar/view.pug` — 캘린더 UI 템플릿 (월 네비게이션, 7열 그리드, 이벤트 바, 생성/편집 모달)
- `src/portal/works/app/project.calendar/view.scss` — 호스트 디스플레이 설정

### 메뉴 통합 (수정)
- `src/portal/works/libs/project.ts` — `extra.menu` 기본값에 `calendar: true` 추가 + null 체크
- `src/app/component.nav.aside/view.pug` — 사이드바에 캘린더 메뉴 링크 추가 (구성원 아래, 회의록 위)
- `src/app/page.project.item/view.pug` — `MENU == 'calendar'` 라우팅 분기 추가
- `src/portal/works/app/project.info/view.pug` — 캘린더 활성화/비활성화 토글 및 메인메뉴 옵션 추가
