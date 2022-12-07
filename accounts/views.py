from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages

from .forms import CustomUserCreationForm, NotificationsForm


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

    if request.method == 'POST':
        form = NotificationsForm(request.POST)
        if form.is_valid():
            user.notification_event_digest = form.cleaned_data['event_switch']
            user.notification_group_digest = form.cleaned_data['group_switch']
            user.notification_post_replies = form.cleaned_data['reply_switch']
            user.save()

            messages.success(request, "Notification preferences updated")
        else:
            messages.error(request, "Error updating preferences %s" % form.errors)
    else:
        form = NotificationsForm(initial={
            'event_switch': user.notification_event_digest,
            'group_switch': user.notification_group_digest,
            'reply_switch': user.notification_post_replies
            }
        )

    context = {
        'snav': 'notifications',
        'user': user,
        'form': form,
    }
    return render(request, 'settings/notifications.html', context)