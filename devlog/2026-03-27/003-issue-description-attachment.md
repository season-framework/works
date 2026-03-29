# 이슈 상세 페이지 본문(설명) 영역 파일 업로드 기능 구현

- **ID**: 003
- **날짜**: 2026-03-27
- **유형**: 기능 추가

## 작업 요약
이슈 상세 페이지의 본문(설명, description) 영역에 파일 첨부 기능을 추가했다. 기존에는 댓글(메시지) 영역에만 파일 업로드가 가능했으나, 이제 설명 영역 하단에서도 파일을 첨부하고 다운로드할 수 있다. 기존 `attachment` 인프라(route, project.attachment 메서드)를 재사용하여 구현했다.

## 변경 파일 목록

### DB Schema
- `src/portal/works/model/db/issueboard/issue.py`
  - `attachment = base.JSONArray()` 필드 추가
- DB 마이그레이션: `ALTER TABLE works_issueboard_issue ADD COLUMN attachment TEXT NULL DEFAULT NULL`

### Package App
- `src/portal/works/app/project.issueboard.issue/view.ts`
  - `load()`: 새 이슈 생성 시 `attachment: []` 초기화, 기존 이슈 로드 시 `attachment` 미존재 방어
  - `uploadDescription(filetype)`: 설명 영역 파일 업로드 메서드 추가
  - `removeDescAttachment(file)`: 설명 첨부파일 제거 메서드 추가
- `src/portal/works/app/project.issueboard.issue/view.pug`
  - 설명 CKEditor 하단에 첨부파일 목록 표시 (파일명 링크 + 삭제 버튼)
  - 업로드 진행률 표시
  - "파일 첨부" 버튼 추가
