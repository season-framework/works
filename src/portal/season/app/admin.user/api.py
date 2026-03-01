import math

orm = wiz.model("portal/season/orm")
db_user = orm.use("user")

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

    temp_password = orm.random(8)
    db_user.update({'password': temp_password}, id=user_id)

    wiz.response.status(200, {'password': temp_password})

def user_delete():
    user_id = wiz.request.query("id", True)
    user = db_user.get(id=user_id)
    if user is None:
        wiz.response.status(404, "사용자를 찾을 수 없습니다")

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
