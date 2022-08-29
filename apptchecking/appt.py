from apscheduler.schedulers.background import BlockingScheduler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import apptchecking.apptdb as db

sched = BlockingScheduler()

# Options for the driver to launch in headless mode
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=options)


def logon():
    print("Logging in to the appt page...", end="\n")
    driver.get("https://vendor.choicehomewarranty.com/index.php?sec=cadsappt")
    driver.find_element_by_name("email").send_keys("Hvac5218@gmail.com")
    driver.find_element_by_name("password").send_keys("bradkin525")
    driver.find_element_by_name("Submit").click()
    driver.find_element_by_link_text("- Appointments").click()


def redirection():
    driver.find_element_by_link_text("- Appointments").click()


def apptRowNum():
    apptcount = driver.find_elements_by_xpath(
        '//*[@id="wrap"]/div[3]/div/div/div/div[2]/table/tbody/tr'
    )
    if len(apptcount) == 2:
        print("There are no appointments at the moment, quitting... \n")
        driver.quit()
    elif len(apptcount) > 2:
        print(f"There are {len(apptcount) - 2} appointments")
        return len(apptcount)


def countRows():
    rows = driver.find_elements_by_xpath(
        '//*[@id="wrap"]/div[3]/div/div/div/div[2]/table/tbody/tr'
    )
    print(len(rows))


def updateDatabase():
    print("Updating database...", end="\n")
    rowcontent = apptRowNum()
    for i in range(3, rowcontent + 1):
        currentSWO = getSWO(i)
        currentSys = getSys(i)
        currentLocation = getLocation(i)
        currentDate = getDate(i)
        db.addappt(currentSWO, currentSys, currentLocation, currentDate)

    print("Database updated")


def printAllAppts():
    rowcount = apptRowNum()
    print("\n=======================APPTS========================")
    for i in range(3, rowcount + 1):
        currentSWO = driver.find_element_by_xpath(
            f'//*[@id="wrap"]/div[3]/div/div/div/div[2]/table/tbody/tr[{i}]/td[1]'
        ).text
        currentSys = driver.find_element_by_xpath(
            f'//*[@id="wrap"]/div[3]/div/div/div/div[2]/table/tbody/tr[{i}]/td[2]'
        ).text
        currentLocation = driver.find_element_by_xpath(
            f'//*[@id="wrap"]/div[3]/div/div/div/div[2]/table/tbody/tr[{i}]/td[3]'
        ).text
        currentDate = driver.find_element_by_xpath(
            f'//*[@id="wrap"]/div[3]/div/div/div/div[2]/table/tbody/tr[{i}]/td[4]'
        ).text
        print(
            f"SWO: {currentSWO} | System: {currentSys} | Location: {currentLocation} | Date: {currentDate}"
        )

    print("\n====================================================")


def getSWO(i):
    return driver.find_element_by_xpath(
        f'//*[@id="wrap"]/div[3]/div/div/div/div[2]/table/tbody/tr[{i}]/td[1]'
    ).text


def getSys(i):
    return driver.find_element_by_xpath(
        f'//*[@id="wrap"]/div[3]/div/div/div/div[2]/table/tbody/tr[{i}]/td[2]'
    ).text


def getLocation(i):
    return driver.find_element_by_xpath(
        f'//*[@id="wrap"]/div[3]/div/div/div/div[2]/table/tbody/tr[{i}]/td[3]'
    ).text


def getDate(i):
    return driver.find_element_by_xpath(
        f'//*[@id="wrap"]/div[3]/div/div/div/div[2]/table/tbody/tr[{i}]/td[4]'
    ).text


# function to see if the total count of appointments in the database is greater than 4 and if so, return true, otherwise return false
def checkApptCount():
    count = db.countappts()
    if db.countappts() > 4:
        print(f"There are {count} appointments")
        return True
    else:
        print(f"There are {4 - count} appointments left to take")
        return False


def checkAppt():
    logon()
    db.createappttable()

    apptRowNum()
    printAllAppts()
    updateDatabase()

    countRows()


# todo: make this the 1st condition as if this has 4 appts the oprogram stops and exits
checkAppt()

sched.add_job(checkAppt, "interval", seconds=600)
sched.start()
