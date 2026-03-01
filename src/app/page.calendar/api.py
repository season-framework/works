import json

Project = wiz.model("portal/works/project")
my_calendar = wiz.model("portal/works/struct/my_calendar")

def my_projects():
    user_id = wiz.session.user_id()
    try:
        result = my_calendar.myProjects(user_id)
    except Exception as e:
        wiz.response.status(500, message=str(e))
    wiz.response.status(200, dict(projects=result, user_id=user_id))

def search():
    user_id = wiz.session.user_id()
    year = int(wiz.request.query("year", 0))
    month = int(wiz.request.query("month", 0))
    if not year or not month:
        import datetime
        now = datetime.datetime.now()
        year = now.year
        month = now.month
    try:
        result = my_calendar.searchMyEvents(user_id, year, month)
    except Exception as e:
        wiz.response.status(500, message=str(e))
    wiz.response.status(200, result)

def move():
    event_id = wiz.request.query("id", True)
    project_id = wiz.request.query("project_id", True)
    new_start = wiz.request.query("start", True)
    new_end = wiz.request.query("end", True)

    try:
        project = Project.get(project_id)
        calendar = project.calendar
        calendar.move(event_id, new_start, new_end)
    except Exception as e:
        wiz.response.status(400, message=str(e))
    wiz.response.status(200)
