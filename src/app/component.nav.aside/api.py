Dashboard = wiz.model("portal/works/struct/dashboard")

def my_projects():
    projects = Dashboard.my_projects()
    wiz.response.status(200, projects)

