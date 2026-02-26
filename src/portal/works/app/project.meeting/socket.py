def _auth(wiz):
    """세션 인증 확인"""
    try:
        wiz.session = wiz.model("portal/season/session").use()
        if not wiz.session.has("id"):
            return False
        return True
    except:
        return False

class Controller:
    def __init__(self, server):
        self.server = server

    def connect(self):
        pass

    def join(self, wiz, data, io):
        meeting_id = data['meeting_id']
        if not _auth(wiz):
            return
        io.join(meeting_id)

    def leave(self, data, io):
        meeting_id = data['meeting_id']
        io.leave(meeting_id)

    def disconnect(self, flask, io):
        pass
