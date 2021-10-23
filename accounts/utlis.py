
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
