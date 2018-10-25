import asyncio
import os

import pyppeteer
from PIL import Image
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from sexy_timetable.generator.main import generate_cool_timetable
from sexy_timetable.forms import UserForm
from pyppeteer import launch
import uuid

from sexy_timetable.mail_try import send_pic

# from sexy_timetable.generator.main import generate_cool_timetable

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

            if not can_log_in(username, raw_password):
                return render(request, 'django_registration/cant_login.html',
                              {'user': user})

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

    # get_timetable()
    # logout(request)

    return render(request, 'django_registration/subscribed.html',
                  {'user': request.user})


@login_required
def send_timetable(request):
    screenshot = get_timetable("zczlozh", "Ranpot12!Ranpot12!")
    # cool_timetable = generate_cool_timetable(screenshot)
    cool_timetable = generate_cool_timetable(screenshot)
    send_pic(request.user, cool_timetable)
    return redirect(reverse("signup_success"))


def get_timetable(username, password):
    filename = create_screenshot(username, password)
    return retrieve(filename)


def retrieve(filename):
    timetable = Image.open(filename)
    os.remove(filename)
    return timetable


def create_screenshot(username, password):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    to_return = loop.run_until_complete(main(username, password))
    loop.close()
    return to_return


async def main(username, password):
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


def can_log_in(username, password):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    to_return = loop.run_until_complete(try_loggin_in(username, password))
    loop.close()
    return to_return


# noinspection PyCompatibility
async def try_loggin_in(username, password):
    browser = await launch(options={'args': ['--no-sandbox', '--disable-setuid-sandbox']})
    page = await browser.newPage()

    await page.setViewport({'width': 1000, 'height': 1700})
    dimensions = await page.evaluate('''() => {
            return {
                width: document.documentElement.clientWidth,
                height: document.documentElement.clientHeight,
                deviceScaleFactor: window.devicePixelRatio,
            }
        }''')

    try:
        await page.goto('https://timetable.ucl.ac.uk/tt/homePage.do')

        await page.waitForXPath("//a[contains(text(), 'Log in')]")
        loginBtn = (await page.xpath("//a[contains(text(), 'Log in')]"))[0]

        await page.waitFor(1000)
        await loginBtn.click()
        #
        # await page.waitFor(1000)
        # await loginBtn.click()

        await page.waitFor(1000)
        await page.type('#username', username)
        await page.type('#password', password)
        loginBtn = (await page.xpath("//button[contains(text(), 'Login')]"))[0]

        await page.waitFor(1000)
        await loginBtn.click()

        # await page.waitFor(1000)
        # await loginBtn.click()

        # if logged in - can click click btnCurrentWeek
        # else - will time out

        found = await page.waitForSelector("#btnCurrentWeek, #password")

        if found._remoteObject['description'] == 'span#btnCurrentWeek':
            # success
            return True
        else:
            # failure
            # description is 'input#password'
            return False

    except pyppeteer.errors.TimeoutError:
        return False
    finally:
        try:
            await browser.close()
        except:
            pass




# @login_required
# def unsubscribe(request):
#     # TODO: redirect properly
#     return render(request, 'registration/subscribed.html',
#                   {'user': request.user})

