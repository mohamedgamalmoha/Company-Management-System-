from django.urls import reverse_lazy
from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.backends import get_user_model
from django.contrib.messages.views import SuccessMessageMixin

from .decorators import ajax_get_required
from accounts.decorators import AdminAuthMixIn
from reports.utils import is_valid_choice
from reports.base_views import BaseSearchList
from .models import Month, Location, Activity, Vacations, Day
from .forms import (MonthCreationForm, MonthUpdateForm, ActivityCreationForm, LocationCreationForm, DayUpdateForm,
                    VacationsCreationForm, MonthListFrom, ActivityListForm, LocationListForm, VacationsListForm,
                    MonthDaysInlineFormset)


User = get_user_model()


def home(request):
    return render(request, 'home.html')


class MonthCreationView(SuccessMessageMixin, CreateView, AdminAuthMixIn):
    model = Month
    form_class = MonthCreationForm
    template_name = 'affairs/creation/month.html'
    success_message = 'تم ادخال البيانات بطريقة صحيحة'
    extra_context = {'title': 'انشاء شهر جديد'}

    def form_valid(self, form):
        month = form.save()
        location = form.cleaned_data.get('location')
        Day.objects.filter(month=month).update(location=location)
        return redirect(reverse('affairs:month_day_inline', kwargs={'pk': month.pk}))


class MonthDetailView(UpdateView, AdminAuthMixIn):
    model = Month
    form_class = MonthUpdateForm
    template_name = 'affairs/update/month.html'
    extra_context = {'title': 'تعديل الشهر'}
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['days'] = Day.objects.filter(month=self.get_object())
        return context


class MonthDayInlineView(SuccessMessageMixin, SingleObjectMixin, FormView, AdminAuthMixIn):
    model = Month
    form_class = MonthDaysInlineFormset
    template_name = 'affairs/update/month_day_inline.html'
    success_message = 'تم التعديل بنجاح'
    extra_context = {
        'title': 'تسجيل الحضور'
    }
    context_object_name = 'month'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=self.model.objects.all())
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=self.model.objects.all())
        return super().get(request, *args, **kwargs)

    def get_form(self, form_class=None):
        return self.form_class(**self.get_form_kwargs(), instance=self.object)

    def get_context_data(self, **kwargs):
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse('affairs:single_month_report_print', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())


class MonthListView(BaseSearchList):
    model = Month
    form_class = MonthListFrom
    context_object_name = 'months'
    template_name = 'affairs/list/month.html'
    extra_context = {
        'title': 'الشهر'
    }

    def get_form_queryset(self, form, queryset):
        worker = form.cleaned_data.get('worker')
        activity = form.cleaned_data.get('activity')
        month = form.cleaned_data.get('month')
        year = form.cleaned_data.get('year')
        if worker:
            queryset = queryset.filter(worker=worker)
        if activity:
            queryset = queryset.filter(activity=activity)
        if is_valid_choice(month):
            queryset = queryset.filter(month=month)
        if is_valid_choice(year):
            queryset = queryset.filter(year=year)
        return queryset


class ActivityCreationView(SuccessMessageMixin, CreateView):
    form_class = ActivityCreationForm
    template_name = 'affairs/creation/base.html'
    success_message = 'تم ادخال البيانات بطريقة صحيحة'
    extra_context = {'title': 'انشاء نشاط  جديد'}

    def form_valid(self, form):
        activity = form.save()
        return redirect(reverse('affairs:activity_detail', kwargs={'pk': activity.pk}))


class ActivityDetailView(UpdateView):
    model = Activity
    form_class = ActivityCreationForm
    template_name = 'affairs/update/base.html'
    extra_context = {'title': 'تعديل النشاط'}
    success_url = '/'


class ActivityDeleteView(DeleteView, SuccessMessageMixin):
    model = Activity
    template_name = 'affairs/delete/activity.html'
    success_message = 'تم الحذف بنجاح'
    success_url = reverse_lazy("affairs:activity_list")
    extra_context = {'title': 'جذف نشاط'}


class ActivityListView(BaseSearchList):
    model = Activity
    form_class = ActivityListForm
    context_object_name = 'activities'
    template_name = 'affairs/list/activity.html'
    extra_context = {
        'title': 'النشاطات'
    }

    def get_form_queryset(self, form, queryset):
        name = form.cleaned_data.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class LocationCreationView(SuccessMessageMixin, CreateView):
    form_class = LocationCreationForm
    template_name = 'affairs/creation/base.html'
    success_message = 'تم ادخال البيانات بطريقة صحيحة'
    extra_context = {'title': 'انشاء  موقع جديد'}

    def form_valid(self, form):
        location = form.save()
        return redirect(reverse('affairs:location_detail', kwargs={'pk': location.pk}))


class LocationDeleteView(DeleteView, SuccessMessageMixin):
    model = Location
    template_name = 'affairs/delete/location.html'
    success_message = 'تم الحذف بنجاح'
    success_url = reverse_lazy('affairs:location_list')
    extra_context = {'title': 'حذف الموقع'}


class LocationDetailView(UpdateView):
    model = Location
    form_class = LocationCreationForm
    template_name = 'affairs/update/base.html'
    extra_context = {'title': 'تعديل الموقع'}
    success_url = '/'


class LocationListView(BaseSearchList):
    model = Location
    form_class = LocationListForm
    context_object_name = 'locations'
    template_name = 'affairs/list/location.html'
    extra_context = {
        'title': 'المواقع'
    }

    def get_form_queryset(self, form, queryset):
        name = form.cleaned_data.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class VacationsCreationView(SuccessMessageMixin, CreateView):
    form_class = VacationsCreationForm
    template_name = 'affairs/creation/base.html'
    success_message = 'تم ادخال البيانات بطريقة صحيحة'
    extra_context = {'title': 'انشاء اجازة جديدة'}

    def form_valid(self, form):
        vacations = form.save()
        return redirect(reverse('affairs:vacations_detail', kwargs={'pk': vacations.pk}))


class VacationsDetailView(UpdateView):
    model = Vacations
    form_class = VacationsCreationForm
    template_name = 'accounts/update/user.html'
    extra_context = {'title': 'تعديل اجازة '}
    success_url = '/'


class VacationsListView(BaseSearchList):
    model = Vacations
    form_class = VacationsListForm
    context_object_name = 'vacations'
    template_name = 'affairs/list/vacations.html'
    extra_context = {
        'title': 'الاجازات'
    }

    def get_form_queryset(self, form, queryset):
        worker = form.cleaned_data.get('worker')
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        if worker:
            queryset = queryset.filter(worker=worker)
        if start_date:
            queryset = queryset.filter(start_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(start_date__lte=end_date)
        return queryset


@ajax_get_required
def validate_month_uniqueness(request):
    worker_id = request.GET.get('worker_id')
    month = request.GET.get('month')
    year = request.GET.get('year')
    _month = Month.objects.filter(worker__id=worker_id, month=month, year=year)
    if _month.exists():
        return JsonResponse({
            'month_id': _month.first().id,
            'is_existed': True
        })
    return JsonResponse({'is_existed': False})
