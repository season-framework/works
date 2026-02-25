import json
import urllib.request

pid = wiz.request.query("project_id", True)
projectModel = wiz.model("portal/works/project")
project = projectModel.get(pid)
if project is None:
    wiz.response.status(404, message="프로젝트를 찾을 수 없습니다")

def __send_notification__(message):
    url = "https://notification.nanoha.kr/api/notification"
    body = {
        "title": "시즌웍스",
        "message": message,
    }
    try:
        json_body = json.dumps(body).encode('utf-8')
        headers = {'Content-Type': 'application/json'}
        req = urllib.request.Request(url, data=json_body, headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=2) as response:
            pass
            # print(f"Status Code: {response.getcode()}")
            # print(f"Response: {response.read().decode('utf-8')}")
    except: pass

def load():
    issue_id = wiz.request.query("issue_id", True)
    info = project.issueboard.issue.get(issue_id)
    wiz.response.status(200, info)

def update():
    data = wiz.request.query("data", True)
    data = json.loads(data)
    data = project.issueboard.issue.update(data)
    project_title = wiz.request.query("project_title", "")
    issue_title = data.get("title", "")
    __send_notification__(f"{project_title} 프로젝트의 {issue_title} 이슈가 업데이트되었습니다.")
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
    project_title = wiz.request.query("project_title", "")
    issue_title = wiz.request.query("issue_title", "")
    __send_notification__(f"{project_title} 프로젝트의 {issue_title} 이슈에 새로운 메세지가 있습니다.")
    wiz.response.status(200)

def favoriteMessage():
    message_id = wiz.request.query("id", True)
    issue_id = wiz.request.query("issue_id", True)
    favorite = wiz.request.query("favorite", True)
    project.issueboard.message.updateFavorite(message_id, favorite)
    wiz.response.status(200)
