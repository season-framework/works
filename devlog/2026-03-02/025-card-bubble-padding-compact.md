# 카드/버블 여백 콤팩트화 — 프로젝트 목록, 위키 목록, 위키 탭, 메시지 버블

- **ID**: 025
- **날짜**: 2026-03-02
- **유형**: UI 개선

## 작업 요약
이슈보드를 제외한 전체 카드/버블 형태 디자인에서 과도한 padding을 콤팩트하게 축소. 프로젝트 목록, 위키 목록, 프로젝트 내 위키 탭, 이슈 세부 메시지 버블 등 5개 파일의 12건 여백을 일괄 조정.

## 변경 파일 목록

### 프로젝트 목록 (`src/app/page.explore.project/view.pug`)
- 카드 리스트 아이템: `p-5` → `px-4 py-3`
- 로딩 스켈레톤: `p-6` → `px-4 py-3` (실제 카드와 통일)

### 위키 목록 (`src/app/page.explore.wiki/view.pug`)
- 카드 리스트 아이템: `p-5` → `px-4 py-3`
- 로딩 스켈레톤: `p-6` → `px-4 py-3` (실제 카드와 통일)

### 프로젝트 내 위키 탭 (`src/portal/works/app/project.wiki/view.pug`)
- 외부 컨테이너: `py-6 px-4` → `py-4 px-4` (이중 패딩 해소)
- 내부 래퍼: `p-4` → `px-2` (이중 패딩 해소)
- 위키 카드: `p-5` → `px-4 py-3`, 아이콘 `size-14` → `size-12`, 간격 `ml-5` → `ml-4`
- 모달 카드: `p-5` → `px-4 py-3`, 아이콘/간격 동일 조정
- 로딩 스켈레톤: `p-6` → `px-4 py-3`
- 카드 간 간격: `gap-y-4` → `gap-y-3`

### 메시지 버블 (`src/portal/works/widget/message.body/view.pug`)
- 메시지 버블: `p-5` → `px-4 py-2.5`
- 답글 버블: `py-2 pl-9` → `py-1.5 pl-9 px-4`
- 첨부파일 영역: `mb-[6px]` → `mb-[4px]`

### 이슈 세부 페이지 (`src/portal/works/app/project.issueboard.issue/view.pug`)
- 작업정보 콘텐츠: `p-5` → `px-4 py-3`, `pb-5` → `pb-4`
- 메시지 목록 래핑: `p-4` → `px-3 py-3`
