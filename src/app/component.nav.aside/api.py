Dashboard = wiz.model("portal/works/struct/dashboard")

def my_projects():
    projects = Dashboard.my_projects()
    wiz.response.status(200, projects)

def profile_image():
    user_id = wiz.session.get("id")
    if not user_id:
        wiz.response.status(200, image=None)
    orm = wiz.model("portal/season/orm")
    db = orm.use("user")
    try:
        user = db.get(id=user_id, fields="profile_image")
    except Exception:
        wiz.response.status(200, image=None)
    img = user.get("profile_image") if user else None
    if img and len(str(img)) < 10:
        img = None
    wiz.response.status(200, image=img)
