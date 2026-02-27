Dashboard = wiz.model("portal/works/struct/dashboard")

def load():
    data = Dashboard.load(meeting_limit=10)
    wiz.response.status(200, **data)
