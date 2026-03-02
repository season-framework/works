# 로그인 페이지 디자인 리뉴얼

- **ID**: 020
- **날짜**: 2026-03-02
- **유형**: 기능 추가

## 작업 요약
로그인 페이지(page.authenticate)를 기존 배경이미지+중앙카드 구조에서 모던한 Split 레이아웃으로 전면 리디자인. 좌측 브랜드 영역(다크 그라데이션 + 브랜드 메시지) + 우측 폼 영역으로 구성. 모바일에서는 폼만 전체 표시. view.ts/api.py 로직은 변경 없이 UI 템플릿과 스타일만 교체.

## 변경 파일 목록
### App - page.authenticate
- `view.pug`: Split 레이아웃 전면 재작성 — 좌우 분할, 브랜드 영역, 모던 인풋/버튼, SSO divider, 회원가입 플로우 전체 리디자인
- `view.scss`: 기존 .circle/.form 스타일 제거, .brand-gradient / .auth-input / .auth-btn-primary 새로 정의
