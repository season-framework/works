import datetime

config = wiz.model("portal/works/config")
orm = wiz.model("portal/season/orm")
issuedb = orm.use("issueboard/issue", module="works")
viewdb = orm.use("issueboard/issue/view", module="works")

class Model:
    def __init__(self, issueboard):
        self.issueboard = issueboard
        self.project = issueboard.project
        self.project_id = issueboard.project.data['id']

    def get(self, issue_id):
        self.project.member.accessLevel(['admin', 'manager', 'user', 'guest'])

        issue = issuedb.get(id=issue_id, project_id=self.project_id)
        if issue is None:
            return None
        issue['worker'] = self.issueboard.worker.managers(issue_id)

        user_id = config.session_user_id()
        issue['role'] = self.issueboard.worker.role(issue_id, user_id)

        viewdb.upsert(dict(user_id=user_id, issue_id=issue_id, last_viewed=datetime.datetime.now()), keys="user_id,issue_id")
        return issue    

    def load(self, issue_id):
        self.project.member.accessLevel(['admin', 'manager', 'user', 'guest'])
        kwargs = dict(id=issue_id, project_id=self.project_id)
        kwargs['fields'] = "id,label_id,user_id,title,process,level,status,planstart,planend,updated,todo,worker"
        return issuedb.rows(**kwargs)

    def create(self, data):
        self.project.member.accessLevel(['admin', 'manager', 'user'])

        user_id = config.session_user_id()

        # create Issue
        data['created'] = datetime.datetime.now()
        data['updated'] = datetime.datetime.now()
        data['user_id'] = user_id
        data['project_id'] = self.project_id

        if 'status' not in data:
            data['status'] = 'open'
        issue_id = issuedb.insert(data)
        data = issuedb.get(id=issue_id)

        # update worker
        self.issueboard.worker.updateOwner(issue_id, [user_id])
        self.issueboard.worker.updateManager(issue_id, data['worker'])
        self.issueboard.message.log(issue_id, "작업이 생성되었습니다")

        self.project.updateTime()
        return data

    def updateLabel(self, issue_id, label_id):
        self.project.member.accessLevel(['admin', 'manager', 'user'])
        udata = dict(label_id=label_id)
        issuedb.update(udata, id=issue_id, project_id=self.project_id)
        self.project.updateTime()

    def updateTime(self, issue_id):
        self.project.member.accessLevel(['admin', 'manager', 'user'])
        data = dict()
        data['updated'] = datetime.datetime.now()
        issuedb.update(data, id=issue_id, project_id=self.project_id)

    def update(self, data):
        self.project.member.accessLevel(['admin', 'manager', 'user'])

        if 'id' not in data:
            return self.create(data)

        issue_id = data['id']
        issue = self.get(issue_id)
        if issue is None:
            raise Exception("Not Allowed")

        user_id = config.session_user_id()
        issue_auth = self.issueboard.worker.role(issue_id, user_id)
        if issue_auth not in ['owner', 'manager']:
            raise Exception("Not Allowed")

        data['process'] = int(data['process'])
        data['level'] = int(data['level'])
        try:
            issue['planstart'] = issue['planstart'].strftime("%Y-%m-%d")
        except (AttributeError, TypeError):
            pass
        try:
            issue['planend'] = issue['planend'].strftime("%Y-%m-%d")
        except (AttributeError, TypeError):
            pass

        if data['planstart'] == '': data['planstart'] = None
        if data['planend'] == '': data['planend'] = None

        # update Issue
        if issue_auth != 'owner':
            # del data['description']
            if data['status'] not in ['open', 'work', 'finish']:
                data['status'] = issue['status']

        del data['project_id']
        del data['user_id']
        del data['created']
        data['updated'] = datetime.datetime.now()

        # 변경 이력 추적 로그
        changes = []
        tracker = dict(title="제목", process="진행률", level="중요도", status="진행상태", planstart="시작일", planend="종료일")
        mapper = dict()
        mapper['status'] = dict(open="시작되지 않음", work="진행중", finish="완료됨", close="종료됨", cancel="취소")
        mapper['level'] = dict()
        mapper['level'][0] = '낮음'
        mapper['level'][1] = '중간'
        mapper['level'][2] = '중요'
        mapper['level'][3] = '긴급'
        
        for key in tracker:
            translate = tracker[key]
            if key not in data: continue
            if data[key] == issue[key]: continue
            before = issue[key] if issue[key] is not None else "지정안됨"
            after = data[key] if data[key] is not None else "지정안됨"
            if key in mapper:
                if before in mapper[key]: before = mapper[key][before]
                if after in mapper[key]: after = mapper[key][after]
            msg = f"'{translate}' 항목이 '{before}' 에서 '{after}' (으)로 변경되었습니다"
            self.issueboard.message.log(issue_id, msg)
            changes.append(translate)
        
        if data['todo'] != issue['todo']:
            msg = f"'TODO' 항목이 변경되었습니다"
            self.issueboard.message.log(issue_id, msg)
            changes.append("TODO")
        
        if 'description' in data:
            if data['description'] != issue['description']:
                msg = f"'설명' 항목이 변경되었습니다"
                self.issueboard.message.log(issue_id, msg)
                changes.append("설명")

        if 'worker' in data:
            if data['worker'] != issue['worker']:
                _workers = []
                for uid in data['worker']:
                    user = config.get_user_info(wiz, uid)
                    if user is not None:
                        _workers.append(user['name'])
                msg = "작업자가 변경되었습니다. 현재 작업자: 지정되지 않음"
                if len(_workers) > 0:
                    _workers = ", ".join(_workers)
                    msg = f"작업자가 변경되었습니다. 현재 작업자: {_workers}"
                self.issueboard.message.log(issue_id, msg)
                changes.append("작업자")

        issuedb.update(data, id=issue_id, project_id=self.project_id)
        data = issuedb.get(id=issue_id, project_id=self.project_id)
        self.issueboard.worker.updateManager(issue_id, data['worker'])
        
        self.issueboard.emit("issue", issue_id)

        self.project.updateTime()

        # Push 알림: 의미있는 변경이 있을 때 관련 사용자에게 발송
        if changes:
            try:
                Push = wiz.model("portal/works/struct/push")
                related_users = set()
                related_users.add(issue['user_id'])
                if data.get('worker'):
                    for w in data['worker']:
                        related_users.add(w)
                if issue.get('worker'):
                    for w in issue['worker']:
                        related_users.add(w)
                related_users.discard(user_id)
                related_users.discard('')

                if related_users:
                    project_title = self.project.data.get('title', '')
                    issue_title = data.get('title', issue.get('title', ''))
                    title = f"[{project_title}] {issue_title}"
                    body = ", ".join(changes) + " 항목이 변경되었습니다"
                    for uid in related_users:
                        try:
                            Push.send(uid, title, body, url="/notification")
                        except Exception:
                            pass
            except Exception:
                pass

        return data