import os
import datetime
import math

orm = wiz.model("portal/season/orm")

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

    size_mb = round(total_size / (1024 * 1024), 2)
    wiz.response.status(200, {'size_bytes': total_size, 'size_mb': size_mb})
