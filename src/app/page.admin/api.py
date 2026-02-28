import os
import datetime
import math
import bcrypt

orm = wiz.model("portal/season/orm")
db_user = orm.use("user")

# ─── 사용자 관리 ───

def user_list():
    page = int(wiz.request.query("page", 1))
    dump = int(wiz.request.query("dump", 20))
    keyword = wiz.request.query("keyword", "")
    membership = wiz.request.query("membership", "")
    status = wiz.request.query("status", "")

    where = dict()
    if membership:
        where['membership'] = membership
    if status:
        where['status'] = status

    query_fn = None
    if keyword:
        def query_fn(db, query):
            return query.where(
                (db.email.contains(keyword)) |
                (db.name.contains(keyword)) |
                (db.id.contains(keyword))
            )

    total = db_user.count(query=query_fn, **where)
    rows = db_user.rows(
        query=query_fn,
        page=page,
        dump=dump,
        orderby="last_access",
        order="DESC",
        fields="id,email,name,membership,status,created,last_access",
        **where
    )

    last_page = math.ceil(total / dump) if total else 1
    wiz.response.status(200, {
        'rows': rows,
        'total': total,
        'page': page,
        'dump': dump,
        'last_page': last_page
    })

def user_get():
    user_id = wiz.request.query("id", True)
    user = db_user.get(id=user_id)
    if user is None:
        wiz.response.status(404, "사용자를 찾을 수 없습니다")

    user = dict(user)
    del user['password']
    del user['onetimepass']
    del user['onetimepass_time']

    # 참여 프로젝트 목록
    try:
        db_member = orm.use("member", module="works")
        db_project = orm.use("project", module="works")
        members = db_member.rows(user=user_id)
        projects = []
        for m in members:
            proj = db_project.get(id=m['project_id'])
            if proj:
                projects.append({
                    'id': proj['id'],
                    'namespace': proj['namespace'],
                    'title': proj['title'],
                    'role': m['role'],
                    'status': proj.get('status', '')
                })
        user['projects'] = projects
    except:
        user['projects'] = []

    wiz.response.status(200, user)

def user_update():
    user_id = wiz.request.query("id", True)
    user = db_user.get(id=user_id)
    if user is None:
        wiz.response.status(404, "사용자를 찾을 수 없습니다")

    data = dict()
    name = wiz.request.query("name", None)
    email = wiz.request.query("email", None)
    membership = wiz.request.query("membership", None)
    status = wiz.request.query("status", None)
    mobile = wiz.request.query("mobile", None)

    if name is not None: data['name'] = name
    if email is not None: data['email'] = email
    if membership is not None: data['membership'] = membership
    if status is not None: data['status'] = status
    if mobile is not None: data['mobile'] = mobile

    if len(data) > 0:
        db_user.update(data, id=user_id)

    wiz.response.status(200, True)

def user_reset_password():
    user_id = wiz.request.query("id", True)
    user = db_user.get(id=user_id)
    if user is None:
        wiz.response.status(404, "사용자를 찾을 수 없습니다")

    # 임시 비밀번호 생성 (8자리)
    temp_password = orm.random(8)
    db_user.update({'password': temp_password}, id=user_id)

    wiz.response.status(200, {'password': temp_password})

def user_delete():
    user_id = wiz.request.query("id", True)
    user = db_user.get(id=user_id)
    if user is None:
        wiz.response.status(404, "사용자를 찾을 수 없습니다")

    # 논리 삭제
    db_user.update({'status': 'deleted'}, id=user_id)
    wiz.response.status(200, True)

def user_switch():
    user_id = wiz.request.query("id", True)
    user = db_user.get(id=user_id)
    if user is None:
        user = db_user.get(email=user_id)
    if user is None:
        wiz.response.status(404, "사용자를 찾을 수 없습니다")

    user_id = user['id']
    wiz.session.create(user_id)
    wiz.response.status(200, wiz.session.get())

# ─── 시스템 설정 ───

def config_load():
    sys_config = wiz.model("portal/season/system_config")
    category = wiz.request.query("category", "")

    if category:
        rows = sys_config.list(category=category)
    else:
        rows = sys_config.list()

    # 카테고리별 그룹핑
    result = {}
    for row in rows:
        cat = row['category']
        if cat not in result:
            result[cat] = []
        result[cat].append({
            'key': row['key_name'],
            'value': row['value'],
            'type': row['value_type'],
            'description': row.get('description', '')
        })

    wiz.response.status(200, result)

def config_update():
    sys_config = wiz.model("portal/season/system_config")
    data = wiz.request.query("data", True)

    if isinstance(data, str):
        import json
        data = json.loads(data)

    for item in data:
        category = item.get('category', '')
        key = item.get('key', '')
        value = item.get('value', '')
        value_type = item.get('type', 'string')
        description = item.get('description', '')

        if not category or not key:
            continue

        # password 타입: '********' 전송 시 기존 값 유지 (변경 안함)
        if value_type == 'password' and value == '********':
            continue

        sys_config.set(category, key, value, value_type=value_type, description=description)

    wiz.response.status(200, True)

def smtp_test():
    to = wiz.request.query("to", True)

    sys_config = wiz.model("portal/season/system_config")
    config = wiz.config("season")

    smtp_host = sys_config.get("smtp", "smtp_host", getattr(config, 'smtp_host', None))
    smtp_port = sys_config.get("smtp", "smtp_port", getattr(config, 'smtp_port', 587))
    smtp_sender = sys_config.get("smtp", "smtp_sender", getattr(config, 'smtp_sender', None))
    smtp_password = sys_config.get("smtp", "smtp_password", getattr(config, 'smtp_password', None))

    if not smtp_host or not smtp_sender:
        wiz.response.status(400, "SMTP 설정이 완료되지 않았습니다")

    import smtplib
    from email.mime.text import MIMEText

    html = """<div style="padding: 24px;">
    <h2>SMTP 테스트 이메일</h2>
    <p>이 이메일은 관리자 페이지에서 발송한 SMTP 테스트 메일입니다.</p>
    <p>발송 시간: {time}</p>
</div>""".format(time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    msg = MIMEText(html, 'html', _charset='utf8')
    msg['Subject'] = '[시즌웍스] SMTP 테스트 이메일'
    msg['From'] = smtp_sender
    msg['To'] = to

    try:
        mailserver = smtplib.SMTP(smtp_host, int(smtp_port))
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.login(smtp_sender, smtp_password)
        mailserver.sendmail(smtp_sender, to, msg.as_string())
        mailserver.quit()
    except Exception as e:
        wiz.response.status(500, f"SMTP 테스트 실패: {str(e)}")

    wiz.response.status(200, "테스트 이메일이 발송되었습니다")

def template_list():
    fs = wiz.project.fs(os.path.join("config", "smtp"))
    files = fs.list()
    templates = []
    for f in files:
        if f.endswith('.html'):
            name = f.replace('.html', '')
            templates.append({'name': name, 'filename': f})
    wiz.response.status(200, templates)

def template_read():
    name = wiz.request.query("name", True)
    fs = wiz.project.fs(os.path.join("config", "smtp"))
    filename = f"{name}.html"
    if not fs.exists(filename):
        wiz.response.status(404, "템플릿을 찾을 수 없습니다")
    content = fs.read(filename)
    wiz.response.status(200, {'name': name, 'content': content})

def template_update():
    name = wiz.request.query("name", True)
    content = wiz.request.query("content", True)
    fs = wiz.project.fs(os.path.join("config", "smtp"))
    filename = f"{name}.html"
    fs.write(filename, content)
    wiz.response.status(200, True)

# ─── 프로젝트 관리 ───

def project_list():
    page = int(wiz.request.query("page", 1))
    dump = int(wiz.request.query("dump", 20))
    keyword = wiz.request.query("keyword", "")
    status = wiz.request.query("status", "")
    visibility = wiz.request.query("visibility", "")

    db_project = orm.use("project", module="works")
    db_member = orm.use("member", module="works")

    where = dict()
    if status:
        where['status'] = status
    if visibility:
        where['visibility'] = visibility

    query_fn = None
    if keyword:
        def query_fn(db, query):
            return query.where(
                (db.title.contains(keyword)) |
                (db.namespace.contains(keyword))
            )

    total = db_project.count(query=query_fn, **where)
    rows = db_project.rows(
        query=query_fn,
        page=page,
        dump=dump,
        orderby="updated",
        order="DESC",
        fields="id,namespace,title,short,visibility,status,start,end,icon,created,updated",
        **where
    )

    # 각 프로젝트의 멤버 수 추가
    for row in rows:
        try:
            row['member_count'] = db_member.count(project_id=row['id'])
        except:
            row['member_count'] = 0

    last_page = math.ceil(total / dump) if total else 1
    wiz.response.status(200, {
        'rows': rows,
        'total': total,
        'page': page,
        'dump': dump,
        'last_page': last_page
    })

def project_update_status():
    project_id = wiz.request.query("id", True)
    new_status = wiz.request.query("status", True)

    db_project = orm.use("project", module="works")
    proj = db_project.get(id=project_id)
    if proj is None:
        wiz.response.status(404, "프로젝트를 찾을 수 없습니다")

    if new_status not in ['draft', 'open', 'close']:
        wiz.response.status(400, "유효하지 않은 상태입니다")

    db_project.update({'status': new_status, 'updated': datetime.datetime.now()}, id=project_id)
    wiz.response.status(200, True)

def project_delete():
    project_id = wiz.request.query("id", True)

    db_project = orm.use("project", module="works")
    db_member = orm.use("member", module="works")

    proj = db_project.get(id=project_id)
    if proj is None:
        wiz.response.status(404, "프로젝트를 찾을 수 없습니다")

    # 관리자 전용: draft 제한 없이 삭제
    db_member.delete(project_id=project_id)
    db_project.delete(id=project_id)
    wiz.response.status(200, True)

def project_storage():
    project_id = wiz.request.query("id", True)

    config_works = wiz.config("works")
    storage_path = getattr(config_works, 'STORAGE_PATH', 'storage/works')

    # SystemConfig에서 오버라이드 확인
    try:
        sys_config = wiz.model("portal/season/system_config")
        db_path = sys_config.get("storage", "works_path")
        if db_path:
            storage_path = db_path
    except:
        pass

    project_dir = os.path.join(storage_path, project_id)
    total_size = 0
    if os.path.exists(project_dir):
        for dirpath, dirnames, filenames in os.walk(project_dir):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.isfile(fp):
                    total_size += os.path.getsize(fp)

    # 바이트 → MB 변환
    size_mb = round(total_size / (1024 * 1024), 2)
    wiz.response.status(200, {'size_bytes': total_size, 'size_mb': size_mb})

# ─── 위키 관리 ───

def wiki_list():
    page = int(wiz.request.query("page", 1))
    dump = int(wiz.request.query("dump", 20))
    keyword = wiz.request.query("keyword", "")
    visibility = wiz.request.query("visibility", "")

    db_book = orm.use("book", module="wiki")
    db_access = orm.use("access", module="wiki")
    db_content = orm.use("content", module="wiki")

    where = dict()
    if visibility:
        where['visibility'] = visibility

    query_fn = None
    if keyword:
        def query_fn(db, query):
            return query.where(
                (db.title.contains(keyword)) |
                (db.namespace.contains(keyword))
            )

    total = db_book.count(query=query_fn, **where)
    rows = db_book.rows(
        query=query_fn,
        page=page,
        dump=dump,
        orderby="updated",
        order="DESC",
        fields="id,namespace,title,visibility,created,updated,icon",
        **where
    )

    # 각 위키의 접근 권한 수, 페이지 수 추가
    for row in rows:
        try:
            row['access_count'] = db_access.count(book_id=row['id'])
        except:
            row['access_count'] = 0
        try:
            row['page_count'] = db_content.count(book_id=row['id'])
        except:
            row['page_count'] = 0

    last_page = math.ceil(total / dump) if total else 1
    wiz.response.status(200, {
        'rows': rows,
        'total': total,
        'page': page,
        'dump': dump,
        'last_page': last_page
    })

def wiki_access():
    book_id = wiz.request.query("id", True)

    db_book = orm.use("book", module="wiki")
    db_access = orm.use("access", module="wiki")

    book = db_book.get(id=book_id)
    if book is None:
        wiz.response.status(404, "위키를 찾을 수 없습니다")

    rows = db_access.rows(book_id=book_id)

    # 사용자 이름 조회
    for row in rows:
        if row['type'] == 'user':
            user = db_user.get(id=row['key'], fields="id,email,name")
            if user:
                row['user_name'] = user['name']
                row['user_email'] = user['email']

    wiz.response.status(200, {'book': book, 'access': rows})

def wiki_delete():
    book_id = wiz.request.query("id", True)

    db_book = orm.use("book", module="wiki")
    db_access = orm.use("access", module="wiki")
    db_content = orm.use("content", module="wiki")

    book = db_book.get(id=book_id)
    if book is None:
        wiz.response.status(404, "위키를 찾을 수 없습니다")

    # 관리자 전용: 위키 삭제 (접근 권한, 콘텐츠, 책 모두 삭제)
    db_content.delete(book_id=book_id)
    db_access.delete(book_id=book_id)
    db_book.delete(id=book_id)
    wiz.response.status(200, True)
