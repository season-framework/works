import json
import time
import math
import functools

pid = wiz.request.query("project_id", True)
projectModel = wiz.model("portal/works/project")
project = projectModel.get(pid)
if project is None:
    wiz.response.status(404, "Project not found")

def load():
    labels = project.issueboard.label.list()
    wiz.response.status(200, labels)

def search():
    dump = 20
    label_id = wiz.request.query("label_id", None)
    status = wiz.request.query("status", True)
    page = wiz.request.query("page", 1)
    page = int(page)
    total, rows = project.issueboard.label.search(status, page=page, label_id=label_id, dump=dump)
    wiz.response.status(200, rows=rows, lastpage=math.ceil(total/dump), page=page)

def addLabel():
    query = wiz.request.query()
    obj = project.issueboard.label.create(**query)
    wiz.response.status(200, obj)

def removeLabel():
    label_id = wiz.request.query("id")
    project.issueboard.label.remove(label_id)
    wiz.response.status(200)

def updateLabels():
    data = wiz.request.query("data")
    data = json.loads(data)
    project.issueboard.label.update(data)
    wiz.response.status(200)

def loadIssues():
    issueIds = wiz.request.query("issueIds")
    issueIds = json.loads(issueIds)
    issues = project.issueboard.issue.load(issueIds)
    wiz.response.status(200, issues)

def updateIssue():
    data = wiz.request.query("data", True)
    data = json.loads(data)
    for item in data:
        project.issueboard.issue.updateLabel(item['issue_id'], item['label_id'])
    wiz.response.status(200)

def loadAllIssues():
    page = int(wiz.request.query("page", 1))
    dump = 30
    status_filter = wiz.request.query("status", "active")

    orm = wiz.model("portal/season/orm")
    issuedb = orm.use("issueboard/issue", module="works")
    labeldb = orm.use("issueboard/label", module="works")

    # 라벨 맵 생성 (칸반 순서 포함)
    labels_raw = labeldb.rows(project_id=pid)
    labels_raw.sort(key=lambda x: (x.get('mode', 0), x.get('order', 0)))
    label_map = {}
    label_order_map = {}
    for idx, lb in enumerate(labels_raw):
        label_map[lb['id']] = lb['title']
        label_order_map[lb['id']] = idx

    kwargs = dict()
    kwargs['project_id'] = pid
    kwargs['fields'] = "id,label_id,user_id,title,process,level,status,planstart,planend,created,updated,todo,worker"

    if status_filter == "active":
        kwargs['status'] = ['open', 'work', 'finish']
    elif status_filter == "noti":
        kwargs['status'] = ['noti']
    elif status_filter == "event":
        kwargs['status'] = ['event']
    elif status_filter == "closed":
        kwargs['status'] = ['close']
    elif status_filter == "canceled":
        kwargs['status'] = ['cancel']

    keyword = wiz.request.query("keyword", "").strip()

    all_rows = issuedb.rows(**kwargs)

    if keyword:
        all_rows = [r for r in all_rows if keyword.lower() in (r.get('title', '') or '').lower()]

    for row in all_rows:
        row['label_title'] = label_map.get(row.get('label_id'), '미분류')
        row['label_order'] = label_order_map.get(row.get('label_id'), 99999)

    # 정렬: 라벨(칸반 순서) ASC → 마감일(planend) ASC (nulls last) → 시작일(planstart) DESC (nulls last)
    def compare_issues(a, b):
        la = a.get('label_order', 99999)
        lb_ord = b.get('label_order', 99999)
        if la != lb_ord:
            return -1 if la < lb_ord else 1

        pa = a.get('planend') or ''
        pb = b.get('planend') or ''
        if pa != pb:
            if not pa: return 1
            if not pb: return -1
            return -1 if pa < pb else 1

        sa = a.get('planstart') or ''
        sb = b.get('planstart') or ''
        if sa != sb:
            if not sa: return 1
            if not sb: return -1
            return 1 if sa < sb else -1

        return 0

    all_rows.sort(key=functools.cmp_to_key(compare_issues))

    total = len(all_rows)
    lastpage = math.ceil(total / dump) if total > 0 else 1
    start_idx = (page - 1) * dump
    end_idx = start_idx + dump
    rows = all_rows[start_idx:end_idx]

    wiz.response.status(200, rows=rows, total=total, lastpage=lastpage, page=page)
