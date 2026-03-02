# 로그인 페이지 인풋/버튼 UX 고도화 (Toss/Apple 스타일)

- **ID**: 021
- **날짜**: 2026-03-02
- **유형**: 기능 추가

## 작업 요약
로그인 페이지의 인풋과 버튼을 Toss/Apple 스타일로 전면 재설계. 평범한 border 인풋을 배경색 기반 미니멀 인풋으로 교체하고, 모호한 "계속" 버튼을 "이메일로 계속하기" + 화살표 아이콘 CTA로 변경. 전체 간격·위계·마이크로인터랙션 개선.

## 변경 파일 목록
### App - page.authenticate
- `view.pug`: 인풋에서 외부 label 제거(placeholder 방식), 버튼 텍스트 명확화("이메일로 계속하기", "이메일로 시작하기"), 이메일 피드백 pill UI, 인증코드 대형 인풋, 회원가입 폼 label-group 구조, 보조 링크 스타일 통일
- `view.scss`: Tailwind @apply 제거 → 순수 CSS로 인풋/버튼 스타일 재작성. cubic-bezier 트랜지션, focus 시 blue ring + shadow, hover 시 배경 변화, 버튼 hover 시 아이콘 슬라이드, divider CSS 방식, 약관 박스 커스텀 스크롤바
