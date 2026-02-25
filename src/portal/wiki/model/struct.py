import season
import datetime

class Struct:
    def __init__(self):
        self.orm = wiz.model("portal/season/orm")
        self.config = wiz.model("portal/wiki/config")
        self._Book = wiz.model("portal/wiki/struct/book")

    def db(self, name):
        return self.orm.use(name, module="wiki")

    @property
    def book(self):
        """Book Aggregate Root 클래스 반환"""
        return self._Book

Model = Struct()
