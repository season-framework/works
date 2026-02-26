import season
import datetime

config = wiz.model("portal/wiki/config")
orm = wiz.model("portal/season/orm")
db = orm.use("content/revision", module="wiki")

class Model:
    def __init__(self, book):
        self.book = book
        self.book_id = book.data.id

    def read(self, revision_id):
        self.book.access.accessLevel(['admin', 'user', 'guest'])
        return db.get(id=revision_id)

    def load(self, content_id):
        self.book.access.accessLevel(['admin', 'user', 'guest'])
        rows = db.rows(content_id=content_id, order="DESC", orderby="created", page=1, dump=20, fields="id,user_id,name,content_id,created")
        # 일괄 사용자 정보 조회 (N+1 방지)
        user_ids = list(set(row['user_id'] for row in rows if row.get('user_id')))
        user_map = {}
        if user_ids:
            userdb = orm.use("user")
            users = userdb.rows(id=user_ids, fields="id,email,membership,name,mobile,status,profile_image,created,last_access")
            for u in users:
                user_map[u['id']] = u
        for row in rows:
            row['user'] = user_map.get(row['user_id'])
        return rows
    
    def commit(self, content_id, name=""):
        try:
            content = self.book.content.load(content_id)
            content['name'] = name
            content['content_id'] = content_id
            content['user_id'] = config.session_user_id()
            content['created'] = datetime.datetime.now()
            del content['id']

            db.insert(content)
        except Exception as e:
            pass