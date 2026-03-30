import datetime

Dashboard = wiz.model("portal/works/struct/dashboard")
MyCalendar = wiz.model("portal/works/struct/my_calendar")
Notification = wiz.model("portal/works/struct/notification")
config = wiz.model("portal/works/config")
orm = wiz.model("portal/season/orm")
projectdb = orm.use("project", module="works")
calendardb = orm.use("calendar", module="works")
attendeedb = orm.use("calendar/attendee", module="works")
attendeegroupdb = orm.use("calendar/attendee_group", module="works")
memberdb = orm.use("member", module="works")

def load():
    data = Dashboard.load(meeting_limit=10)
    wiz.response.status(200, **data)

def my_calendar():
    user_id = wiz.session.get("id")
    year = int(wiz.request.query("year", 2026))
    month = int(wiz.request.query("month", 1))
    try:
        events = MyCalendar.searchMyEvents(user_id, year, month)
    except Exception as e:
        wiz.response.status(500, message=str(e))
    wiz.response.status(200, events=events)

def _enrich_projects(items):
    project_ids = set()
    for item in items:
        if item.get('project_id') and not item.get('project'):
            project_ids.add(item['project_id'])
    projects = {}
    for pid in project_ids:
        try:
            p = projectdb.get(id=pid, fields="id,namespace,title")
            if p:
                projects[pid] = p
        except Exception:
            pass
    for item in items:
        pid = item.get('project_id', '')
        if pid and pid in projects and not item.get('project'):
            item['project'] = projects[pid]

def _calendar_to_notification(event):
    now = datetime.datetime.now()
    is_past = False
    try:
        end_str = str(event.get('end') or event.get('start') or '')
        if end_str:
            end_dt = datetime.datetime.strptime(end_str[:19], '%Y-%m-%d %H:%M:%S')
            is_past = now > end_dt
    except Exception:
        pass
    return {
        'id': 'cal_' + event['id'],
        'type': 'calendar_invited',
        'ref_type': 'calendar',
        'ref_id': event['id'],
        'project_id': event.get('project_id', ''),
        'user_id': event.get('user_id', ''),
        'title': event.get('title', ''),
        'message': '',
        'is_read': is_past,
        'created': str(event.get('created', '')),
        'start': str(event.get('start', '')),
        'end': str(event.get('end', '')),
        'all_day': event.get('all_day', False),
    }

def _calendar_events_for_user(user_id, limit=200):
    now = datetime.datetime.now()
    cutoff = now - datetime.timedelta(days=30)

    event_ids = set()

    try:
        attendees = attendeedb.rows(user_id=user_id, fields="event_id")
        for a in attendees:
            event_ids.add(a['event_id'])
    except Exception:
        pass

    try:
        members = memberdb.rows(user=user_id, fields="project_id")
        for m in members:
            try:
                groups = attendeegroupdb.rows(project_id=m['project_id'], group_type='project_all', fields="event_id")
                for g in groups:
                    event_ids.add(g['event_id'])
            except Exception:
                pass
    except Exception:
        pass

    items = []
    event_id_list = sorted(event_ids)[:100]
    for eid in event_id_list:
        try:
            event = calendardb.get(id=eid)
            if not event or event.get('status') != 'active':
                continue
            start_str = str(event.get('start') or '')
            if start_str:
                try:
                    start_dt = datetime.datetime.strptime(start_str[:19], '%Y-%m-%d %H:%M:%S')
                    if start_dt < cutoff:
                        continue
                except Exception:
                    pass
            items.append(_calendar_to_notification(event))
        except Exception:
            continue

    items.sort(key=lambda x: str(x.get('created', '')), reverse=True)
    return items[:limit]

def notifications():
    dump = int(wiz.request.query("dump", 10))
    user_id = config.session_user_id()
    items = []
    existing_cal_ref_ids = set()

    try:
        result = Dashboard.unread_issues(limit=50, page=1)
        for item in result.get('items', []):
            items.append({
                'id': 'issue_' + item['id'],
                'type': 'issue_mentioned' if item.get('is_mentioned') else 'issue_assigned',
                'ref_type': 'issue',
                'ref_id': item['id'],
                'project_id': item.get('project_id', ''),
                'title': item.get('title', ''),
                'message': item.get('project', {}).get('title', ''),
                'is_read': False,
                'created': str(item.get('updated', '')),
                'status': item.get('status', ''),
                'project': item.get('project', {}),
                'planend': item.get('planend', ''),
                'is_mentioned': item.get('is_mentioned', False),
            })
    except Exception:
        pass

    try:
        notif_result = Notification.list(user_id, page=1, limit=50, is_read=False)
        notif_items = notif_result.get('items', [])
        for item in notif_items:
            items.append(item)
            if item.get('ref_type') == 'calendar' and item.get('ref_id'):
                existing_cal_ref_ids.add(item['ref_id'])
    except Exception:
        pass

    try:
        cal_events = _calendar_events_for_user(user_id)
        for ev in cal_events:
            if ev['ref_id'] not in existing_cal_ref_ids and not ev.get('is_read'):
                items.append(ev)
    except Exception:
        pass

    _enrich_projects(items)
    items.sort(key=lambda x: str(x.get('created', '')), reverse=True)
    total = len(items)
    items = items[:dump]

    wiz.response.status(200, items=items, total=total)

def unread_issues():
    page = int(wiz.request.query("page", 1))
    dump = int(wiz.request.query("dump", 20))
    try:
        result = Dashboard.unread_issues(limit=dump, page=page)
    except Exception as e:
        wiz.response.status(500, message=str(e))
    wiz.response.status(200, **result)

def all_issues():
    page = int(wiz.request.query("page", 1))
    dump = int(wiz.request.query("dump", 20))
    try:
        result = Dashboard.all_related_issues(limit=dump, page=page)
    except Exception as e:
        wiz.response.status(500, message=str(e))
    wiz.response.status(200, **result)

def mentioned_issues():
    page = int(wiz.request.query("page", 1))
    dump = int(wiz.request.query("dump", 20))
    try:
        result = Dashboard.mentioned_issues(limit=dump, page=page)
    except Exception as e:
        wiz.response.status(500, message=str(e))
    wiz.response.status(200, **result)
