import os
import math
import json
import time
import datetime
import shutil
import zipfile
import tempfile

segment = wiz.request.match("/api/works/project/<project_id>/<path:path>")
action = segment.path
project_id = segment.project_id
projectModel = wiz.model("portal/works/project")
project = projectModel.get(project_id)
fs = wiz.model("portal/works/fs").use(f"project/{project_id}/drive")

# 공통 null 체크 (FN-0008): load 외 모든 액션에서도 project 존재 확인
if project is None and action != "load":
    wiz.response.status(404)

# Path Traversal 방어 함수 (FN-0003)
def safe_path(user_path):
    """사용자 입력 경로가 base 디렉토리를 벗어나지 못하도록 검증"""
    base = os.path.realpath(fs.abspath(""))
    resolved = os.path.realpath(fs.abspath(user_path))
    if not resolved.startswith(base + os.sep) and resolved != base:
        wiz.response.status(403, "접근이 허용되지 않는 경로입니다")
    return user_path

# Project API
if action == "load":
    if project is None:
        wiz.response.status(404)
    wiz.response.status(200, project.data)

elif action == "update":
    data = wiz.request.query("data", True)
    data = json.loads(data)
    data['id'] = project.data['id']
    
    namespaceChanged = False
    if project.data['namespace'] != data['namespace']:
        exists = projectModel.get(data['namespace'])
        if exists is not None:
            wiz.response.status(400, 'Namespace가 사용중입니다')
        namespaceChanged = True
    
    project.update(data)
    project = projectModel.get(data['namespace'])
    wiz.response.status(200, data=project.data, namespaceChanged=namespaceChanged)

elif action == "untrack":
    status = wiz.request.query("status", True)
    project.untrack(status)
    wiz.response.status(200)

# Member API
elif action == "member/load":
    members = project.member.members()
    wiz.response.status(200, members)

elif action == "member/create":
    try:
        user = wiz.request.query("user", True)
        role = wiz.request.query("role", True)
        project.member.create(user, role)
    except Exception as e:
        wiz.response.status(500, str(e))
    wiz.response.status(200)

elif action == "member/remove":
    try:
        user = wiz.request.query("user", True)
        project.member.remove(user)
    except Exception as e:
        wiz.response.status(500, str(e))
    wiz.response.status(200)

elif action == "member/update":
    try:
        user = wiz.request.query("user", True)
        role = wiz.request.query("role", True)
        project.member.update(dict(role=role, user=user))
    except Exception as e:
        wiz.response.status(500, str(e))
    wiz.response.status(200)

# Plan API
elif action == "plan/load":
    data = project.plan.load()
    wiz.response.status(200, data)

elif action == "plan/update":
    data = wiz.request.query("data", True)
    data = json.loads(data)
    project.plan.update(data)
    wiz.response.status(200)

# Drive API
elif action == "drive/tree":
    try:
        project.member.accessLevel(['admin', 'manager', 'user', 'guest'])
    except Exception as e:
        wiz.response.status(401, str(e))
    path = wiz.request.query("path", "")
    safe_path(path)
    fs.makedirs(path)
    root = driveItem(path)
    children = []
    for item in fs.ls(path):
        children.append(driveItem(os.path.join(path, item)))
    wiz.response.status(200, dict(root=root, children=children))

elif action == "drive/create":
    try:
        project.member.accessLevel(['admin', 'manager', 'user'])
    except Exception as e:
        wiz.response.status(401, str(e))
    root_id = wiz.request.query("root_id", "")
    title = wiz.request.query("title", True)
    path = os.path.join(root_id, title)
    safe_path(path)
    if fs.exists(path):
        wiz.response.status(401)
    fs.makedirs(path)
    wiz.response.status(200)

elif action == "drive/update":
    try:
        project.member.accessLevel(['admin', 'manager', 'user'])
    except Exception as e:
        wiz.response.status(401, str(e))
    file_id = wiz.request.query("id", True)
    root_id = wiz.request.query("root_id", "")
    title = wiz.request.query("title", True)
    safe_path(file_id)
    path = os.path.join(root_id, title)
    safe_path(path)
    if fs.exists(path):
        wiz.response.status(401)
    fs.move(file_id, path)
    wiz.response.status(200)

elif action == "drive/delete":
    try:
        project.member.accessLevel(['admin', 'manager', 'user'])
    except Exception as e:
        wiz.response.status(401, str(e))
    path = wiz.request.query("id", "")
    if len(path) == 0:
        wiz.response.status(401)
    safe_path(path)
    fs.remove(path)
    wiz.response.status(200)

elif action == "drive/deletes":
    try:
        project.member.accessLevel(['admin', 'manager', 'user'])
    except Exception as e:
        wiz.response.status(401, str(e))
    data = wiz.request.query("data", "")
    data = json.loads(data)
    for path in data:
        safe_path(path)
        fs.remove(path)
    wiz.response.status(200)

elif action == "drive/upload":
    try:
        project.member.accessLevel(['admin', 'manager', 'user'])
    except Exception as e:
        wiz.response.status(401, str(e))

    filepath = None
    try:
        filepath = json.loads(wiz.request.query("path", ""))
    except Exception:
        pass

    segment = wiz.request.match("/api/works/project/<project_id>/drive/upload/<path:path>")
    path = segment.path
    if path is None: path = ""
    safe_path(path)
    path = fs.abspath(path)
    files = wiz.request.files()
    for i in range(len(files)):
        f = files[i]
        try: fpath = filepath[i]
        except Exception: fpath = None
        name = f.filename
        if fpath is not None:
            name = fpath
        target = os.path.join(path, name)
        # 업로드 파일명도 traversal 방어
        base = os.path.realpath(fs.abspath(""))
        if not os.path.realpath(target).startswith(base + os.sep):
            continue
        fs.write.file(target, f)
    wiz.response.status(200)

elif action == "drive/download":
    try:
        project.member.accessLevel(['admin', 'manager', 'user', 'guest'])
    except Exception as e:
        wiz.response.status(401, str(e))
    segment = wiz.request.match("/api/works/project/<project_id>/drive/download/<path:path>")
    path = segment.path
    safe_path(path)
    path = fs.abspath(path)

    if fs.isdir(path):
        filename = os.path.splitext(os.path.basename(path))[0] + ".zip"
        zippath = os.path.join(tempfile.gettempdir(), 'works', datetime.datetime.now().strftime("%Y%m%d"), str(int(time.time())), filename)
        if len(zippath) < 10: 
            wiz.response.status(404)
        try:
            os.remove(zippath)
        except Exception:
            pass
        os.makedirs(os.path.dirname(zippath), exist_ok=True)
        with zipfile.ZipFile(zippath, 'w') as zipdata:
            for folder, subfolders, files in os.walk(path):
                for file in files:
                    zipdata.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder, file), path), compress_type=zipfile.ZIP_DEFLATED)
        path = zippath

    wiz.response.download(path)

elif action.startswith("attachment/list"):
    try:
        project.member.accessLevel(['admin', 'manager', 'user', 'guest'])
    except Exception as e:
        wiz.response.status(401, str(e))
    page = int(wiz.request.query("page", 1))
    namespace = wiz.request.query("ns", ".attachment")
    dump = 24
    if namespace == '.attachment': dump = 40
    try:
        orm = wiz.model("portal/season/orm")
        attachmentdb = orm.use("attachment", module="works")
        where = dict()
        where['project_id'] = project_id
        where['namespace'] = namespace
        where['page'] = page
        where['dump'] = dump
        where['orderby'] = "created"
        where['order'] = "DESC"
        where['like'] = "namespace"
        total = attachmentdb.count(**where)
        rows = attachmentdb.rows(**where)
    except Exception as e:
        wiz.response.status(500)
    if namespace == '.attachment':
        cache = dict()
        for row in rows:
            try:
                issue_id = row["namespace"].split(":")[1]
                if issue_id not in cache:
                    cache[issue_id] = project.issueboard.issue.get(issue_id)
                row["issue_title"] = cache[issue_id]["title"]
            except Exception:
                row["issue_title"] = None

    wiz.response.status(200, rows=rows, lastpage=math.ceil(total/dump), page=page)

else:
    wiz.response.status(404)

def driveItem(path):
    def convert_size():
        size_bytes = os.path.getsize(fs.abspath(path)) 
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    item = dict()
    item['id'] = path
    item['type'] = 'folder' if fs.isdir(path) else 'file'
    item['title'] = os.path.basename(path)
    item['root_id'] = os.path.dirname(path)
    item['created'] = datetime.datetime.fromtimestamp(os.stat(fs.abspath(path)).st_ctime).strftime('%Y-%m-%d %H:%M:%S')
    item['modified'] = datetime.datetime.fromtimestamp(os.stat(fs.abspath(path)).st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    item['size'] = convert_size()
    return item
