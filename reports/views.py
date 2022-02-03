from django.views.generic import TemplateView, DetailView


from .utils import is_valid_choice
from .base_views import BaseSearchList, BaseWorkerReportView
from .forms import MultiWorkerForm, AccommodationFrom, SingleMonthForm, LocationForm
from accounts.models import Worker
from accounts.decorators import AdminAuthMixIn
from affairs.models import Month, Day, Location


class MultiWorkerReportView(AdminAuthMixIn, BaseWorkerReportView):
    form_class = MultiWorkerForm
    template_name = 'reports/multi_worker.html'

    def get_queryset(self):
        queryset = super(MultiWorkerReportView, self).get_queryset()
        activity = self.request.user.activity
        if activity:
            queryset = queryset.filter(activity=activity)
        return queryset

    def get_worker_queryset(self, form,  queryset):
        workers = form.cleaned_data.get('workers')
        if workers:
            queryset = queryset.filter(worker__in=workers)
        return queryset

    def get_form_queryset(self, form, queryset):
        queryset = super(MultiWorkerReportView, self).get_form_queryset(form, queryset)
        activity = form.cleaned_data.get('activity')
        if activity:
            queryset = queryset.filter(activity=activity)
        return queryset


class MultiWorkerReportPrintView(AdminAuthMixIn, TemplateView):
    template_name = 'reports/new_multi_worker_print.html'

    def get_context_data(self, **kwarg):
        context = super().get_context_data(**kwarg)
        ids = self.request.GET.getlist('ids', [])
        if len(ids) and ids[0].startswith(','):
            ids = ids[0][1:].split(',')
        context.update({
            'months': Month.objects.filter(id__in=ids).order_by('worker__name', 'month', 'year').distinct(),
            'locations':  Location.objects.values().order_by('id')
        })
        return context


class SingleMonthReportView(AdminAuthMixIn, BaseSearchList):
    model = Month
    form_class = SingleMonthForm
    context_object_name = 'months'
    template_name = 'reports/single_month.html'

    def get_form_queryset(self, form, queryset):
        worker = form.cleaned_data.get('worker')
        month = form.cleaned_data.get('month')
        year = form.cleaned_data.get('year')
        if not worker:
            return queryset
        queryset = queryset.filter(worker=worker)
        if is_valid_choice(str(month) if month is not None else None):
            queryset = queryset.filter(month=month)
        if is_valid_choice(str(year) if year is not None else None):
            queryset = queryset.filter(year=year)
        return queryset

    def get_queryset(self):
        queryset = super(SingleMonthReportView, self).get_queryset()
        activity = self.request.user.activity
        if activity:
            queryset = queryset.filter(activity=activity)
        return queryset


class SingleMonthReportPrintView(AdminAuthMixIn, DetailView):
    model = Month
    context_object_name = 'month'
    template_name = 'reports/single_month_report.html'

    def get_context_data(self, **kwargs):
        context = super(SingleMonthReportPrintView, self).get_context_data(**kwargs)
        context['days'] = Day.objects.filter(month=self.get_object())
        return context


class AccommodationReportView(AdminAuthMixIn, BaseSearchList):
    model = Worker
    form_class = AccommodationFrom
    context_object_name = 'workers'
    template_name = 'reports/accommodation.html'
    ordering = ('expiration_date', 'qid_expiration_date')

    def get_form_queryset(self, form, queryset):
        expiration_date = form.cleaned_data.get('expiration_date')
        qid_expiration_date = form.cleaned_data.get('qid_expiration_date')
        if is_valid_choice(str(expiration_date) if expiration_date is not None else None):
            queryset = queryset.filter(expiration_date__lte=expiration_date)
        if is_valid_choice(str(qid_expiration_date) if qid_expiration_date is not None else None):
            queryset = queryset.filter(qid_expiration_date__lte=qid_expiration_date)
        return queryset


class LocationReportView(AdminAuthMixIn, BaseSearchList):
    model = Month
    form_class = LocationForm
    context_object_name = 'months'
    template_name = 'reports/location_report.html'

    def get_form_queryset(self, form,  queryset):
        location = form.cleaned_data.get('location')
        month = form.cleaned_data.get('month')
        year = form.cleaned_data.get('year')
        if location:
            queryset = queryset.filter(months__location=location)
        if is_valid_choice(str(month) if month is not None else None):
            queryset = queryset.filter(month=month)
        if is_valid_choice(str(year) if year is not None else None):
            queryset.filter(year=year)
        return queryset

    def get_queryset(self):
        queryset = super(LocationReportView, self).get_queryset()
        activity = self.request.user.activity
        if activity:
            queryset = queryset.filter(activity=activity)
        return queryset
