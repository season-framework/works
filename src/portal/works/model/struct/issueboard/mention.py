import re
import datetime

config = wiz.model("portal/works/config")
orm = wiz.model("portal/season/orm")
mentiondb = orm.use("issueboard/mention", module="works")
memberdb = orm.use("member", module="works")

class Model:
    def __init__(self, issueboard):
        self.issueboard = issueboard
        self.project = issueboard.project
        self.project_id = issueboard.project.data['id']

    def _get_member_name_map(self):
        """프로젝트 멤버의 이름 → user_id 매핑 생성"""
        members = memberdb.rows(project_id=self.project_id)
        name_map = {}
        for m in members:
            user = config.get_user_info(wiz, m['user'])
            if user is not None:
                name_map[user['name']] = user['id']
        return name_map

    def parse_mentions(self, message_text):
        """메시지 텍스트에서 @이름 패턴을 파싱하여 멘션된 사용자 ID 목록 반환"""
        if not message_text:
            return []

        pattern = r'@(\S+)'
        matches = re.findall(pattern, message_text)
        if not matches:
            return []

        name_map = self._get_member_name_map()
        mentioned_ids = []
        for name in matches:
            if name in name_map:
                mentioned_ids.append(name_map[name])

        return list(set(mentioned_ids))

    def create_mentions(self, message_id, issue_id, user_id, message_text):
        """메시지에서 멘션을 파싱하고 DB에 저장"""
        mentioned_ids = self.parse_mentions(message_text)
        now = datetime.datetime.now()

        for mentioned_user_id in mentioned_ids:
            if mentioned_user_id == user_id:
                continue
            mentiondb.insert(dict(
                message_id=message_id,
                issue_id=issue_id,
                user_id=user_id,
                mentioned_user_id=mentioned_user_id,
                is_read=False,
                created=now
            ))

        return mentioned_ids

    def delete_by_message(self, message_id):
        """특정 메시지의 멘션 레코드 삭제"""
        mentiondb.delete(message_id=message_id)

    def update_mentions(self, message_id, issue_id, user_id, message_text):
        """메시지 수정 시 멘션 업데이트 (기존 삭제 후 재생성)"""
        self.delete_by_message(message_id)
        return self.create_mentions(message_id, issue_id, user_id, message_text)

    def mark_read(self, user_id, issue_id):
        """특정 이슈의 해당 사용자에 대한 멘션을 읽음 처리"""
        mentions = mentiondb.rows(mentioned_user_id=user_id, issue_id=issue_id, is_read=False)
        for m in mentions:
            mentiondb.update(dict(is_read=True), id=m['id'])

    def has_unread(self, user_id, issue_id):
        """해당 사용자에게 읽지 않은 멘션이 있는지 확인"""
        count = mentiondb.count(mentioned_user_id=user_id, issue_id=issue_id, is_read=False)
        return count > 0

    def unread_issue_ids(self, user_id):
        """읽지 않은 멘션이 있는 이슈 ID 목록 반환"""
        mentions = mentiondb.rows(mentioned_user_id=user_id, is_read=False, fields="issue_id")
        issue_ids = list(set([m['issue_id'] for m in mentions]))
        return issue_ids
