import season

class Controller(wiz.controller("base")):
    def __init__(self):
        super().__init__()
        
        if wiz.session.has("id") == False:
            wiz.response.status(401)

