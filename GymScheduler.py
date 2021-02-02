from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import schedule
from inspect import currentframe, getframeinfo
import traceback



from time import sleep
import random
import hashlib
import os
import concurrent.futures



DAYS = [{"day" : "Monday"}, {"day" : "Tuesday"}, {"day" : "Wednesday"}, {"day" : "Thursday"}, {"day" : "Friday"}, {"day" : "Saturday"}, {"day" : "Sunday"}]
TIMES = {
    1: ["8:30 AM - 9:30 AM", "08:30"],
    2: ["10:00 AM - 11:00 AM", "10:00"],
    3: ["11:30 AM - 12:30 PM", "11:30"],
    4: ["1:00 PM - 2:00 PM", "13:00"],
    5: ["2:30 PM - 3:30 PM", "14:30"],
    6: ["4:00 PM - 5:00 PM", "16:00"],
    7: ["5:30 PM - 6:30 PM", "17:30"],
}

WTIMES = {
    1: ["9:30 AM - 10:30 AM", "09:30"],
    2: ["11:00 AM - 12:00 PM", "11:00"],
    3: ["12:30 PM - 1:30 PM", "12:30"],
    4: ["2:00 PM - 3:00 PM", "14:00"],
    5: ["3:30 PM - 4:30 PM", "15:30"],
}

URL = "https://my.campusrec.uci.edu/Program/GetProducts?classification=74a158bc-9073-4039-b45d-b4c1749b7736"

USERNAME = ""#"lvernian" #"avernian"
PASSWORD = ""#"TheGnarIsComing01UCI" #"bde*99Av"

def main():
    global USERNAME, PASSWORD
    schedule = []
    found = False
    print(f"\n\n{'- '*30}\nWelcome to the official UCI Campus Recreation Gym Scheduler!\nPress control+c to quit at any time.\n{'- '*30}\n\n")

    for i in range(7):
        f = input(f"Do you want to workout {DAYS[i]['day']}? (Y/N): ").lower()
        if (f == "y") or (f == "yes") or (f == "yea"):
            while True:
                try:
                    if i >= 5:
                        time = int(input(f"\nWhat time do you want to workout {DAYS[i]['day']}?\nSelect the NUMBER associated with your preferred time:\n 1) {WTIMES[1][0]}\n 2) {WTIMES[2][0]}\n 3) {WTIMES[3][0]}\n 4) {WTIMES[4][0]}\n 5) {WTIMES[5][0]}\n\n"))
                    else:
                        time = int(input(f"\nWhat time do you want to workout {DAYS[i]['day']}?\nSelect the NUMBER associated with your preferred time:\n 1) 8:30am - 9:30am\n 2) 10:00am - 11:00am\n 3) 11:30am - 12:30pm\n 4) 1:00pm - 2:00pm\n 5) 2:30pm - 3:30pm\n 6) 4:00pm - 5:00pm\n 7) 5:30pm - 6:30pm\n\n"))
                    if ( (i >= 5) and ((time < 1) or (time > 5)))  or ((time < 1) or (time > 7)):
                        print("\n")
                    else:
                        found = True
                        DAYS[i]["time"] = time
                        break
                except:
                    print("\n")


    if found:
        printSchedule()
        USERNAME = input("\nEnter your UCI username: ")
        PASSWORD = input("\nEnter your UCI password: ")
        print("\n\nScheduling workouts .. .. ..\n\n")

        #Sync so that the function is called at second :00
        sleep(60 - datetime.now().second)
        scheduleScrape()
    else:
        print("\nNothing to schedule.\n")


def printSchedule():
    found = False
    for i, elem in enumerate(DAYS):
        if not elem.get("time"):
            continue

        if i >= 5:
            print(f"\n{elem['day']} @ {WTIMES[elem['time']][0]}")
        else:
            print(f"\n{elem['day']} @ {TIMES[elem['time']][0]}")
        found = True

    return found



def scheduleScrape():
    #schedule at second :10
    sleep(1)
    #print(datetime.now().second)
    for i, elem in enumerate(DAYS):
        if not elem.get("time"):
            continue

        #Schedule
        if i == 0:
            schedule.every().sunday.at(TIMES[elem["time"]][1]).do(scrape, i, TIMES[elem["time"]][0])
        elif i == 1:
            schedule.every().monday.at(TIMES[elem["time"]][1]).do(scrape, i, TIMES[elem["time"]][0])
        elif i == 2:
            schedule.every().tuesday.at(TIMES[elem["time"]][1]).do(scrape, i, TIMES[elem["time"]][0])
        elif i == 3:
            schedule.every().wednesday.at(TIMES[elem["time"]][1]).do(scrape, i, TIMES[elem["time"]][0])
        elif i == 4:
            schedule.every().thursday.at(TIMES[elem["time"]][1]).do(scrape, i, TIMES[elem["time"]][0])
        elif i == 5:
            schedule.every().friday.at(WTIMES[elem["time"]][1]).do(scrape, i, WTIMES[elem["time"]][0])
        elif i == 6:
            schedule.every().saturday.at(WTIMES[elem["time"]][1]).do(scrape, i, WTIMES[elem["time"]][0])


    while True:
        schedule.run_pending()
        time.sleep(10)  # wait

def scrape(dayIndex, dayTime, headless=True):
    global USERNAME, PASSWORD
    browser = None
    try:
        opts = Options()
        opts.add_argument("--disable-extensions")
        if headless:
            opts.add_argument("--headless")
        prefs = {'profile.managed_default_content_settings.images': 2}
        opts.add_experimental_option('prefs', prefs)
        opts.add_argument("--window-size=1500,1000")

        # Find random user agent and set add to browser options
        #opts.add_argument("user-agent=" + AGENTS[random.randint(1, 3400)])
        # Instantiate new browser
        browser = webdriver.Chrome(options=opts, executable_path='./chromedriver')



        browser.get(URL)
        sleep(3)

        #print(getframeinfo(currentframe()).lineno)
        #Click on the day
        browser.find_elements_by_class_name("list-group-item")[dayIndex].click()
        sleep(3)

        slotAvailable = False
        #Iterate through available times
        for availability in browser.find_elements_by_class_name("caption"):
            if dayTime in availability.find_element_by_class_name("program-schedule-card-header").text:
                #Case this is the time user wants to schedule
                slotAvailable = True
                # click on register
                availability.find_element_by_class_name("btn").click()
                sleep(1)

                # click on log in with UCI Net ID
                actions = ActionChains(browser)
                actions.send_keys((Keys.TAB * 2) + Keys.ENTER)
                actions.perform()

                sleep(3)

                # enter username and password and hit enter
                actions = ActionChains(browser)
                actions.send_keys(USERNAME + Keys.TAB + PASSWORD + Keys.TAB + Keys.ENTER)
                actions.perform()

                sleep(3)

                break

        #print(getframeinfo(currentframe()).lineno)
        #Logged in, time to hit register again
        # Iterate through available times
        for availability in browser.find_elements_by_class_name("caption"):
            if dayTime in availability.find_element_by_class_name("program-schedule-card-header").text:
                slotAvailable = True
                # Case this is the time user wants to schedule
                # click on register
                availability.find_element_by_class_name("btn").click()
                sleep(3)
                break

        if not slotAvailable:
            print(f"\n\n- - - - - - - - - -\nUnable to schedule {DAYS[dayIndex]['day']} @ {dayTime}, time slot does not exist.\n- - - - - - - - - -\n\n")

        #print(getframeinfo(currentframe()).lineno)
        switches = browser.find_elements_by_class_name("radio-inline")
        #print(getframeinfo(currentframe()).lineno)

        switches[0].click() #Y
        #switches[1].click() #N
        #switches[2].click() #Y
        switches[3].click() #N
        #switches[4].click() #Y
        switches[5].click() #N
        #switches[6].click() #Y
        switches[7].click() #N

        #print(getframeinfo(currentframe()).lineno)

        # Click on Add to Cart
        clicked = False
        for container in browser.find_elements_by_class_name("container-fluid"):
            for button in container.find_elements_by_class_name("btn"):
                if "Add" in button.text:
                    button.click()
                    sleep(3)
                    clicked = True
                    break
            if clicked:
                break

        #print(getframeinfo(currentframe()).lineno)

        # Click on checkout
        browser.find_element_by_id("checkoutButton").click()
        sleep(1)
        #print(getframeinfo(currentframe()).lineno)

        # click on checkout again
        actions = ActionChains(browser)
        actions.send_keys((Keys.TAB * 3) + Keys.ENTER)
        actions.perform()

        sleep(5)

        print(f"\n\n{'- '*30}\nSuccessfully scheduled {DAYS[dayIndex]['day']} @ {dayTime}!\n{'- '*30}\n\n")
        browser.close()
    except Exception as e:
        print(traceback.format_exc())
        print(e)
        print(f"\n\n{'- '*30}\nUnable to schedule {DAYS[dayIndex]['day']} @ {dayTime}.\n{'- '*30}\n\n")
        if browser:
            browser.close()



def test():
    opts = Options()
    opts.add_argument("--disable-extensions")
    #opts.add_argument("--headless")
    prefs = {'profile.managed_default_content_settings.images': 2}
    opts.add_experimental_option('prefs', prefs)
    opts.add_argument("--window-size=1280,720")

    # Find random user agent and set add to browser options
    # opts.add_argument("user-agent=" + AGENTS[random.randint(1, 3400)])
    # Instantiate new browser
    browser = webdriver.Chrome(options=opts, executable_path='./chromedriver')

    browser.get("https://www.google.com")
    sleep(5)

    browser.close()

if __name__ == "__main__":
    # main()
    scrape(6, "2:00 PM - 3:00 PM", True)
    #test()
