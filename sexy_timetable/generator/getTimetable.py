import os

from selenium import webdriver
import asyncio
from pyppeteer import launch
import uuid
from PIL import Image


USERNAME = "zcabzbo"
PASSWORD = "021997Mno5"

"""
# open browser
driver = webdriver.Chrome()
driver.set_window_size(800, 3000)
driver.get("https://timetable.ucl.ac.uk/tt/homePage.do")

# open log in page
login_button = driver.find_element_by_link_text("Log in")
login_button.click()

# enter log in credentials
username_field = driver.find_element_by_id("username")
password_field = driver.find_element_by_id("password")

username_field.send_keys(USERNAME)
password_field.send_keys(PASSWORD)

login_button = driver.find_element_by_name("_eventId_proceed")
login_button.click()

current_week_button = driver.find_element_by_id("btnCurrentWeek")
current_week_button.click()


# make screenshot
# screenshot = driver.save_screenshot('my_screenshot.png')

# driver.implicitly_wait(10000)
# driver.close()
"""


def get_timetable():
    filename = create_screenshot()
    return retrieve(filename)


def retrieve(filename):
    timetable = Image.open(filename)
    os.remove(filename)
    return timetable


def create_screenshot():
    return asyncio.get_event_loop().run_until_complete(main())


async def main():
    browser = await launch()
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