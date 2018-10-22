import asyncio
import os

from PIL import Image
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from sexy_timetable.forms import UserForm
from pyppeteer import launch
import uuid


USERNAME = "zcabzbo"
PASSWORD = "021997Mno5"


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
    get_timetable()
    user = request.user
    # logout(request)
    return render(request, 'django_registration/subscribed.html',
                  {'user': user})


def get_timetable():
    filename = create_screenshot()
    return retrieve(filename)


def retrieve(filename):
    timetable = Image.open(filename)
    os.remove(filename)
    return timetable


def create_screenshot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    to_return = loop.run_until_complete(main())
    loop.close()
    return to_return


async def main():
    browser = await launch(options={'args': ['--no-sandbox', '--disable-setuid-sandbox']})
    page = await browser.newPage()
    await page.setViewport({'width':1000, 'height':1700})
    dimensions = await page.evaluate('''() => {
        return {
            width: document.documentElement.clientWidth,
            height: document.documentElement.clientHeight,
            deviceScaleFactor: window.devicePixelRatio,
        }
    }''')
    await page.goto('https://timetable.ucl.ac.uk/tt/homePage.do')
    # await page.click()
    # element = await page.querySelector("a:contains(\'Log in\')")
    # const
    # linkHandlers = await page.$x();
    await page.waitForXPath("//a[contains(text(), 'Log in')]")
    loginBtn = (await page.xpath("//a[contains(text(), 'Log in')]"))[0]
    await loginBtn.click()

    # await page.waitForNavigation()
    await page.waitForSelector('#username')
    await page.type('#username', USERNAME)
    await page.type('#password', PASSWORD)
    loginBtn = (await page.xpath("//button[contains(text(), 'Login')]"))[0]
    await loginBtn.click()

    await page.waitForSelector("#btnCurrentWeek")
    await page.click("#btnCurrentWeek")

    await page.waitForSelector("#btnNextWeek")
    await page.click("#btnNextWeek")

    name = str(uuid.uuid4()) + ".png"
    await page.screenshot({'path': name, 'fullPage': True})

    # >>> {'width': 800, 'height': 600, 'deviceScaleFactor': 1}
    await browser.close()

    return name
# @login_required
# def unsubscribe(request):
#     # TODO: redirect properly
#     return render(request, 'registration/subscribed.html',
#                   {'user': request.user})

