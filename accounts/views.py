from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


@login_required
def account_details(request):
    user = request.user

    context = {
        'snav': 'account',
        'user': user,
    }
    return render(request, 'settings/account_details.html', context)


@login_required
def notifications(request):
    user = request.user

    context = {
        'snav': 'notifications',
        'user': user,
    }
    return render(request, 'settings/notifications.html', context)