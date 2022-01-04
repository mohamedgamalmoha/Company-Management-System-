from django.db.models import Q
from django.views.generic import ListView

from affairs.models import Month
from .utils import start_end_date_prepare
from affairs.utils import get_range_months_lte_index, get_range_months_gte_index


class BaseSearchList(ListView):
    form_class = None
    extra_context = {}
    initial = {}
    prefix = None
    ordering = None

    def get_initial(self):
        return self.initial.copy()

    def get_prefix(self):
        return self.prefix

    def get_form_kwargs(self):
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
        }
        if self.request.method == 'GET':
            kwargs.update({
                'data': self.request.GET,
            })
        return kwargs

    def get_form_class(self):
        return self.form_class

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs())

    def get_form_queryset(self, form, queryset):
        return queryset.filter(**form.fields)

    def get_queryset(self):
        queryset = super().get_queryset()

        form = self.get_form()
        if form.is_valid():
            queryset = self.get_form_queryset(form, queryset)

        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        if 'form' not in kwargs:
            kwargs.update({'form': self.get_form()})
        return super().get_context_data(**kwargs)


class BaseWorkerReportView(BaseSearchList):
    model = Month
    form_class = None
    context_object_name = 'months'
    ordering = ('-year', 'month')

    def get_worker_queryset(self, form,  queryset):
        return queryset

    def get_form_queryset(self, form, queryset):
        queryset = self.get_worker_queryset(form, queryset)

        location = form.cleaned_data.get('location')

        start_date_month = self.request.GET.get('start_date_month')
        start_date_year = self.request.GET.get('start_date_year')
        end_date_month = self.request.GET.get('end_date_month')
        end_date_year = self.request.GET.get('end_date_year')

        if location:
            queryset = queryset.filter(months__location=location)

        if not all([start_date_month, start_date_year, end_date_month, end_date_year]):
            return queryset

        year_start_date, month_start_date, year_end_date, month_end_date = start_end_date_prepare(
           start_date_year, start_date_month, end_date_year, end_date_month
        )

        months_start_date_lst = list(get_range_months_gte_index(month_start_date))
        months_end_date_lst = list(get_range_months_lte_index(month_end_date))

        return queryset.filter(
            (Q(year=year_start_date) & Q(month__in=months_start_date_lst)) |
            (Q(year__gt=year_start_date) & Q(year__lt=year_end_date)) |
            (Q(year=year_end_date) & Q(month__in=months_end_date_lst))
        )
