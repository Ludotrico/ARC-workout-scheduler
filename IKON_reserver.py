from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from datetime import datetime
import schedule
from inspect import currentframe, getframeinfo
import traceback

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

from time import sleep
from sys import exit
import random
import hashlib
import os
import concurrent.futures
from tkinter import *
from tkcalendar import *

os.environ["TK_SILENCE_DEPRECATION"] = "1"




USERNAME = None
PASSWORD = None
RESORT = None #"brighton"
DAY = None #"Wed Dec 23 2020"

DAY_OBJ = None


WEEKDAY = {

    0: {"abbr": "Mon", "full": "Monday"},
    1: {"abbr": "Tue", "full": "Tuesday"},
    2: {"abbr": "Wed", "full": "Wednesday"},
    3: {"abbr": "Thu", "full": "Thursday"},
    4: {"abbr": "Fri", "full": "Friday"},
    5: {"abbr": "Sat", "full": "Saturday"},
    6: {"abbr": "Sun", "full": "Sunday"},

}
MONTH = {
    1: {"abbr": "Jan", "full": "January"},
    2: {"abbr": "Feb", "full": "February"},
    3: {"abbr": "Mar", "full": "March"},
    4: {"abbr": "Apr", "full": "April"},
    5: {"abbr": "May", "full": "May"},
    6: {"abbr": "Jun", "full": "June"},
    7: {"abbr": "Jul", "full": "July"},
    8: {"abbr": "Aug", "full": "August"},
    9: {"abbr": "Sep", "full": "September"},
    10: {"abbr": "Oct", "full": "October"},
    11: {"abbr": "Nov", "full": "November"},
    12: {"abbr": "Dec", "full": "December"},
}

RESORTS = {
    1: "Arapahoe Basin",
    2: "Aspen Mountain", #FP
    3: "Aspen Highands", #FP
    4: "Snowmass", #FP
    5: "Buttermilk", #FP
    6: "Big Sky",
    7: "Brighton",
    8: "Crystal Mountain",
    9: "Jackson Hole Mountain Resort", #FP
    10: "Loon Mountain",
    11: "Lake Louise", #FP
    12: "Taos",
    13: "The Summit at Snoqualmie",
    14: "Windham Mountain",
    15: "Winter Park",
}





def main():
    global USERNAME, PASSWORD, RESORT, DAY, DAY_OBJ
    print(f"\n\n{'- '*30}\nWelcome to the official IKON Pass Reserver!\nPress control+c to quit at any time.\n{'- '*30}\n\n")

    resortNum = int(input(f"\nWhich mountain resort would you like to make a reservation in?\n 1) Arapahoe Basin Ski Area, CO\n 2) Aspen Mountain, CO\n 3) Aspen Highands, CO\n 4) Snowmass, CO\n 5) Buttermilk, CO\n 6) Big Sky Resort, MT\n 7) Brighton, UT\n 8) Crystal Mountain, WA\n 9) Jackson Hole Mountain Resort, WY\n 10) Loon Mountain, NH\n 11) Lake Louise, AB\n 12) Taos Ski Valley, NM\n 13) The Summit at Snoqualmie, WA\n 14) Windham Mountain, NY\n 15) Winter Park, CO\nSelect the NUMBER associated with your preferred time: "))
    RESORT = RESORTS[resortNum]

    print("\nSelect the day you want to reserve in the date picker window to continue.\n")

    root = Tk()
    root.title("IKON Pass Reservation")
    root.geometry("600x400")

    now = datetime.now()
    cal = Calendar(root, select_mode="day", year=now.year, month=now.month, day=now.day)
    cal.pack(pady=20, fill="both", expand=True)

    lbl = Label(root, text="Confirm date ↓")
    lbl.pack(pady=0)

    def dateConfirmed():
        global USERNAME, PASSWORD, RESORT, DAY, DAY_OBJ

        sDate = cal.get_date()
        month = int(sDate[:sDate.find('/')])
        sDate = sDate[sDate.find('/')+1:]

        day = int(sDate[:sDate.find('/')])
        sDate = sDate[sDate.find('/') + 1:]

        year = int(f"20{sDate}")



        date = datetime(day=day, month=month, year=year)
        DAY = f"{WEEKDAY[date.weekday()]['abbr']} {MONTH[date.month]['abbr']} {date.day if (date.day > 10) else '0' + str(date.day)} {date.year}"

        DAY_OBJ = date


        root.destroy()

        print(f"Selected: {DAY}\n")
        makeReservation()

    btn = Button(root, text="Confirm date", command=dateConfirmed)
    btn.pack(pady=20)
    root.mainloop()


def makeReservation():
    global USERNAME, PASSWORD, RESORT, DAY, DAY_OBJ

    USERNAME = input("Enter your email: ")
    PASSWORD = input("Enter your pasword: ")

    print(f"\n\nReseravation: {RESORT} on {DAY}.\nWill make reservation as soon as a spot opens up...\n\n")

    while True:

        opts = Options()
        opts.add_argument("--disable-extensions")
        opts.add_argument("--headless")
        prefs = {'profile.managed_default_content_settings.images': 2}
        opts.add_experimental_option('prefs', prefs)
        opts.add_argument("--window-size=1200,1000")

        # Find random user agent and set add to browser options
        # opts.add_argument("user-agent=" + AGENTS[random.randint(1, 3400)])
        # Instantiate new browser
        browser = webdriver.Chrome(options=opts, executable_path='./chromedriver')

        browser.get("https://account.ikonpass.com/en/login")
        sleep(3)


        # LOGIN
        actions = ActionChains(browser)
        actions.send_keys((Keys.TAB * 22) + USERNAME + (Keys.TAB) + PASSWORD + (Keys.ENTER))
        actions.perform()

        sleep(3)

        try:
            browser.find_elements_by_class_name("sc-AxjAm")[0].click()
            sleep(3)
        except Exception as e:
            print("Email or password incorrect! Restarting program.\n\n")
            break

        actions = ActionChains(browser)
        actions.send_keys((Keys.TAB * 2) + RESORT)
        actions.perform()

        try:
            browser.find_element_by_id("react-autowhatever-resort-picker-section-0-item-0").click()
            sleep(1)
        except Exception as e:
            print(f"Resort {RESORT} not found!\nMake sure your version of the IKON pass can access {RESORT} and make sure they require reservations in the first place. Restarting program.\n\n")
            break


        continues = browser.find_elements_by_class_name("sc-qQLmQ")
        for c in continues:
            c.find_element_by_class_name("sc-AxjAm").click()
        sleep(3)

        while (browser.find_element_by_class_name("goPjwB").text.lower() != f"{MONTH[DAY_OBJ.month]['full'].lower()} {DAY_OBJ.year}"):
            browser.find_element_by_class_name("iiFRwl").find_elements_by_class_name("eaiGnt")[1].click()

        days = browser.find_elements_by_class_name("DayPicker-Day")
        for day in days:
            try:
                if day.get_attribute("aria-label") == DAY:
                    day.click()
                    break
            except:
                browser.close()
                continue

        sleep(2)

        try:
            if browser.find_element_by_class_name("sc-pdihw").text == "NO RESERVATIONS AVAILABLE":
                browser.close()
                sleep(10)
                continue
        except:
            #Reservation available
            browser.find_element_by_class_name("sc-pCOsa").find_element_by_class_name("sc-AxjAm").click()
            sleep(3)
            browser.find_element_by_class_name("sc-qWPci").find_element_by_class_name("sc-AxgMl").click()
            sleep(3)
            browser.find_element_by_class_name("input").click()
            sleep(1)
            browser.find_element_by_class_name("sc-qQkIG").find_element_by_class_name("sc-AxgMl").click()
            sleep(3)
            browser.close()
            print(f"SUCCESS! You have now reserved {RESORT} on {DAY}. Goodbye and happy shredding!\n\n")
            exit(1)

    browser.close()
    main()




if __name__ == "__main__":
    main()
