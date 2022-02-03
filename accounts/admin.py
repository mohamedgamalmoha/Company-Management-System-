from django.urls import reverse
from django.utils.html import format_html
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from .models import Worker
from .utlis import permission_str
from affairs.models import Activity, Location, Month, Day, Vacations
from affairs.admin import MonthInlineAdmin, VacationsInlineAdmin


User = get_user_model()

Permission_Models = [User, Worker, Activity, Location, Month, Day]


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff')
    readonly_fields = ('last_login', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    sortable_by = ('date_of_creation',)
    ordering = ('-date_joined',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        field = super().formfield_for_manytomany(db_field, request, **kwargs)
        if db_field.name == 'user_permissions':
            content_types_ids = [ContentType.objects.get_for_model(permission).id for permission in Permission_Models]
            queryset = Permission.objects.filter(content_type__pk__in=content_types_ids)
            field._set_choices((permission.pk, permission_str(permission)) for permission in queryset)
        return field

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'first_name', 'last_name', 'password1', 'password2')}
         ),
    )

    def get_readonly_fields(self, request, obj=None):
        return super(UserAdmin, self).get_readonly_fields(request, obj) if obj else ()


class WorkerAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'nationality', 'qid_expiration_date', 'expiration_date')
    search_fields = ('name', 'nationality', 'guarantee')
    list_filter = ('nationality',  'qid_expiration_date', 'expiration_date', 'guarantee')
    inlines = (MonthInlineAdmin, VacationsInlineAdmin)
    fieldsets = (
        (None, {'fields': ('name', )}),
        ('معلومات الاقامة', {'fields': ('nationality', ('qid', 'qid_expiration_date'), ('passport_number',
                                                                                        'expiration_date'), 'guarantee',
                                        'settlement_id')}
         ),
        ('تفاصيل العقد', {'fields':
                              ('basic_salary',
                               ('feeding_allowance', 'housing_allowance', 'transporting_allowance'))}
         ),
    )
    extra_fieldsets = ('طباعة', {'fields': ('get_all_months_details', 'get_all_vacations_details')}),
    readonly_fields = ('get_all_months_details', 'get_all_vacations_details')

    def print_dunc(self, obj):
        return format_html('<a href="javascript:window.print()">Print this page</a>')

    def get_inlines(self, request, obj):
        return super().get_inlines(request, obj) if obj else ()

    def get_readonly_fields(self, request, obj=None):
        return super().get_readonly_fields(request, obj) if obj else ()

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        all_fieldsets = list(fieldsets[:])
        all_fieldsets.extend(self.extra_fieldsets)
        return all_fieldsets if obj else fieldsets

    def get_all_months_details(self, obj):
        if not Month.objects.filter(worker=obj).exists():
            return format_html(f'<input type="submit" disabled value="تنزيل الملف"')
        view_name = "affairs:get_all_months_details"
        link = reverse(view_name, args=[obj.pk])
        html = f'<input type="button" onclick="location.href=\'{link}\'"value = "تنزيل الملف" / > '
        return format_html(html)

    get_all_months_details.short_description = 'تقرير شامل للمرتبات في كل الشهور '

    def get_all_vacations_details(self, obj):
        if not Vacations.objects.filter(worker=obj).exists():
            return format_html(f'<input type="submit" disabled value="تنزيل الملف"')
        view_name = "affairs:get_all_vacations_details"
        link = reverse(view_name, args=[obj.pk])
        html = f'<input type="button" onclick="location.href=\'{link}\'"value = "تنزيل الملف" / > '
        return format_html(html)

    get_all_vacations_details.short_description = 'تقرير شامل للاجازات  غي كل الشهور'


# admin.site.unregister(Group)
# admin.site.register(Worker, WorkerAdmin)
# admin.site.register(User, CustomUserAdmin)
