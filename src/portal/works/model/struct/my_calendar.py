import datetime

config = wiz.model("portal/works/config")
orm = wiz.model("portal/season/orm")
calendardb = orm.use("calendar", module="works")
attendeedb = orm.use("calendar/attendee", module="works")
categorydb = orm.use("calendar/category", module="works")
memberdb = orm.use("member", module="works")
projectdb = orm.use("project", module="works")

class MyCalendar:
    def __init__(self):
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

    def myProjects(self, user_id):
        """내가 참여한 프로젝트 + 각 프로젝트 카테고리 목록"""
        memberships = memberdb.rows(user=user_id)
        project_ids = [m['project_id'] for m in memberships]
        
        results = []
        for pid in project_ids:
            proj = projectdb.get(id=pid)
            if proj is None:
                continue
            if proj.get('status') == 'deleted':
                continue
            cats = categorydb.rows(
                project_id=pid,
                status='active',
                orderby='sort_order',
                order='ASC'
            )
            for c in cats:
                c = self.formatDatetime(c, ['created', 'updated'])
            results.append(dict(
                id=proj['id'],
                title=proj.get('title', ''),
                namespace=proj.get('namespace', ''),
                status=proj.get('status', ''),
                categories=cats
            ))
        return results

    def searchMyEvents(self, user_id, year, month):
        """내가 작성자이거나 참가자인 일정 전체 조회 (cross-project)"""
        start_date = f"{year}-{month:02d}-01 00:00:00"
        if month == 12:
            end_date = f"{year + 1}-01-01 00:00:00"
        else:
            end_date = f"{year}-{month + 1:02d}-01 00:00:00"

        # 1) 내가 작성자인 일정
        own_rows = calendardb.rows(
            user_id=user_id,
            status='active',
            end=lambda f: f >= start_date,
            start=lambda f: f < end_date,
            orderby='start',
            order='ASC'
        )

        # 2) 내가 참가자인 일정 (event_id 수집)
        att_rows = attendeedb.rows(user_id=user_id)
        att_event_ids = set([a['event_id'] for a in att_rows])

        # 참가자 일정 중 해당 월 범위 조회
        att_events = []
        for eid in att_event_ids:
            ev = calendardb.get(id=eid)
            if ev is None:
                continue
            if ev.get('status') != 'active':
                continue
            if hasattr(ev.get('end'), 'strftime'):
                ev_end = ev['end'].strftime('%Y-%m-%d %H:%M:%S')
                ev_start = ev['start'].strftime('%Y-%m-%d %H:%M:%S')
            else:
                ev_end = str(ev.get('end', ''))
                ev_start = str(ev.get('start', ''))
            if ev_end >= start_date and ev_start < end_date:
                att_events.append(ev)

        # 합치기 (중복 제거)
        seen = set()
        merged = []
        for row in own_rows + att_events:
            rid = row.get('id', '')
            if rid in seen:
                continue
            seen.add(rid)
            row = self.formatDatetime(row, ['start', 'end', 'created', 'updated'])
            row['user'] = self.transformUser(row.get('user_id', ''))
            # 카테고리 정보
            cat_id = row.get('category_id', '')
            if cat_id:
                cat = categorydb.get(id=cat_id)
                if cat:
                    cat = self.formatDatetime(cat, ['created', 'updated'])
                row['category'] = cat
            else:
                row['category'] = None
            # 프로젝트 정보
            pid = row.get('project_id', '')
            proj = projectdb.get(id=pid)
            row['project_title'] = proj.get('title', '') if proj else ''
            row['project_namespace'] = proj.get('namespace', '') if proj else ''
            # 참가자 정보
            att_list = attendeedb.rows(event_id=rid)
            attendees = []
            for a in att_list:
                u = self.transformUser(a.get('user_id', ''))
                attendees.append(dict(
                    user_id=a.get('user_id', ''),
                    user_name=u.get('name', '') if u else ''
                ))
            row['attendees'] = attendees
            merged.append(row)

        merged.sort(key=lambda x: x.get('start', ''))
        return merged

Model = MyCalendar()
