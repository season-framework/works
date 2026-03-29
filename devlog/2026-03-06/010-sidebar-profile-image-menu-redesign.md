# 사이드바 프로필 이미지 표시 + 메뉴 레이아웃 재설계

- **ID**: 010
- **날짜**: 2026-03-06
- **유형**: 기능 추가

## 작업 요약
사이드바 프로필 영역에서 사용자가 설정한 프로필 이미지를 원형으로 표시하도록 개선. 세션 쿠키 크기 제한으로 인해 별도 API 엔드포인트를 추가하여 DB에서 프로필 이미지를 로드. 하단 메뉴 버튼을 2×2 pill 카드에서 단일 행 아이콘 바 형태로 재설계.

## 변경 파일 목록

### API (component.nav.aside/api.py)
- `profile_image()` 함수 추가: DB에서 사용자의 `profile_image` (base64 data URL) 조회 후 반환

### TypeScript (component.nav.aside/view.ts)
- `profileImage: string` 프로퍼티 추가
- `loadProfileImage()` 메서드 추가: `wiz.call('profile_image')`로 이미지 로드
- `ngOnInit()`에서 `loadProfileImage()` 호출

### Template (component.nav.aside/view.pug)
- 프로필 영역: `profileImage`가 있으면 `background-image`로 원형 이미지 표시, 없으면 이름 첫 글자를 블루 그라디언트 원에 표시
- 메뉴 버튼: 2×2 pill 카드 → 단일 행 아이콘 바 (알림, 관리자, 로그아웃) 형태로 재설계
- `routerLinkActive="nav-action-active"` 활용하여 현재 페이지 하이라이트
