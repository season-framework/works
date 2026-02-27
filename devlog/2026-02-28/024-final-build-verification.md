# 전체 빌드 및 디자인 통합 검증

- **ID**: 024
- **날짜**: 2026-02-28
- **유형**: 설정 변경

## 작업 요약
전 20개 디자인 개편 작업(FN-0032~0050) 완료 후 최종 통합 검증 수행. 잔여 gray-*/fa-* 사용 전수 조사하여 works 위젯 2개(message.body, widget.project.issueboard.issue) 추가 정리. 클린 빌드(clean: true) 최종 확인.

## 변경 파일 목록

### portal/works/widget/message.body/view.pug (추가 정리)
- `fa-solid.fa-reply` → `ti.ti-arrow-back-up`, `fa-solid.fa-reply.rotate-180` → `ti.ti-arrow-forward-up`
- `fa-regular.fa-star` / `fa-solid.fa-star` → `ti.ti-star` / `ti.ti-star-filled`
- `fa-solid.fa-download` → `ti.ti-download`
- `text-gray-500` → `text-neutral-400`, `bg-gray-700` → `bg-neutral-100 text-neutral-600`
- `bg-slate-100` → `bg-neutral-100`

### portal/works/widget/widget.project.issueboard.issue/view.pug (추가 정리)
- `border-gray-300` → `border-neutral-200`, `hover:shadow-md` 제거
- `bg-gray-300 rounded-full` 스켈레톤 → `bg-neutral-200 rounded-md animate-pulse`
- FA 아이콘 모두 Tabler 교체: `fa-tag`→`ti-tag`, `fa-exclamation-circle`→`ti-alert-circle`, `fa-bullhorn`→`ti-speakerphone`, `fa-square-check`→`ti-square-check`, `fa-hourglass-end`→`ti-hourglass`
- `text-gray-500` → `text-neutral-500`/`text-neutral-400`

## 검증 결과
- `src/app/` 전체: gray-* 0건, fa-* 0건
- `src/portal/works/` 전체: gray-* 0건, fa-* 0건
- `src/portal/wiki/` 전체: gray-* 0건, fa-* 0건
- 클린 빌드: 성공 (EsBuild 834ms)
