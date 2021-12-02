from django.db.models import Q
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView
from django.contrib.auth import login
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.backends import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin

from .models import Worker
from .decorators import AdminAuthMixIn
from affairs.models import Month, Vacations
from reports.base_views import BaseSearchList
from .forms import RegistrationForm, UserCreationForm, UserUpdateForm, WorkerCreationForm, WorkerListForm, UserListForm


User = get_user_model()


class LogInView(SuccessMessageMixin, LoginView):
    template_name = 'accounts/auth/login.html'
    success_url = reverse_lazy('affairs:home')
    redirect_authenticated_user = True
    success_message = 'تم نسجيل الدخول'


class RegistrationView(SuccessMessageMixin, CreateView):
    form_class = RegistrationForm
    template_name = 'accounts/auth/registration.html'
    success_message = 'تم ادخال البيانات بطريقة صحيحة'
    success_url = reverse_lazy('affairs:home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return HttpResponseRedirect(self.success_url)


class LogOutView(SuccessMessageMixin, LogoutView):
    template_name = 'accounts/auth/logout.html'
    success_message = 'تم نسجيل الخروج'
    success_url = reverse_lazy('affairs:home')


class UserCreationView(SuccessMessageMixin, CreateView, AdminAuthMixIn):
    form_class = UserCreationForm
    template_name = 'accounts/creation/user.html'
    success_message = 'تم ادخال البيانات بطريقة صحيحة'
    extra_context = {'title': 'انشاء مستخدم جديد'}

    def get_success_url(self):
        return self.object.get_absolute_url()


class UserDetailView(UpdateView, AdminAuthMixIn):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/update/user.html'
    extra_context = {'title': 'تعديل موظف'}
    success_url = '/'


class UserChangePasswordView(SuccessMessageMixin, UpdateView):
    model = User
    form_class = SetPasswordForm
    template_name = 'accounts/update/user_change_password.html'
    success_message = 'تم ادخال البيانات بطريقة صحيحة'
    extra_context = {'title': 'تغير كلمة السر'}
    success_url = reverse_lazy('affairs:home')

    def get_form_kwargs(self):
        kwargs = {
            'prefix': self.get_prefix(),
            'initial': self.get_initial(),
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        kwargs.update({'user': self.object})
        return kwargs


class UserListView(BaseSearchList, AdminAuthMixIn):
    model = User
    form_class = UserListForm
    template_name = 'accounts/list/user.html'
    context_object_name = 'users'
    extra_context = {'title': 'موظف'}

    def get_form_queryset(self, form, queryset):
        name = form.cleaned_data.get('name')
        if not name or name.strip() == '':
            return queryset
        return queryset.filter(
            Q(firstname__icontains=name) | Q(lastname__icontains=name)
        )


class WorkerCreationView(SuccessMessageMixin, CreateView, AdminAuthMixIn):
    form_class = WorkerCreationForm
    template_name = 'accounts/creation/worker.html'
    success_message = 'تم ادخال البيانات بطريقة صحيحة'
    extra_context = {'title': 'اضافة عامل جديد'}

    def get_success_url(self):
        return self.object.get_absolute_url()


class WorkerDetailView(UpdateView, AdminAuthMixIn):
    model = Worker
    form_class = WorkerCreationForm
    template_name = 'accounts/update/worker.html'
    extra_context = {'title': 'تعديل عامل'}
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(WorkerDetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        context['vacations'] = Vacations.objects.filter(worker=obj)

        activity = self.request.user.activity
        if activity:
            context['months'] = Month.objects.filter(worker=obj, activity=activity)
        else:
            context['months'] = Month.objects.filter(worker=obj)
        return context


class WorkerListView(BaseSearchList, AdminAuthMixIn):
    model = Worker
    form_class = WorkerListForm
    template_name = 'accounts/list/worker.html'
    context_object_name = 'workers'
    extra_context = {'title': 'عمال'}

    def get_form_queryset(self, form, queryset):
        name = form.cleaned_data.get('name')
        if not name or name.strip() == '':
            return queryset
        return queryset.filter(name__icontains=name)

