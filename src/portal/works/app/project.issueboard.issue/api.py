import json
import zipfile
import io
import urllib

pid = wiz.request.query("project_id", True)
projectModel = wiz.model("portal/works/project")
project = projectModel.get(pid)
if project is None:
    wiz.response.status(404, "Project not found")

def load():
    issue_id = wiz.request.query("issue_id", True)
    info = project.issueboard.issue.get(issue_id)
    wiz.response.status(200, info)

def update():
    data = wiz.request.query("data", True)
    data = json.loads(data)
    data = project.issueboard.issue.update(data)
    wiz.response.status(200, data)

def message():
    message_id = wiz.request.query("message_id", True)
    issue = project.issueboard.message.get(message_id)
    wiz.response.status(200, issue)

def messages():
    issue_id = wiz.request.query("issue_id", True)
    _type = wiz.request.query("type", True)
    favorite = None
    if _type == 'favorite':
        _type = ['message', 'file']
        favorite = 1
    if _type == 'message':
        _type = ['message', 'file']
    first = wiz.request.query("first", None)
    rows = project.issueboard.message.list(issue_id, type=_type, first=first, favorite=favorite)
    wiz.response.status(200, rows)

def unreadMessages():
    issue_id = wiz.request.query("issue_id", True)
    _type = wiz.request.query("type", True)
    favorite = None
    if _type == 'favorite':
        _type = ['message', 'file']
        favorite = 1
    if _type == 'message':
        _type = ['message', 'file']
    last = wiz.request.query("last", None)
    rows = project.issueboard.message.unread(issue_id, type=_type, last=last, favorite=favorite)
    wiz.response.status(200, rows)

def sendMessage():
    issue_id = wiz.request.query("issue_id", True)
    data = wiz.request.query("data", True)
    data = json.loads(data)
    data['issue_id'] = issue_id
    project.issueboard.message.update(data)
    wiz.response.status(200)

def favoriteMessage():
    message_id = wiz.request.query("id", True)
    issue_id = wiz.request.query("issue_id", True)
    favorite = wiz.request.query("favorite", True)
    project.issueboard.message.updateFavorite(message_id, favorite)
    wiz.response.status(200)

def markRead():
    issue_id = wiz.request.query("issue_id", True)
    user_id = wiz.session.get("id")
    try:
        project.issueboard.read.markRead(user_id, issue_id)
    except Exception as e:
        wiz.response.status(500, message=str(e))
    wiz.response.status(200)

def members():
    members = project.member.members()
    result = []
    for m in members:
        if not m.get('id'):
            continue
        if m.get('meta') and m['meta'].get('id'):
            result.append(dict(
                id=m['meta']['id'],
                name=m['meta'].get('name', ''),
                email=m['meta'].get('email', ''),
                profile_image=m['meta'].get('profile_image', '')
            ))
    wiz.response.status(200, result)

def download_files_zip():
    flask = wiz.response._flask
    files_data = wiz.request.query("files", True)
    files_data = json.loads(files_data)
    zip_name = wiz.request.query("zip_name", "files")

    fs = wiz.model("portal/works/fs").use(f"project/{project.id}/attachment")

    buf = io.BytesIO()
    try:
        with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
            used_names = {}
            for item in files_data:
                fid = item.get('id', '')
                fname = item.get('filename', fid)
                if not fs.isfile(fid):
                    continue
                filepath = fs.abspath(fid)
                if fname in used_names:
                    used_names[fname] += 1
                    name_parts = fname.rsplit('.', 1)
                    if len(name_parts) == 2:
                        fname = f"{name_parts[0]}_{used_names[fname]}.{name_parts[1]}"
                    else:
                        fname = f"{fname}_{used_names[fname]}"
                else:
                    used_names[fname] = 0
                zf.write(filepath, fname)
    except Exception as e:
        wiz.response.status(500, message=str(e))
    buf.seek(0)

    encoded_name = urllib.parse.quote(zip_name + ".zip")
    resp = flask.Response(buf.getvalue(), mimetype='application/zip')
    resp.headers['Content-Disposition'] = f"attachment; filename*=UTF-8''{encoded_name}"
    wiz.response.response(resp)
