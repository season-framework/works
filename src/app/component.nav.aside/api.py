Dashboard = wiz.model("portal/works/struct/dashboard")
Notification = wiz.model("portal/works/struct/notification")
Push = wiz.model("portal/works/struct/push")
config = wiz.model("portal/works/config")

def my_projects():
    projects = Dashboard.my_projects()
    wiz.response.status(200, projects)

def profile_image():
    user_id = wiz.session.get("id")
    if not user_id:
        wiz.response.status(200, image=None)
    orm = wiz.model("portal/season/orm")
    db = orm.use("user")
    try:
        user = db.get(id=user_id, fields="profile_image")
    except Exception:
        wiz.response.status(200, image=None)
    img = user.get("profile_image") if user else None
    if img and len(str(img)) < 10:
        img = None
    wiz.response.status(200, image=img)

def unread_count():
    user_id = config.session_user_id()
    count = 0
    try:
        count += Notification.unread_count(user_id)
    except Exception:
        pass
    try:
        orm = wiz.model("portal/season/orm")
        readdb = orm.use("issueboard/issue/read", module="works")
        mentiondb = orm.use("issueboard/mention", module="works")
        issuedb = orm.use("issueboard/issue", module="works")
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

def push_subscribe():
    user_id = wiz.session.get("id")
    if not user_id:
        wiz.response.status(401, message="Login required")
    endpoint = wiz.request.query("endpoint", True)
    p256dh = wiz.request.query("p256dh", True)
    auth = wiz.request.query("auth", True)
    user_agent = wiz.request.query("user_agent", "")
    subscription_info = dict(endpoint=endpoint, keys=dict(p256dh=p256dh, auth=auth), user_agent=user_agent)
    try:
        Push.subscribe(user_id, subscription_info)
    except Exception as e:
        wiz.response.status(500, message=str(e))
    wiz.response.status(200)

def push_unsubscribe():
    user_id = wiz.session.get("id")
    if not user_id:
        wiz.response.status(401, message="Login required")
    endpoint = wiz.request.query("endpoint", True)
    try:
        Push.unsubscribe(user_id, endpoint)
    except Exception as e:
        wiz.response.status(500, message=str(e))
    wiz.response.status(200)
