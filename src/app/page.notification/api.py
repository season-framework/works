Dashboard = wiz.model("portal/works/struct/dashboard")
config = wiz.model("portal/works/config")

def _collect_users(items):
    user_ids = set()
    for item in items:
        if item.get('user_id'):
            user_ids.add(item['user_id'])
        worker = item.get('worker')
        if worker:
            if isinstance(worker, list):
                for w in worker:
                    user_ids.add(w)
            elif isinstance(worker, str) and worker:
                user_ids.add(worker)
    users = {}
    for uid in user_ids:
        users[uid] = config.get_user_info(wiz, uid)
    return users

def all_issues():
    page = int(wiz.request.query("page", 1))
    dump = int(wiz.request.query("dump", 20))
    try:
        result = Dashboard.all_related_issues(limit=dump, page=page)
    except Exception as e:
        wiz.response.status(500, message=str(e))
    result['users'] = _collect_users(result.get('items', []))
    wiz.response.status(200, **result)

def mentioned_issues():
    page = int(wiz.request.query("page", 1))
    dump = int(wiz.request.query("dump", 20))
    try:
        result = Dashboard.mentioned_issues(limit=dump, page=page)
    except Exception as e:
        wiz.response.status(500, message=str(e))
    result['users'] = _collect_users(result.get('items', []))
    wiz.response.status(200, **result)
