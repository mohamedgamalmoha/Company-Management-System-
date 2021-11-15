from django.contrib.auth.models import Permission
from django.contrib.auth.backends import get_user_model
from django.contrib.contenttypes.models import ContentType

from .models import Worker
from affairs.models import Activity, Location, Month, Day, Vacations


User = get_user_model()
Permission_Models = [User, Worker, Activity, Location, Month, Day]


def permission_str(perm):
    name = perm.name
    new_name = name
    str_content = str(perm.content_type)
    first_index = str(perm.content_type).find("|") + 1
    if name.startswith('Can view'):
        new_name = 'باستطاعته رؤية'
    elif name.startswith('Can add'):
        new_name = 'باستطاعته اضافة'
    elif name.startswith('Can delete'):
        new_name = 'باستطاعته مسح'
    elif name.startswith('Can change'):
        new_name = 'باستطاعته تغير'
    new_name += str_content[first_index:]
    return new_name


def get_permissions_labels():
    content_types_ids = [ContentType.objects.get_for_model(permission).id for permission in Permission_Models]
    queryset = Permission.objects.filter(content_type__pk__in=content_types_ids)
    return ((permission.pk, permission_str(permission)) for permission in queryset)
