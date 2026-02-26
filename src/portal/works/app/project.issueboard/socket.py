def _auth(wiz, project_id):
    """세션 인증 + 프로젝트 접근 권한 확인"""
    try:
        wiz.session = wiz.model("portal/season/session").use()
        if not wiz.session.has("id"):
            return False
        projectModel = wiz.model("portal/works/project")
        project = projectModel.get(project_id)
        if project is None:
            return False
        project.member.accessLevel(['admin', 'manager', 'user', 'guest'])
        return True
    except:
        return False

class Controller:
    def __init__(self, server):
        self.server = server

    def connect(self):
        pass

    def join(self, wiz, data, io):
        project_id = data['project_id']
        if not _auth(wiz, project_id):
            return
        io.join(project_id)

    def leave(self, data, io):
        project_id = data['project_id']
        io.leave(project_id)

    def disconnect(self, flask, io):
        pass
