import season
import datetime

class Struct:
    def __init__(self):
        self.orm = wiz.model("portal/season/orm")
        self.config = wiz.model("portal/works/config")
        self._Project = wiz.model("portal/works/struct/project")

    def db(self, name):
        return self.orm.use(name, module="works")

    @property
    def project(self):
        """Project Aggregate Root 클래스 반환 (호출마다 동일 클래스)"""
        return self._Project

Model = Struct()
