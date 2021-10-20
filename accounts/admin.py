from django.urls import reverse
from django.utils.html import format_html
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from affairs.admin import MonthInlineAdmin, VacationsInlineAdmin


User = get_user_model()


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'get_name', 'is_staff')
    readonly_fields = ('password', 'last_login', 'date_joined', 'get_all_months_details', 'get_all_vacations_details')
    extra_fieldsets = (
        ('تفاصيل الاقامة',
         {'fields': ('nationality', 'passport_number', 'expiration_date')}),
        ('تفاصيل العقد',
         {'fields': ('basic_salary', ('feeding_allowance', 'housing_allowance', 'transporting_allowance'))}),
        ('تقارير',
         {'fields': ('get_all_months_details', 'get_all_vacations_details')})
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    inlines = (MonthInlineAdmin, VacationsInlineAdmin)
    sortable_by = ('date_of_creation', )
    ordering = ('-date_joined', )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    add_fieldsets = (
        (None, {
            'fields': ('username', 'first_name', 'last_name', 'password1', 'password2')}
         ),
    )

    def get_all_months_details(self, obj):
        view_name = "affairs:get_all_months_details"
        link = reverse(view_name, args=[obj.pk])
        html = f'<input type="button" onclick="location.href=\'{link}\'"value = "تنزيل الملف" / > '
        return format_html(html)
    get_all_months_details.short_description = 'تقرير شامل للمرتبات في كل الشهور '

    def get_all_vacations_details(self, obj):
        view_name = "affairs:get_all_vacations_details"
        link = reverse(view_name, args=[obj.pk])
        html = f'<input type="button" onclick="location.href=\'{link}\'"value = "تنزيل الملف" / > '
        return format_html(html)
    get_all_vacations_details.short_description = 'تقرير شامل للاجازات  غي كل الشهور'

    def get_fieldsets(self, request, obj=None):
        a = list(super(CustomUserAdmin, self).get_fieldsets(request, obj))
        if obj:
            a.extend(list(self.extra_fieldsets))
        return tuple(a)

    def get_inlines(self, request, obj):
        return super(CustomUserAdmin, self).get_inlines(request, obj) if obj else []

    def get_readonly_fields(self, request, obj=None):
        return super(UserAdmin, self).get_readonly_fields(request, obj) if obj else []

    def get_name(self, obj):
        return obj.get_full_name() or 'لا يوجد'
    get_name.short_description = 'الاسم'


admin.site.register(User, CustomUserAdmin)
