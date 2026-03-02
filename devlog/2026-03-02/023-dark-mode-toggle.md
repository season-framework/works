# 다크모드/라이트모드 토글 기능 구현

- **ID**: 023
- **날짜**: 2026-03-02
- **유형**: 기능 추가

## 작업 요약
사이드바에 다크모드/라이트모드 전환 토글을 구현했다. CSS 변수 기반 테마 시스템을 구축하고, 전역 Tailwind 유틸리티 클래스 오버라이드를 통해 기존 컴포넌트들이 자동으로 다크 테마에 대응하도록 했다.

## 변경 파일 목록

### 신규 파일
- `portal/season/libs/theme.ts` — 테마 관리 서비스 (localStorage 저장, html data-theme 속성 관리)

### 수정된 패키지 파일
- `portal/season/libs/service.ts` — Theme 모듈 import 및 초기화 추가
- `portal/season/styles/content/color.scss` — `[data-theme="dark"]` 전체 셀렉터 추가: CSS 변수 다크 오버라이드, 배경/텍스트/테두리/호버/그림자/스크롤바/폼 입력/인증 페이지 스타일 전역 오버라이드

### 수정된 소스 파일
- `component.nav.aside/view.pug` — 다크모드 토글 버튼 추가 (프로젝트 이동 위), 로고 이미지 다크모드 분기 (logo-black↔logo-white)
- `layout.aside/view.pug` — 로딩 화면 배경에 bg-white 추가 (다크모드 대응)

### 수정된 프로젝트 설정
- `src/angular/tailwind.config.js` — `darkMode: 'class'` 추가
