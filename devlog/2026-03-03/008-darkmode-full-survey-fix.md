# 다크모드 전수 점검 및 잔여 이슈 수정

- **ID**: 008
- **날짜**: 2026-03-03
- **유형**: 기능 추가

## 작업 요약
FN-0004~0007 적용 후 전체 다크모드 UI 전수 점검 수행. 미커버 컬러 유틸리티 클래스 전수 검색 결과, 추가로 yellow(warning/star), green-100, amber-100, indigo(member avatar), violet(admin badge), sky(employee badge) 계열의 배경·텍스트·ring 오버라이드가 필요함을 확인하고 color.scss에 약 30줄 추가. 이슈 상세(issueboard.issue)와 이슈모음(page.issues)의 글로벌 fix 적용도 확인 완료.

## 변경 파일 목록

### 스타일
- `src/portal/season/styles/content/color.scss`: 추가 컬러 오버라이드 블록 (~30줄)
  - Yellow: bg-yellow-100/500/600, text-yellow-500/600/700, hover:bg-yellow-500
  - Green-100, Amber-100: 추가 밝은 배경 오버라이드
  - Indigo: bg-indigo-100, text-indigo-600
  - Violet: bg-violet-50, text-violet-600, ring-violet-200
  - Sky: bg-sky-50, text-sky-400/600, ring-sky-200
  - text-green-500 추가
