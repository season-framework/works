Dashboard = wiz.model("portal/works/struct/dashboard")
MyCalendar = wiz.model("portal/works/struct/my_calendar")

def load():
    data = Dashboard.load(meeting_limit=10)
    wiz.response.status(200, **data)

def my_calendar():
    user_id = wiz.session.get("id")
    year = int(wiz.request.query("year", 2026))
    month = int(wiz.request.query("month", 1))
    try:
        events = MyCalendar.searchMyEvents(user_id, year, month)
    except Exception as e:
        wiz.response.status(500, message=str(e))
    wiz.response.status(200, events=events)
