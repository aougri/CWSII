from types import NoneType
from apscheduler.schedulers.background import BlockingScheduler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Options for the driver to launch in headless mode
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

# create a new Chrome session
print("Starting program...", end="\n")
driver = webdriver.Chrome(options=options)


def login():
    print_logo()
    print("Logging in...", end="\n")
    driver.get("https://vendor.choicehomewarranty.com/index.php?sec=cadsavail")
    driver.find_element("name","email").send_keys("Hvac5218@gmail.com")
    driver.find_element("name","password").send_keys("bradkin525")
    driver.find_element("name","Submit").click()
    

def rowCount():
    rows = driver.find_elements("xpath",'//*[@id="availOrders"]/tbody/tr')
    if len(rows):
        print("There are no job listings at the moment, quitting... \n")
        driver.quit()

    else:
        return rows


def count():
    rowCount = rowCount()