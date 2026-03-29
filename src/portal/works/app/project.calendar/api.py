import json
import datetime

config = wiz.model("portal/works/config")
orm = wiz.model("portal/season/orm")

user_id = wiz.session.get("id")
project_id = wiz.request.query("project_id", True)
project = wiz.model("portal/works/project").get(project_id)
if project is None:
    wiz.response.status(404, "Project not found")

def search():
    year = int(wiz.request.query("year", datetime.datetime.now().year))
    month = int(wiz.request.query("month", datetime.datetime.now().month))
    rows = project.calendar.search(year, month)
    wiz.response.status(200, rows)

def read():
    event_id = wiz.request.query("id", True)
    data = project.calendar.get(event_id)
    isEditable = project.member.accessLevel(['admin', 'manager', 'user'], False)
    wiz.response.status(200, data=data, isEditable=isEditable)

def create():
    data = wiz.request.query()
    if 'project_id' in data:
        del data['project_id']
    try:
        result = project.calendar.create(data)
    except Exception as e:
        wiz.response.status(400, message=str(e))
    wiz.response.status(200, result)

def update():
    data = wiz.request.query()
    if 'project_id' in data:
        del data['project_id']
    try:
        result = project.calendar.update(data)
    except Exception as e:
        wiz.response.status(400, message=str(e))
    wiz.response.status(200, result)

def delete():
    event_id = wiz.request.query("id", True)
    try:
        project.calendar.delete(event_id)
    except Exception as e:
        wiz.response.status(400, message=str(e))
    wiz.response.status(200, True)

def move():
    event_id = wiz.request.query("id", True)
    new_start = wiz.request.query("start", True)
    new_end = wiz.request.query("end", True)
    try:
        result = project.calendar.move(event_id, new_start, new_end)
    except Exception as e:
        wiz.response.status(400, message=str(e))
    wiz.response.status(200, result)

def categories():
    rows = project.calendar.getCategories()
    wiz.response.status(200, rows)

def create_category():
    data = wiz.request.query()
    if 'project_id' in data:
        del data['project_id']
    try:
        result = project.calendar.createCategory(data)
    except Exception as e:
        wiz.response.status(400, message=str(e))
    wiz.response.status(200, result)

def update_category():
    data = wiz.request.query()
    if 'project_id' in data:
        del data['project_id']
    try:
        result = project.calendar.updateCategory(data)
    except Exception as e:
        wiz.response.status(400, message=str(e))
    wiz.response.status(200, result)

def delete_category():
    category_id = wiz.request.query("id", True)
    try:
        project.calendar.deleteCategory(category_id)
    except Exception as e:
        wiz.response.status(400, message=str(e))
    wiz.response.status(200, True)

def reorder_categories():
    order_list = wiz.request.query("order_list", True)
    try:
        order_list = json.loads(order_list)
    except Exception:
        wiz.response.status(400, message="Invalid order_list format")
    try:
        project.calendar.reorderCategories(order_list)
    except Exception as e:
        wiz.response.status(400, message=str(e))
    wiz.response.status(200, True)

def attendees():
    event_id = wiz.request.query("event_id", True)
    rows = project.calendar.getAttendees(event_id)
    wiz.response.status(200, rows)

def add_attendee():
    event_id = wiz.request.query("event_id", True)
    target_user_id = wiz.request.query("user_id", True)
    try:
        result = project.calendar.addAttendee(event_id, target_user_id)
    except Exception as e:
        wiz.response.status(400, message=str(e))
    wiz.response.status(200, result)

def remove_attendee():
    event_id = wiz.request.query("event_id", True)
    target_user_id = wiz.request.query("user_id", True)
    try:
        project.calendar.removeAttendee(event_id, target_user_id)
    except Exception as e:
        wiz.response.status(400, message=str(e))
    wiz.response.status(200, True)

def add_group_attendee():
    event_id = wiz.request.query("event_id", True)
    group_type = wiz.request.query("group_type", True)
    group_id = wiz.request.query("group_id", "")
    try:
        result = project.calendar.addGroupAttendee(event_id, group_type, group_id)
    except Exception as e:
        wiz.response.status(400, message=str(e))
    wiz.response.status(200, result)

def remove_group_attendee():
    event_id = wiz.request.query("event_id", True)
    group_type = wiz.request.query("group_type", True)
    group_id = wiz.request.query("group_id", "")
    try:
        project.calendar.removeGroupAttendee(event_id, group_type, group_id)
    except Exception as e:
        wiz.response.status(400, message=str(e))
    wiz.response.status(200, True)

def members():
    memberdb = orm.use("member", module="works")
    userdb = orm.use("user")
    users = memberdb.rows(project_id=project_id)
    result = []
    for m in users:
        user = userdb.get(id=m['user'])
        if user is None:
            continue
        result.append(dict(
            id=m['user'],
            name=user.get('name', ''),
            email=user.get('email', ''),
            role=m.get('role', ''),
            profile_image=user.get('profile_image', '')
        ))
    wiz.response.status(200, result)
