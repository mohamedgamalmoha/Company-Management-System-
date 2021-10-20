from django.shortcuts import render
from django.contrib.auth.backends import get_user_model


User = get_user_model()


def home(request):
    return render(request, 'home.html')

