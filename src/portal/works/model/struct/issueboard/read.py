import datetime

config = wiz.model("portal/works/config")
orm = wiz.model("portal/season/orm")
readdb = orm.use("issueboard/issue/read", module="works")
messagedb = orm.use("issueboard/message", module="works")
mentiondb = orm.use("issueboard/mention", module="works")
issuedb = orm.use("issueboard/issue", module="works")
workerdb = orm.use("issueboard/worker", module="works")
memberdb = orm.use("member", module="works")

class Model:
    def __init__(self, issueboard):
        self.issueboard = issueboard
        self.project = issueboard.project
        self.project_id = issueboard.project.data['id']

    def _getLatestMessageId(self, issue_id):
        """이슈의 최신 메시지 ID 조회"""
        rows = messagedb.rows(issue_id=issue_id, order="DESC", orderby="id", page=1, dump=1, fields="id")
        if rows:
            return rows[0]['id']
        return 0

    def markRead(self, user_id, issue_id):
        """이슈 열람 시 읽음 처리"""
        latest_msg_id = self._getLatestMessageId(issue_id)
        now = datetime.datetime.now()

        readdb.upsert(dict(
            user_id=user_id,
            issue_id=issue_id,
            last_read_message_id=latest_msg_id,
            last_read_at=now,
            is_read=True
        ), keys="user_id,issue_id")

        # 해당 이슈의 멘션도 읽음 처리
        self.issueboard.mention.mark_read(user_id, issue_id)

    def markUnreadForOthers(self, issue_id, sender_user_id):
        """새 메시지 발생 시 발신자 제외 관련 사용자들의 읽음 상태를 안읽음으로 전환"""
        # 이슈의 관련 사용자: 요청자 + 작업자
        issue = issuedb.get(id=issue_id, project_id=self.project_id, fields="user_id,worker")
        if issue is None:
            return

        related_users = set()
        related_users.add(issue['user_id'])
        if issue.get('worker'):
            for w in issue['worker']:
                related_users.add(w)

        # 기존에 읽음 처리된 사용자들의 기록 조회
        existing_reads = readdb.rows(issue_id=issue_id)
        for r in existing_reads:
            related_users.add(r['user_id'])

        related_users.discard(sender_user_id)

        now = datetime.datetime.now()
        for uid in related_users:
            record = readdb.get(user_id=uid, issue_id=issue_id)
            if record is not None:
                readdb.update(dict(is_read=False), id=record['id'])
            else:
                readdb.upsert(dict(
                    user_id=uid,
                    issue_id=issue_id,
                    last_read_message_id=0,
                    last_read_at=now,
                    is_read=False
                ), keys="user_id,issue_id")

    def isUnread(self, user_id, issue_id):
        """개별 이슈 읽음 여부 확인"""
        record = readdb.get(user_id=user_id, issue_id=issue_id)
        if record is None:
            # 자신이 관련된 이슈인지 확인
            issue = issuedb.get(id=issue_id, fields="user_id,worker")
            if issue is None:
                return False
            is_related = (issue['user_id'] == user_id)
            if not is_related and issue.get('worker'):
                is_related = user_id in issue['worker']
            if not is_related:
                # 멘션 여부 확인
                is_related = self.issueboard.mention.has_unread(user_id, issue_id)
            if is_related:
                # 메시지가 있는 이슈면 안읽음
                msg_count = messagedb.count(issue_id=issue_id)
                return msg_count > 0
            return False

        if not record['is_read']:
            return True

        # 멘션 기반 안읽음 체크
        if self.issueboard.mention.has_unread(user_id, issue_id):
            return True

        # 마지막 읽은 메시지 이후 새 메시지가 있는지
        latest = self._getLatestMessageId(issue_id)
        if latest > record['last_read_message_id']:
            return True

        return False

    def getUnreadMap(self, user_id, issue_ids):
        """이슈 ID 리스트에 대한 읽음/안읽음 맵 반환"""
        if not issue_ids:
            return {}

        result = {}
        read_records = readdb.rows(user_id=user_id, issue_id=issue_ids)
        read_map = {r['issue_id']: r for r in read_records}

        # 멘션 안읽음 이슈 확인
        unread_mentions = mentiondb.rows(mentioned_user_id=user_id, issue_id=issue_ids, is_read=False, fields="issue_id")
        mention_unread_set = set(m['issue_id'] for m in unread_mentions)

        # 이슈별 최신 메시지 ID 일괄 조회
        issues_data = issuedb.rows(id=issue_ids, fields="id,user_id,worker")
        issue_map = {i['id']: i for i in issues_data}

        for issue_id in issue_ids:
            if issue_id in mention_unread_set:
                result[issue_id] = True
                continue

            record = read_map.get(issue_id)
            if record is not None:
                if not record['is_read']:
                    result[issue_id] = True
                else:
                    result[issue_id] = False
            else:
                # 레코드 없음 → 관련 사용자이고 메시지 있으면 안읽음
                issue = issue_map.get(issue_id)
                if issue:
                    is_related = (issue['user_id'] == user_id)
                    if not is_related and issue.get('worker'):
                        is_related = user_id in issue['worker']
                    if is_related:
                        result[issue_id] = True
                    else:
                        result[issue_id] = False
                else:
                    result[issue_id] = False

        return result

    def getUnreadIssues(self, user_id, project_ids=None, page=1, dump=20):
        """안읽은 이슈 목록 조회 (멘션 포함)"""
        # 1. is_read=False인 레코드
        kwargs = dict(user_id=user_id, is_read=False, order="DESC", orderby="last_read_at", fields="issue_id")
        unread_records = readdb.rows(**kwargs)
        unread_issue_ids = [r['issue_id'] for r in unread_records]

        # 2. 멘션 기반 안읽음 이슈
        mention_issue_ids = self.issueboard.mention.unread_issue_ids(user_id)

        # 합집합
        all_unread_ids = list(set(unread_issue_ids + mention_issue_ids))

        if not all_unread_ids:
            return {'items': [], 'total': 0}

        # 프로젝트 필터
        def query_fn(db, qs):
            qs = qs.where(db.id.in_(all_unread_ids))
            if project_ids:
                qs = qs.where(db.project_id.in_(project_ids))
            return qs

        issues = issuedb.rows(
            query=query_fn,
            order="DESC",
            orderby="updated",
            page=page,
            dump=dump,
            fields="id,project_id,title,status,level,user_id,worker,updated,planend"
        )

        total = issuedb.count(query=query_fn)

        return {'items': issues, 'total': total}

    def getAllUnreadIssues(self, user_id, project_ids=None, limit=10):
        """대시보드용: 안읽은 이슈 최신순 N건"""
        result = self.getUnreadIssues(user_id, project_ids=project_ids, page=1, dump=limit)
        return result
