import datetime

config = wiz.model("portal/works/config")
orm = wiz.model("portal/season/orm")
db = orm.use("calendar", module="works")
attendeedb = orm.use("calendar/attendee", module="works")
categorydb = orm.use("calendar/category", module="works")
attendeegroupdb = orm.use("calendar/attendee_group", module="works")
memberdb = orm.use("member", module="works")
userdb = orm.use("user")

class Model:
    def __init__(self, project):
        self.project = project
        self.project_id = project.data['id']
        self.cache = dict()
        self.cache['users'] = dict()

    def transformUser(self, user_id):
        if user_id in self.cache['users']:
            user = self.cache['users'][user_id]
        else:
            user = config.get_user_info(wiz, user_id)
            self.cache['users'][user_id] = user
        if user is None:
            user = dict()
        return user

    def formatDatetime(self, data, keys):
        for key in keys:
            if key in data and data[key] is not None:
                if hasattr(data[key], 'strftime'):
                    data[key] = data[key].strftime('%Y-%m-%d %H:%M:%S')
        return data

    # ── 카테고리 ──

    def getCategories(self):
        self.project.member.accessLevel(['admin', 'manager', 'user', 'guest'])
        rows = categorydb.rows(
            project_id=self.project_id,
            status='active',
            orderby='sort_order',
            order='ASC'
        )
        for i in range(len(rows)):
            rows[i] = self.formatDatetime(rows[i], ['created', 'updated'])
        return rows

    def createCategory(self, data):
        self.project.member.accessLevel(['admin', 'manager', 'user'])
        data['project_id'] = self.project_id
        data['status'] = 'active'
        data['created'] = datetime.datetime.now()
        data['updated'] = datetime.datetime.now()
        if 'sort_order' not in data:
            cnt = categorydb.count(project_id=self.project_id, status='active')
            data['sort_order'] = (cnt or 0) + 1
        insert_id = categorydb.insert(data)
        return categorydb.get(id=insert_id)

    def updateCategory(self, data):
        self.project.member.accessLevel(['admin', 'manager', 'user'])
        cat_id = data.get('id')
        if not cat_id:
            raise Exception("Category ID required")
        existing = categorydb.get(id=cat_id, project_id=self.project_id)
        if existing is None:
            raise Exception("Category not found")
        data['updated'] = datetime.datetime.now()
        if 'created' in data:
            del data['created']
        categorydb.update(data, id=cat_id)
        return categorydb.get(id=cat_id)

    def deleteCategory(self, category_id):
        self.project.member.accessLevel(['admin', 'manager', 'user'])
        existing = categorydb.get(id=category_id, project_id=self.project_id)
        if existing is None:
            raise Exception("Category not found")
        categorydb.update(dict(status='deleted', updated=datetime.datetime.now()), id=category_id)

    def reorderCategories(self, order_list):
        self.project.member.accessLevel(['admin', 'manager', 'user'])
        now = datetime.datetime.now()
        for item in order_list:
            cat_id = item.get('id')
            sort_order = item.get('sort_order')
            if not cat_id or sort_order is None:
                continue
            existing = categorydb.get(id=cat_id, project_id=self.project_id, status='active')
            if existing is None:
                continue
            categorydb.update(dict(sort_order=int(sort_order), updated=now), id=cat_id)

    # ── 개별 참가자 ──

    def getAttendees(self, event_id):
        rows = attendeedb.rows(event_id=event_id, project_id=self.project_id)
        for i in range(len(rows)):
            rows[i] = self.formatDatetime(rows[i], ['created'])
            rows[i]['user'] = self.transformUser(rows[i].get('user_id', ''))
        return rows

    def addAttendee(self, event_id, user_id):
        self.project.member.accessLevel(['admin', 'manager', 'user'])
        existing = db.get(id=event_id, project_id=self.project_id)
        if existing is None:
            raise Exception("Event not found")
        dup = attendeedb.get(event_id=event_id, user_id=user_id)
        if dup is not None:
            return dup
        data = dict()
        data['event_id'] = event_id
        data['user_id'] = user_id
        data['project_id'] = self.project_id
        data['status'] = 'accepted'
        data['created'] = datetime.datetime.now()
        insert_id = attendeedb.insert(data)
        return attendeedb.get(id=insert_id)

    def removeAttendee(self, event_id, user_id):
        self.project.member.accessLevel(['admin', 'manager', 'user'])
        attendeedb.delete(event_id=event_id, user_id=user_id, project_id=self.project_id)

    # ── 그룹 참가자 ──

    def addGroupAttendee(self, event_id, group_type, group_id=''):
        self.project.member.accessLevel(['admin', 'manager', 'user'])
        existing = db.get(id=event_id, project_id=self.project_id)
        if existing is None:
            raise Exception("Event not found")
        dup = attendeegroupdb.get(event_id=event_id, project_id=self.project_id, group_type=group_type, group_id=group_id)
        if dup is not None:
            return dup
        data = dict()
        data['event_id'] = event_id
        data['project_id'] = self.project_id
        data['group_type'] = group_type
        data['group_id'] = group_id
        data['created'] = datetime.datetime.now()
        insert_id = attendeegroupdb.insert(data)
        return attendeegroupdb.get(id=insert_id)

    def removeGroupAttendee(self, event_id, group_type, group_id=''):
        self.project.member.accessLevel(['admin', 'manager', 'user'])
        attendeegroupdb.delete(event_id=event_id, project_id=self.project_id, group_type=group_type, group_id=group_id)

    def getGroupAttendees(self, event_id):
        rows = attendeegroupdb.rows(event_id=event_id, project_id=self.project_id)
        for i in range(len(rows)):
            rows[i] = self.formatDatetime(rows[i], ['created'])
        return rows

    def resolveGroupMembers(self, group_type, group_id=''):
        """그룹 타입에 따라 실제 사용자 목록을 반환"""
        if group_type == 'project_all':
            members = memberdb.rows(project_id=self.project_id)
            user_ids = list(set([m['user'] for m in members]))
            result = []
            for uid in user_ids:
                user = self.transformUser(uid)
                result.append(dict(
                    user_id=uid,
                    user_name=user.get('name', '') if user else ''
                ))
            return result
        return []

    def _attachExtras(self, row):
        event_id = row.get('id', '')
        # 개별 참가자 목록
        att_rows = attendeedb.rows(event_id=event_id)
        attendees = []
        for a in att_rows:
            a = self.formatDatetime(a, ['created'])
            user = self.transformUser(a.get('user_id', ''))
            a['user'] = user
            a['user_name'] = user.get('name', '') if user else ''
            attendees.append(a)
        row['attendees'] = attendees

        # 그룹 참가자 목록
        group_rows = attendeegroupdb.rows(event_id=event_id, project_id=self.project_id)
        group_attendees = []
        for g in group_rows:
            g = self.formatDatetime(g, ['created'])
            group_attendees.append(g)
        row['group_attendees'] = group_attendees

        # 그룹을 resolve하여 전체 참가자 목록 생성
        resolved_ids = set([a.get('user_id', '') for a in att_rows])
        resolved_attendees = list(attendees)
        for g in group_rows:
            members = self.resolveGroupMembers(g.get('group_type', ''), g.get('group_id', ''))
            for m in members:
                if m['user_id'] not in resolved_ids:
                    resolved_ids.add(m['user_id'])
                    resolved_attendees.append(dict(
                        user_id=m['user_id'],
                        user_name=m['user_name'],
                        user=self.transformUser(m['user_id']),
                        from_group=g.get('group_type', '')
                    ))
        row['resolved_attendees'] = resolved_attendees

        # 카테고리 정보
        cat_id = row.get('category_id', '')
        if cat_id:
            cat = categorydb.get(id=cat_id, project_id=self.project_id)
            if cat:
                cat = self.formatDatetime(cat, ['created', 'updated'])
            row['category'] = cat
        else:
            row['category'] = None
        return row

    # ── 일정 CRUD ──

    def search(self, year, month):
        self.project.member.accessLevel(['admin', 'manager', 'user', 'guest'])

        project_id = self.project_id

        # 이전 달 1일부터 다음 달 말일까지 (캘린더 그리드에 겹치는 주 포함)
        if month == 1:
            start_date = f"{year - 1}-12-01 00:00:00"
        else:
            start_date = f"{year}-{month - 1:02d}-01 00:00:00"

        if month == 12:
            end_date = f"{year + 1}-02-01 00:00:00"
        elif month == 11:
            end_date = f"{year + 1}-01-01 00:00:00"
        else:
            end_date = f"{year}-{month + 2:02d}-01 00:00:00"

        rows = db.rows(
            project_id=project_id,
            status='active',
            end=lambda f: f >= start_date,
            start=lambda f: f < end_date,
            orderby='start',
            order='ASC'
        )

        for i in range(len(rows)):
            rows[i] = self.formatDatetime(rows[i], ['start', 'end', 'created', 'updated'])
            rows[i]['user'] = self.transformUser(rows[i].get('user_id', ''))
            rows[i] = self._attachExtras(rows[i])

        return rows

    def get(self, event_id):
        self.project.member.accessLevel(['admin', 'manager', 'user', 'guest'])

        data = db.get(id=event_id, project_id=self.project_id)
        if data is None:
            raise Exception("Event not found")
        data = self.formatDatetime(data, ['start', 'end', 'created', 'updated'])
        data['user'] = self.transformUser(data['user_id'])
        data = self._attachExtras(data)
        return data

    def create(self, data):
        self.project.member.accessLevel(['admin', 'manager', 'user'])

        attendees = []
        if 'attendees' in data:
            try:
                import json
                att = data['attendees']
                if isinstance(att, str):
                    att = json.loads(att)
                attendees = att if isinstance(att, list) else []
            except Exception:
                attendees = []
            del data['attendees']

        group_attendees = []
        if 'group_attendees' in data:
            try:
                import json
                ga = data['group_attendees']
                if isinstance(ga, str):
                    ga = json.loads(ga)
                group_attendees = ga if isinstance(ga, list) else []
            except Exception:
                group_attendees = []
            del data['group_attendees']

        data['project_id'] = self.project_id
        data['user_id'] = config.session_user_id()
        data['status'] = 'active'
        data['created'] = datetime.datetime.now()
        data['updated'] = datetime.datetime.now()

        if 'all_day' not in data:
            data['all_day'] = False
        else:
            data['all_day'] = data['all_day'] in [True, 'true', 'True', '1', 1]

        if 'category_id' not in data:
            data['category_id'] = ''

        insert_id = db.insert(data)

        # 개별 참가자 추가
        for uid in attendees:
            try:
                self.addAttendee(insert_id, uid)
            except Exception:
                pass

        # 그룹 참가자 추가
        for g in group_attendees:
            try:
                gt = g.get('group_type', '') if isinstance(g, dict) else str(g)
                gid = g.get('group_id', '') if isinstance(g, dict) else ''
                self.addGroupAttendee(insert_id, gt, gid)
            except Exception:
                pass

        self.project.updateTime()
        return self.get(insert_id)

    def update(self, data):
        self.project.member.accessLevel(['admin', 'manager', 'user'])

        event_id = data.get('id')
        if not event_id:
            raise Exception("Event ID required")

        existing = db.get(id=event_id, project_id=self.project_id)
        if existing is None:
            raise Exception("Event not found")

        attendees = None
        if 'attendees' in data:
            try:
                import json
                att = data['attendees']
                if isinstance(att, str):
                    att = json.loads(att)
                attendees = att if isinstance(att, list) else []
            except Exception:
                attendees = []
            del data['attendees']

        group_attendees = None
        if 'group_attendees' in data:
            try:
                import json
                ga = data['group_attendees']
                if isinstance(ga, str):
                    ga = json.loads(ga)
                group_attendees = ga if isinstance(ga, list) else []
            except Exception:
                group_attendees = []
            del data['group_attendees']

        data['project_id'] = self.project_id
        data['updated'] = datetime.datetime.now()

        if 'all_day' in data:
            data['all_day'] = data['all_day'] in [True, 'true', 'True', '1', 1]

        if 'created' in data:
            del data['created']
        if 'user' in data:
            del data['user']
        if 'category' in data:
            del data['category']
        if 'resolved_attendees' in data:
            del data['resolved_attendees']

        db.update(data, id=event_id)

        # 개별 참가자 동기화
        if attendees is not None:
            existing_att = attendeedb.rows(event_id=event_id, project_id=self.project_id)
            existing_uids = set([a['user_id'] for a in existing_att])
            new_uids = set(attendees)
            for uid in new_uids - existing_uids:
                try:
                    self.addAttendee(event_id, uid)
                except Exception:
                    pass
            for uid in existing_uids - new_uids:
                self.removeAttendee(event_id, uid)

        # 그룹 참가자 동기화
        if group_attendees is not None:
            existing_groups = attendeegroupdb.rows(event_id=event_id, project_id=self.project_id)
            existing_group_keys = set()
            for eg in existing_groups:
                key = (eg.get('group_type', ''), eg.get('group_id', ''))
                existing_group_keys.add(key)
            new_group_keys = set()
            for g in group_attendees:
                gt = g.get('group_type', '') if isinstance(g, dict) else str(g)
                gid = g.get('group_id', '') if isinstance(g, dict) else ''
                new_group_keys.add((gt, gid))
            for gt, gid in new_group_keys - existing_group_keys:
                try:
                    self.addGroupAttendee(event_id, gt, gid)
                except Exception:
                    pass
            for gt, gid in existing_group_keys - new_group_keys:
                self.removeGroupAttendee(event_id, gt, gid)

        self.project.updateTime()
        return self.get(event_id)

    def move(self, event_id, new_start, new_end):
        self.project.member.accessLevel(['admin', 'manager', 'user'])
        existing = db.get(id=event_id, project_id=self.project_id)
        if existing is None:
            raise Exception("Event not found")
        db.update(dict(start=new_start, end=new_end, updated=datetime.datetime.now()), id=event_id)
        self.project.updateTime()
        return self.get(event_id)

    def delete(self, event_id):
        self.project.member.accessLevel(['admin', 'manager', 'user'])

        existing = db.get(id=event_id, project_id=self.project_id)
        if existing is None:
            raise Exception("Event not found")

        db.update(dict(status='deleted', updated=datetime.datetime.now()), id=event_id)
        self.project.updateTime()
