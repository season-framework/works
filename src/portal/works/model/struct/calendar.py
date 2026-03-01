import datetime

config = wiz.model("portal/works/config")
orm = wiz.model("portal/season/orm")
db = orm.use("calendar", module="works")
attendeedb = orm.use("calendar/attendee", module="works")
categorydb = orm.use("calendar/category", module="works")

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

    # ── 참가자 ──

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

    def _attachExtras(self, row):
        event_id = row.get('id', '')
        # 참가자 목록
        att_rows = attendeedb.rows(event_id=event_id)
        attendees = []
        for a in att_rows:
            a = self.formatDatetime(a, ['created'])
            user = self.transformUser(a.get('user_id', ''))
            a['user'] = user
            a['user_name'] = user.get('name', '') if user else ''
            attendees.append(a)
        row['attendees'] = attendees
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

        start_date = f"{year}-{month:02d}-01 00:00:00"
        if month == 12:
            end_date = f"{year + 1}-01-01 00:00:00"
        else:
            end_date = f"{year}-{month + 1:02d}-01 00:00:00"

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
            except:
                attendees = []
            del data['attendees']

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

        # 참가자 추가
        for uid in attendees:
            try:
                self.addAttendee(insert_id, uid)
            except:
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
            except:
                attendees = []
            del data['attendees']

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

        db.update(data, id=event_id)

        # 참가자 동기화
        if attendees is not None:
            existing_att = attendeedb.rows(event_id=event_id, project_id=self.project_id)
            existing_uids = set([a['user_id'] for a in existing_att])
            new_uids = set(attendees)
            for uid in new_uids - existing_uids:
                try:
                    self.addAttendee(event_id, uid)
                except:
                    pass
            for uid in existing_uids - new_uids:
                self.removeAttendee(event_id, uid)

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

