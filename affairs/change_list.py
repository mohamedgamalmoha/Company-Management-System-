from django.contrib.admin.views.main import ChangeList


class BaseChangeList(ChangeList):
    list_title: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = self.list_title


class MonthChangeList(BaseChangeList):
    list_title = 'الحضور الشهري للعامل'
