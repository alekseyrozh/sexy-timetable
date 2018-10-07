from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.views import View

from sexy_timetable.forms import UserForm
from .models import Greeting


# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    # TODO: proper index
                    # TODO: redirect properly
    return render(request, 'index.html')


class UserFormView(View):
    form_class = UserForm
    template_name = 'registration/registration.html'

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
    return render(request, 'registration/subscribed.html',
                  {'user': request.user})


@login_required
def unsubscribe(request):
    return render(request, 'registration/subscribed.html',
                  {'user': request.user})
