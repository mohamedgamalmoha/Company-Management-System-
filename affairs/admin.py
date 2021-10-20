from django.urls import reverse
from django.contrib import admin
from django.utils.html import format_html

from .models import Activity, Location, Month, Day, Vacations


class VacationsInlineAdmin(admin.TabularInline):
    model = Vacations
    extra = 2
    readonly_fields = ('get_duration', )

    def get_duration(self, obj):
        if obj.start_date and obj.end_date:
            return obj.duration_in_days
        return 0
    get_duration.short_description = 'عدد ايام الاجازة'


class DayInlineAdmin(admin.TabularInline):
    model = Day
    extra = 0
    max_num = 31
    readonly_fields = ('day_number', )

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class MonthInlineAdmin(admin.TabularInline):
    model = Month
    max_num = 31
    can_delete = False
    fields = ('user', 'activity', 'month', 'get_detail_link_view', 'get_month_details')
    readonly_fields = ('get_detail_link_view', 'get_month_details')

    def get_extra(self, request, obj=None, **kwargs):
        return 0 if obj.user_months.all().exists() else 1

    def get_detail_link_view(self, obj):
        view_name = f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change"
        link = reverse(view_name, args=[obj.pk])
        html = f'<input type="button" onclick="location.href=\'{link}\'"value = "تفاصيل" / > '
        return format_html(html)
    get_detail_link_view.short_description = 'المزيد من التفاصيل'

    def get_month_details(self, obj):
        print(obj)
        if not obj or not obj.pk:
            return '--'
        view_name = "affairs:single_month_attendance_details"
        link = reverse(view_name, args=[obj.pk])
        html = f'<input type="button" onclick="location.href=\'{link}\'"value = "تنزيل الملف" / > '
        return format_html(html)
    get_month_details.short_description = 'تنزيل التقرير لهذا الشهر'


class MonthAdmin(admin.ModelAdmin):
    exclude = ('year', )
    inlines = (DayInlineAdmin, )
    fieldsets = (
        ('المعلومات الاساسية',
         {'fields': ('user', 'activity', 'month')}
         ),
        ('الاحوال المالية',
         {'fields': ('basic_salary',
                     ('feeding_allowance', 'housing_allowance', 'transporting_allowance', 'get_total_allowance'),
                     ('total_extra_work_hours', 'total_extra_work_hours_money'),
                     ('total_deduction', 'total_rewards', 'total_loans'),
                     ('total_absence_hours', 'total_absence_deduction'),
                     ('total_salary', 'total_salary_deduction', 'net_salary'),
                     )}
         ),
    )
    readonly_fields = ('basic_salary', 'feeding_allowance', 'housing_allowance', 'transporting_allowance', 'total_loans',
                       'total_extra_work_hours', 'total_deduction', 'total_rewards', 'total_extra_work_hours_money',
                       'get_total_allowance', 'total_absence_hours', 'total_absence_deduction', 'total_salary',
                       'total_salary_deduction', 'net_salary')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Activity)
admin.site.register(Location)
admin.site.register(Month, MonthAdmin)
