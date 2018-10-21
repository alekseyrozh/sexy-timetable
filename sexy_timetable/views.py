from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from sexy_timetable.forms import UserForm


def index(request):
    return redirect(reverse('signup'))


class UserFormView(View):
    form_class = UserForm
    template_name = 'django_registration/register_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            raw_password = form.cleaned_data['password']

            user.set_password(raw_password)
            user.save()

            user = authenticate(username=username, password=raw_password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse("signup_success"))

        return render(request, self.template_name, {'form': form})


@login_required
def signup_success(request):
    user = request.user
    logout(request)
    return render(request, 'django_registration/subscribed.html',
                  {'user': user})


# @login_required
# def unsubscribe(request):
#     # TODO: redirect properly
#     return render(request, 'registration/subscribed.html',
#                   {'user': request.user})

