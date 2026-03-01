import math

orm = wiz.model("portal/season/orm")
db_user = orm.use("user")

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

    db_content.delete(book_id=book_id)
    db_access.delete(book_id=book_id)
    db_book.delete(id=book_id)
    wiz.response.status(200, True)
