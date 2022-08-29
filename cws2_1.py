# all imports
import time

from apscheduler.schedulers.background import BlockingScheduler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import db.db as db
import methods
import whatsappScript

acceptableCities = [
    "Lakeland",
    "Winter Haven",
    "Auburndale",
    "Plant City",
    "Seffner",
    "Valrico",
    "Brandon",
    "Mango",
    "Fish Hawk",
    "Riverview",
    "Gibsonton",
    "Tampa",
    "Temple Terrace",
    "Clearwater",
    "Dunedin",
    "Belleair",
    "Belleair Bluffs",
    "Largo",
    "Indian Rocks Beach",
    "Indian Shores",
    "Seminole",
    "Oldsmar",
    "Feather Sound",
    "Gandy",
    "Pinellas Park",
    "Lealman",
    "St. Petersburg",
    "Saint Petersburg",
    "Bardmoor",
    "Treasure Islands",
    "Gulfport",
    "Historic Old Northeast",
    "Tierra Verde",
    "Greater Pinellas Point",
    "Gandy",
    "Palm Harbor",
    "Tarpon Springs",
    "Winston",
    "Crystal Lake",
    "Lithia",
    "The Villages",
]
acceptableJobTypes = ["Air Conditioning"]
sched = BlockingScheduler()

# Options for the driver to launch in headless mode
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

# create a new Chrome session
print("Starting program...", end="\n")
driver = webdriver.Chrome(options=options)


# all functions for the task

# Goes through all the process in logging in
def login():
    print("Logging in...", end="\n")
    driver.get("https://vendor.choicehomewarranty.com/index.php?sec=cadsavail")
    driver.find_element_by_name("email").send_keys("Hvac5218@gmail.com")
    driver.find_element_by_name("password").send_keys("bradkin525")
    driver.find_element_by_name("Submit").click()
    time.sleep(10)


# Function to switch between windows
def windowSwitch(windowIndex):
    print("Switching windows...", end="\n")
    window = driver.window_handles[windowIndex]
    driver.switch_to.window(window)


# todo function to check if the appt has less than 4


# Function to count the rows in the table
def rowCount():
    rows = driver.find_elements_by_xpath('//*[@id="availOrders"]/tbody/tr')
    if len(rows) == 0:
        print("There are no job listings at the moment, quitting... \n")
        driver.quit()

    else:
        return len(rows)


def getSWO(i):
    print("Getting SWO...", end="\n")
    swo = driver.find_element_by_xpath(
        f'//*[@id="availOrders"]/tbody/tr[{i}]/td[1]'
    ).text
    return swo


def getJobType(i):
    print("Getting job type...", end="\n")
    job_type = driver.find_element_by_xpath(
        f'//*[@id="availOrders"]/tbody/tr[{i}]/td[2]'
    ).text
    return job_type


def getLocation(i):
    print("Getting location...", end="\n")
    location = driver.find_element_by_xpath(
        f'//*[@id="availOrders"]/tbody/tr[{i}]/td[3]'
    ).text
    return location


def printAllCities():
    rows = rowCount()
    print("\n=======================CITIES========================")
    for i in range(1, rows + 1):
        curr_row_content = driver.find_element_by_xpath(
            f'//*[@id="availOrders"]/tbody/tr[{i}]/td[3]'
        ).text
        curr_row_jobtype = driver.find_element_by_xpath(
            f'//*[@id="availOrders"]/tbody/tr[{i}]/td[2]'
        ).text
        print(curr_row_content + " / " + curr_row_jobtype)
    print("=====================================================\n")


# Main function to act as the main loop for the task
def main():
    jobs = 0

    # Login to the website

    login()
    printAllCities()

    # Count the rows in the table
    rows = rowCount()

    while jobs < 4:
        for i in range(1, rows + 1):
            curr_row_content = driver.find_element_by_xpath(
                f'//*[@id="availOrders"]/tbody/tr[{i}]/td[2]'
            ).text
            if curr_row_content in acceptableJobTypes:
                curr_row_location = driver.find_element_by_xpath(
                    f'//*[@id="availOrders"]/tbody/tr[{i}]/td[3]'
                ).text
                city = methods.findCity(curr_row_location)
                if city not in acceptableCities:
                    print(
                        "The current city is not acceptable, skipping..."
                        + city
                        + "\n The current row is: "
                        + str(i)
                        + "\n"
                        + "Next row in 10 minutes"
                    )
                    # time.sleep(600)
                    continue
                else:

                    swo = getSWO(i)
                    job_type = getJobType(i)
                    location = getLocation(i)

                    res = db.datacheck(swo)

                    if res == None:
                        db.data_entry(swo, job_type, location)
                        print("Found a job at: " + curr_row_location)
                        driver.find_element_by_xpath(
                            f'//*[@id="availOrders"]/tbody/tr[{i}]/td[4]/a'
                        ).click()
                        driver.find_element_by_class_name("accept").click()
                        windowSwitch(1)
                        # Send the whatsapp message
                        whatsappScript.sendMessage(
                            "Job found at "
                            + curr_row_location
                            + "!"
                            + "Accept at:"
                            + driver.current_url
                        )

                        windowSwitch(0)

                        # time.sleep(600)
                    else:
                        print("Job already in database, skipping..." + location)
                        continue

        if i == rows:
            print("All jobs have been scanned, quitting...")
            driver.quit()
            break
        if jobs == 4:
            print("All the jobs have been secured, end of the program")
            driver.quit()
            break
        break


main()
