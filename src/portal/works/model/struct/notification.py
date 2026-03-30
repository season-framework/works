import datetime

config = wiz.model("portal/works/config")
orm = wiz.model("portal/season/orm")
notificationdb = orm.use("notification", module="works")

class Model:
    @staticmethod
    def create(user_id, ntype, title, message="", project_id="", ref_type="", ref_id=""):
        data = dict()
        data['user_id'] = user_id
        data['project_id'] = project_id
        data['type'] = ntype
        data['ref_type'] = ref_type
        data['ref_id'] = ref_id
        data['title'] = title
        data['message'] = message
        data['is_read'] = False
        data['created'] = datetime.datetime.now()
        insert_id = notificationdb.insert(data)

        # Push 발송 (best-effort)
        try:
            push = wiz.model("portal/works/struct/push")
            push.send(user_id, title, message, url="/notification")
        except Exception:
            pass

        return insert_id

    @staticmethod
    def create_bulk(user_ids, ntype, title, message="", project_id="", ref_type="", ref_id="", exclude_user_id=None):
        now = datetime.datetime.now()
        created_ids = []
        for uid in user_ids:
            if exclude_user_id and uid == exclude_user_id:
                continue
            data = dict()
            data['user_id'] = uid
            data['project_id'] = project_id
            data['type'] = ntype
            data['ref_type'] = ref_type
            data['ref_id'] = ref_id
            data['title'] = title
            data['message'] = message
            data['is_read'] = False
            data['created'] = now
            insert_id = notificationdb.insert(data)
            created_ids.append(insert_id)

            try:
                push = wiz.model("portal/works/struct/push")
                push.send(uid, title, message, url="/notification")
            except Exception:
                pass

        return created_ids

    @staticmethod
    def list(user_id, page=1, limit=20, is_read=None, ref_type=None):
        where = dict()
        where['user_id'] = user_id
        if is_read is not None:
            where['is_read'] = is_read
        if ref_type is not None:
            where['ref_type'] = ref_type
        where['page'] = page
        where['dump'] = limit
        where['orderby'] = 'created'
        where['order'] = 'DESC'
        rows = notificationdb.rows(**where)
        total = notificationdb.count(user_id=user_id, **(dict(is_read=is_read) if is_read is not None else {}), **(dict(ref_type=ref_type) if ref_type is not None else {}))

        for i in range(len(rows)):
            if rows[i].get('created') and hasattr(rows[i]['created'], 'strftime'):
                rows[i]['created'] = rows[i]['created'].strftime('%Y-%m-%d %H:%M:%S')
            if rows[i].get('read_at') and hasattr(rows[i]['read_at'], 'strftime'):
                rows[i]['read_at'] = rows[i]['read_at'].strftime('%Y-%m-%d %H:%M:%S')

        return dict(items=rows, total=total)

    @staticmethod
    def unread_count(user_id):
        return notificationdb.count(user_id=user_id, is_read=False)

    @staticmethod
    def mark_read(notification_id, user_id):
        item = notificationdb.get(id=notification_id, user_id=user_id)
        if item is None:
            raise Exception("Notification not found")
        notificationdb.update(dict(is_read=True, read_at=datetime.datetime.now()), id=notification_id)

    @staticmethod
    def mark_all_read(user_id):
        rows = notificationdb.rows(user_id=user_id, is_read=False)
        now = datetime.datetime.now()
        for row in rows:
            notificationdb.update(dict(is_read=True, read_at=now), id=row['id'])

    @staticmethod
    def delete_old(days=90):
        cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
        rows = notificationdb.rows(created=lambda f: f < cutoff.strftime('%Y-%m-%d %H:%M:%S'))
        for row in rows:
            notificationdb.delete(id=row['id'])
