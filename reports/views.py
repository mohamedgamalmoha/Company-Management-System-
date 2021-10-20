from django.db.models import Q
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.contrib.auth.backends import get_user_model

from affairs.models import Month, Day, Vacations
from affairs.utils import MONTHS_NAMES, get_range_months
from .csv import cls_to_func_csv_action
from .reports import OverallResidenceReport, SingleMonthReport, OverallVacationReport
from .forms import SalaryRangeMonthReportForm, LocationReportForm, ResidenceReportForm

User = get_user_model()


class BaseListViewReport(ListView):
    form_class = None

    def get_form_class(self):
        return self.form_class

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class()

    def get_form_queryset(self, form, queryset):
        raise NotImplemented

    def get_queryset(self):
        queryset = super().get_queryset()
        form = self.form_class(self.request.GET)
        if form.is_valid():
            return self.get_form_queryset(form, queryset)
        return queryset

    def get_context_data(self, **kwargs):
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return super().get_context_data(**kwargs)


class ExtendBaseListViewReport(BaseListViewReport):
    model = User
    queryset = model.objects.filter(is_superuser=False)
    context_object_name = 'objects'
    template_name = 'admin/accounts/change_list_new.html'


class SalaryRangeMonthView(ExtendBaseListViewReport):
    form_class = SalaryRangeMonthReportForm
    extra_context = {
        'header': 'تقارير المرتبات'
    }

    def get_form_queryset(self, form, queryset):
        month_start = form.cleaned_data['month_start']
        month_end = form.cleaned_data['month_end']
        if month_start not in MONTHS_NAMES or month_end not in MONTHS_NAMES:
            return queryset
        months_lst = get_range_months(month_start, month_end)
        return queryset.filter(
            user_months__month__in=months_lst
        )


class LocationReportView(ExtendBaseListViewReport):
    form_class = LocationReportForm
    extra_context = {
        'header': 'تقارير المواقع'
    }

    def get_form_queryset(self, form, queryset):
        month = form.cleaned_data['month']
        location = form.cleaned_data['location']
        if month not in MONTHS_NAMES:
            return queryset
        return queryset.filter(
            Q(user_months__month=month) &
            Q(user_months__months__location__name=location)
        )


class ResidenceReportView(ExtendBaseListViewReport):
    form_class = ResidenceReportForm
    extra_context = {
        'header': 'تقارير الاقامة'
    }

    def get_form_queryset(self, form, queryset):
        return queryset.filter(
            Q(expiration_date__gte=form.cleaned_data['date_start']) &
            Q(expiration_date__lse=form.cleaned_data['date_end'])
        )


def get_all_months_details(request, user_id):
    user = get_object_or_404(User, id=user_id)
    months = Month.objects.filter(user=user)
    return cls_to_func_csv_action(User, csv_queryset=months, csv_class=OverallResidenceReport)


def get_single_month_attendance_details(request, month_id):
    month = get_object_or_404(Month, id=month_id)
    return cls_to_func_csv_action(Month, csv_queryset=month, csv_class=SingleMonthReport)


def get_all_vacations_details(request, user_id):
    user = get_object_or_404(User, id=user_id)
    queryset = Vacations.objects.filter(user=user)
    return cls_to_func_csv_action(Month, csv_queryset=queryset, csv_class=OverallVacationReport)
