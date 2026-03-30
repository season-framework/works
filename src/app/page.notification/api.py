import datetime

Dashboard = wiz.model("portal/works/struct/dashboard")
Notification = wiz.model("portal/works/struct/notification")
config = wiz.model("portal/works/config")
orm = wiz.model("portal/season/orm")
readdb = orm.use("issueboard/issue/read", module="works")
mentiondb = orm.use("issueboard/mention", module="works")
projectdb = orm.use("project", module="works")
notificationdb = orm.use("notification", module="works")
calendardb = orm.use("calendar", module="works")
attendeedb = orm.use("calendar/attendee", module="works")
attendeegroupdb = orm.use("calendar/attendee_group", module="works")
memberdb = orm.use("member", module="works")
issuedb = orm.use("issueboard/issue", module="works")

def _enrich_items(items):
    user_ids = set()
    for item in items:
        if item.get('user_id'):
            user_ids.add(item['user_id'])
    users = {}
    for uid in user_ids:
        info = config.get_user_info(wiz, uid)
        if info:
            users[uid] = info
    return users

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

def _issue_to_notification(item):
    return {
        'id': 'issue_' + item['id'],
        'issue_id': item['id'],
        'type': 'issue_mentioned' if item.get('is_mentioned') else 'issue_assigned',
        'ref_type': 'issue',
        'ref_id': item['id'],
        'project_id': item.get('project_id', ''),
        'user_id': item.get('user_id', ''),
        'title': item.get('title', ''),
        'message': item.get('project', {}).get('title', ''),
        'is_read': item.get('is_read', False),
        'created': str(item.get('updated', '')),
        'status': item.get('status', ''),
        'project': item.get('project', {}),
        'planend': item.get('planend', ''),
        'is_mentioned': item.get('is_mentioned', False),
    }

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

    # Direct attendee
    try:
        attendees = attendeedb.rows(user_id=user_id, fields="event_id")
        for a in attendees:
            event_ids.add(a['event_id'])
    except Exception:
        pass

    # Group attendee (project_all)
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

def list():
    user_id = config.session_user_id()
    page = int(wiz.request.query("page", 1))
    dump = int(wiz.request.query("dump", 20))
    ref_type = wiz.request.query("ref_type", "")
    is_read_str = wiz.request.query("is_read", "")

    is_read = None
    if is_read_str == "true":
        is_read = True
    elif is_read_str == "false":
        is_read = False

    if ref_type == "issue":
        try:
            result = Dashboard.all_related_issues(limit=dump, page=page)
        except Exception as e:
            wiz.response.status(500, message=str(e))
        items = []
        for item in result.get('items', []):
            nitem = _issue_to_notification(item)
            if is_read is not None and nitem['is_read'] != is_read:
                continue
            items.append(nitem)
        total = result.get('total', 0)
        users = _enrich_items(result.get('items', []))
        wiz.response.status(200, items=items, total=total, users=users)

    elif ref_type == "calendar":
        try:
            result = Notification.list(user_id, page=1, limit=200, is_read=is_read, ref_type='calendar')
        except Exception as e:
            wiz.response.status(500, message=str(e))

        notif_items = result.get('items', [])
        existing_ref_ids = set()
        for item in notif_items:
            if item.get('ref_id'):
                existing_ref_ids.add(item['ref_id'])

        cal_events = _calendar_events_for_user(user_id)
        for ev in cal_events:
            if ev['ref_id'] not in existing_ref_ids:
                if is_read is not None and ev['is_read'] != is_read:
                    continue
                notif_items.append(ev)

        _enrich_projects(notif_items)
        notif_items.sort(key=lambda x: str(x.get('created', '')), reverse=True)
        total = len(notif_items)
        start = (page - 1) * dump
        end = start + dump
        items = notif_items[start:end]
        users = _enrich_items(notif_items)
        wiz.response.status(200, items=items, total=total, users=users)

    else:
        try:
            issue_result = Dashboard.all_related_issues(limit=200, page=1)
        except Exception:
            issue_result = {'items': [], 'total': 0}
        try:
            notif_result = Notification.list(user_id, page=1, limit=200, is_read=is_read)
        except Exception:
            notif_result = {'items': [], 'total': 0}

        combined = []
        for item in issue_result.get('items', []):
            nitem = _issue_to_notification(item)
            if is_read is not None and nitem['is_read'] != is_read:
                continue
            combined.append(nitem)

        notif_items = notif_result.get('items', [])
        existing_cal_ref_ids = set()
        for item in notif_items:
            combined.append(item)
            if item.get('ref_type') == 'calendar' and item.get('ref_id'):
                existing_cal_ref_ids.add(item['ref_id'])

        cal_events = _calendar_events_for_user(user_id)
        for ev in cal_events:
            if ev['ref_id'] not in existing_cal_ref_ids:
                if is_read is not None and ev['is_read'] != is_read:
                    continue
                combined.append(ev)

        _enrich_projects(combined)
        combined.sort(key=lambda x: str(x.get('created', '')), reverse=True)
        total = len(combined)
        start = (page - 1) * dump
        end = start + dump
        items = combined[start:end]
        users = _enrich_items(combined)
        wiz.response.status(200, items=items, total=total, users=users)

def unread_count():
    user_id = config.session_user_id()
    count = 0
    try:
        count += Notification.unread_count(user_id)
    except Exception:
        pass
    try:
        read_records = readdb.rows(user_id=user_id, is_read=False, fields="issue_id")
        mention_records = mentiondb.rows(mentioned_user_id=user_id, is_read=False, fields="issue_id")
        unread_ids = set([r['issue_id'] for r in read_records] + [m['issue_id'] for m in mention_records])
        if unread_ids:
            excluded = set(Dashboard._excluded_project_ids())
            if excluded:
                issues = issuedb.rows(id=sorted(unread_ids), fields="id,project_id")
                count += sum(1 for i in issues if i['project_id'] not in excluded)
            else:
                count += len(unread_ids)
    except Exception:
        pass
    wiz.response.status(200, count=count)

def mark_read():
    user_id = config.session_user_id()
    notification_id = wiz.request.query("notification_id", True)
    if str(notification_id).startswith('issue_'):
        issue_id = str(notification_id)[6:]
        try:
            records = readdb.rows(user_id=user_id, issue_id=issue_id)
            now = datetime.datetime.now()
            for r in records:
                readdb.update(dict(is_read=True, last_read_at=now), id=r['id'])
            mentions = mentiondb.rows(mentioned_user_id=user_id, issue_id=issue_id)
            for m in mentions:
                mentiondb.update(dict(is_read=True), id=m['id'])
        except Exception as e:
            wiz.response.status(400, message=str(e))
    elif str(notification_id).startswith('cal_'):
        event_id = str(notification_id)[4:]
        try:
            existing = notificationdb.rows(user_id=user_id, ref_type='calendar', ref_id=event_id)
            now = datetime.datetime.now()
            if existing:
                for rec in existing:
                    if not rec.get('is_read'):
                        notificationdb.update(dict(is_read=True, read_at=now), id=rec['id'])
            else:
                ev = calendardb.get(id=event_id)
                notificationdb.insert(dict(
                    user_id=user_id,
                    project_id=ev.get('project_id', '') if ev else '',
                    type='calendar_invited',
                    ref_type='calendar',
                    ref_id=event_id,
                    title=ev.get('title', '') if ev else '',
                    message='',
                    is_read=True,
                    created=now,
                    read_at=now,
                ))
        except Exception as e:
            wiz.response.status(400, message=str(e))
    else:
        try:
            Notification.mark_read(notification_id, user_id)
        except Exception as e:
            wiz.response.status(400, message=str(e))
    wiz.response.status(200)

def mark_all_read():
    user_id = config.session_user_id()
    try:
        Notification.mark_all_read(user_id)
    except Exception:
        pass
    try:
        records = readdb.rows(user_id=user_id, is_read=False)
        now = datetime.datetime.now()
        for r in records:
            readdb.update(dict(is_read=True, last_read_at=now), id=r['id'])
        mentions = mentiondb.rows(mentioned_user_id=user_id, is_read=False)
        for m in mentions:
            mentiondb.update(dict(is_read=True), id=m['id'])
    except Exception:
        pass
    try:
        now = datetime.datetime.now()
        cal_events = _calendar_events_for_user(user_id)
        existing_notifs = notificationdb.rows(user_id=user_id, ref_type='calendar')
        existing_map = {}
        for n in existing_notifs:
            existing_map[n['ref_id']] = n
        for ev in cal_events:
            eid = ev['ref_id']
            if eid in existing_map:
                if not existing_map[eid].get('is_read'):
                    notificationdb.update(dict(is_read=True, read_at=now), id=existing_map[eid]['id'])
            else:
                notificationdb.insert(dict(
                    user_id=user_id,
                    project_id=ev.get('project_id', ''),
                    type='calendar_invited',
                    ref_type='calendar',
                    ref_id=eid,
                    title=ev.get('title', ''),
                    message='',
                    is_read=True,
                    created=now,
                    read_at=now,
                ))
    except Exception:
        pass
    wiz.response.status(200)
