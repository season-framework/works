import datetime

config = wiz.model("portal/works/config")
orm = wiz.model("portal/season/orm")
messagedb = orm.use("issueboard/message", module="works")
issuedb = orm.use("issueboard/issue", module="works")

class Model:
    def __init__(self, issueboard):
        self.issueboard = issueboard
        self.project = issueboard.project
        self.project_id = issueboard.project.data['id']

    def _send_push_to_related(self, issue_id, sender_user_id, message_text):
        """이슈 관련 사용자에게 push 알림 발송 (발신자 제외)"""
        try:
            Push = wiz.model("portal/works/struct/push")
            issue = issuedb.get(id=issue_id, project_id=self.project_id, fields="user_id,worker,title")
            if issue is None:
                return

            related_users = set()
            related_users.add(issue['user_id'])
            if issue.get('worker'):
                for w in issue['worker']:
                    related_users.add(w)
            related_users.discard(sender_user_id)
            related_users.discard('')

            if not related_users:
                return

            project_title = self.project.data.get('title', '')
            issue_title = issue.get('title', '')
            title = f"[{project_title}] {issue_title}"
            body = message_text[:100] if message_text else "새 메시지가 있습니다"

            for uid in related_users:
                try:
                    Push.send(uid, title, body, url="/notification")
                except Exception:
                    pass
        except Exception:
            pass

    def create(self, data):
        self.project.member.accessLevel(['admin', 'manager', 'user'])

        user_id = config.session_user_id()
        issue_id = data['issue_id']
        data['user_id'] = user_id
        data['updated'] = datetime.datetime.now()
        data['created'] = datetime.datetime.now()
        data['favorite'] = 0
        message_id = messagedb.insert(data)

        # 멘션 처리: message 타입이 log가 아닌 경우에만
        if data.get('type', '') != 'log' and data.get('message', ''):
            self.issueboard.mention.create_mentions(message_id, issue_id, user_id, data['message'])

        # 새 메시지 → 관련 사용자 읽음 상태 갱신 (안읽음으로 전환)
        self.issueboard.read.markUnreadForOthers(issue_id, user_id)

        self.project.issueboard.issue.updateTime(issue_id)

        parent_id = 0
        if 'parent_id' in data:
            parent_id = data['parent_id']

        self.issueboard.emit("message", {"issue_id": issue_id, "message_id": str(message_id), "parent_id": str(parent_id)})
        self.project.updateTime()

        # Push 알림 발송 (log 타입 제외)
        if data.get('type', '') != 'log':
            self._send_push_to_related(issue_id, user_id, data.get('message', ''))

    def updateFavorite(self, message_id, favorite):
        self.project.member.accessLevel(['admin', 'manager', 'user'])
        messagedb.update(dict(favorite=favorite), id=message_id)

    def update(self, data):
        self.project.member.accessLevel(['admin', 'manager', 'user'])

        if 'id' not in data:
            return self.create(data)
        message_id = data['id']
        user_id = config.session_user_id()
        if 'id' in data: del data['id']
        if 'type' in data: del data['type']
        if 'issue_id' in data: del data['issue_id']
        if 'user_id' in data: del data['user_id']
        if 'created' in data: del data['created']
        data['updated'] = datetime.datetime.now()
        messagedb.update(data, id=message_id, user_id=user_id)
        
        msg = messagedb.get(id=message_id)
        if msg is not None:
            issue_id = msg['issue_id']
            # 멘션 업데이트
            if msg.get('type', '') != 'log' and data.get('message', ''):
                self.issueboard.mention.update_mentions(message_id, issue_id, user_id, data['message'])
            self.project.issueboard.issue.updateTime(issue_id)

        self.project.updateTime()

    def remove(self, message_id):
        self.project.member.accessLevel(['admin', 'manager', 'user'])

        user_id = config.session_user_id()
        messagedb.delete(id=message_id, user_id=user_id)
        self.project.updateTime()

    def log(self, issue_id, message):
        self.project.member.accessLevel(['admin', 'manager', 'user'])
        data = dict(issue_id=issue_id, message=message, attachment=[], type="log")
        self.create(data)

    def get(self, message_id):
        self.project.member.accessLevel(['admin', 'manager', 'user', 'guest'])
        item = messagedb.get(id=message_id)
        if item is None:
            return None
        if self.project.issueboard.issue.get(item['issue_id']) is None:
            return None
        item['reply'] = messagedb.rows(parent_id=item['id'], order="ASC", orderby="id")
        return item

    def list(self, issue_id, type="log", first=None, favorite=None):
        self.project.member.accessLevel(['admin', 'manager', 'user', 'guest'])

        def query(db, qs):
            nullcheck = (db.parent_id.is_null(True) | (db.parent_id == 0))
            qs = qs.where(nullcheck)
            return qs

        kwargs = dict(
            query=query,
            issue_id=issue_id, 
            type=type, 
            order="DESC", 
            orderby="id"
        )

        if favorite is not None:
            kwargs['favorite'] = 1

        if first is not None:
            def idOperator(field):
                return field < first
            kwargs['id'] = idOperator

        rows = messagedb.rows(page=1, dump=10, **kwargs)

        # Batch fetch replies to avoid N+1 queries
        parent_ids = [rows[i]['id'] for i in range(len(rows))]
        if parent_ids:
            all_replies = messagedb.rows(parent_id=parent_ids, issue_id=issue_id, order="ASC", orderby="id")
            reply_map = {}
            for reply in all_replies:
                pid = reply['parent_id']
                if pid not in reply_map:
                    reply_map[pid] = []
                reply_map[pid].append(reply)
        else:
            reply_map = {}

        for i in range(len(rows)):
            rows[i]['reply'] = reply_map.get(rows[i]['id'], [])

        return rows
    
    def unread(self, issue_id, type="log", last=None, favorite=None):
        self.project.member.accessLevel(['admin', 'manager', 'user', 'guest'])

        def query(db, qs):
            nullcheck = (db.parent_id.is_null(True) | (db.parent_id == 0))
            qs = qs.where(nullcheck)
            return qs

        kwargs = dict(
            query=query,
            issue_id=issue_id, 
            type=type, 
            order="ASC", 
            orderby="id"
        )

        if favorite is not None:
            kwargs['favorite'] = 1

        if last is not None:
            def idOperator(field):
                return field > last
            kwargs['id'] = idOperator

        rows = messagedb.rows(**kwargs)

        # Batch fetch replies to avoid N+1 queries
        parent_ids = [rows[i]['id'] for i in range(len(rows))]
        if parent_ids:
            all_replies = messagedb.rows(parent_id=parent_ids, issue_id=issue_id, order="ASC", orderby="id")
            reply_map = {}
            for reply in all_replies:
                pid = reply['parent_id']
                if pid not in reply_map:
                    reply_map[pid] = []
                reply_map[pid].append(reply)
        else:
            reply_map = {}

        for i in range(len(rows)):
            rows[i]['reply'] = reply_map.get(rows[i]['id'], [])

        return rows