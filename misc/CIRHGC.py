import time

from apscheduler.schedulers.background import BlockingScheduler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import methods
import whatsappScript

acceptableCities = [
    "Lakeland",
    "Ruskin",
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




def print_logo():
    print("""
    
    
                                                           _____                   _____                    _____          
                                                          /\    \                 /\    \                  /\    \         
                                                         /::\    \               /::\____\                /::\    \        
                                                        /::::\    \             /:::/    /               /::::\    \       
                                                       /::::::\    \           /:::/   _/___            /::::::\    \      
                                                      /:::/\:::\    \         /:::/   /\    \          /:::/\:::\    \     
                                                     /:::/  \:::\    \       /:::/   /::\____\        /:::/__\:::\    \    
                                                    /:::/    \:::\    \     /:::/   /:::/    /        \:::\   \:::\    \   
                                                   /:::/    / \:::\    \   /:::/   /:::/   _/___    ___\:::\   \:::\    \  
                                                  /:::/    /   \:::\    \ /:::/___/:::/   /\    \  /\   \:::\   \:::\    \ 
                                                 /:::/____/     \:::\____\:::|   /:::/   /::\____\/::\   \:::\   \:::\____\
                                                 \ :::\    \      \::/    /:::|__/:::/   /:::/    /\:::\   \:::\   \::/    /
                                                  \:::\    \      \/____/ \:::\/:::/   /:::/    /  \:::\   \:::\   \/____/ 
                                                   \:::\    \              \::::::/   /:::/    /    \:::\   \:::\    \     
                                                    \:::\    \              \::::/___/:::/    /      \:::\   \:::\____\    
                                                     \:::\    \              \:::\__/:::/    /        \:::\  /:::/    /    
                                                      \:::\    \              \::::::::/    /          \:::\/:::/    /     
                                                       \:::\    \              \::::::/    /            \::::::/    /      
                                                        \:::\____\              \::::/    /              \::::/    /       
                                                         \::/    /               \::/____/                \::/    /        
                                                          \/____/                 ~~                       \/____/         
                                                                                                                           

    
    
    
     """)



def login():
    print_logo()
    print("Logging in...", end="\n")
    driver.get("https://vendor.choicehomewarranty.com/index.php?sec=cadsavail")
    driver.find_element_by_name("email").send_keys("Hvac5218@gmail.com")
    driver.find_element_by_name("password").send_keys("bradkin525")
    driver.find_element_by_name("Submit").click()
    time.sleep(5)


def windowSwitch(windowIndex):
    print("Switching windows...", end="\n")
    window = driver.window_handles[windowIndex]
    driver.switch_to.window(window)
    print(driver.window_handles[windowIndex])


def rowCount():
    rows = driver.find_elements_by_xpath('//*[@id="availOrders"]/tbody/tr')
    if len(rows) == 0:
        print("There are no job listings at the moment, quitting... \n")
        driver.quit()

    else:
        return rows


def getSWO(i):
    swo = driver.find_element_by_xpath(
        f'//*[@id="availOrders"]/tbody/tr[{i}]/td[1]'
    ).text
    return swo


def getJobType(i):
    job_type = driver.find_element_by_xpath(
        f'//*[@id="availOrders"]/tbody/tr[{i}]/td[2]'
    ).text
    return job_type


def getLocation(i):
    location = driver.find_element_by_xpath(
        f'//*[@id="availOrders"]/tbody/tr[{i}]/td[3]'
    ).text
    return location


def count():    
    rows = rowCount()

    for i in range(1, len(rows)):
        swo = getSWO(i)
        job = getJobType(i)
        fulllocation = getLocation(i)
        location = methods.findCity(fulllocation)
        if job in acceptableJobTypes and location not in acceptableCities:
            print(f"{job} => OK || {location} => NO")
        elif job not in acceptableJobTypes and location in acceptableCities:
            print(f"{job} => NO || {location} => OK")
        elif job in acceptableJobTypes and location in acceptableCities:
            print(f"{job} => OK || {location} = OK     <======= FOUND A JOB")
            res = methods.searchforword("/home/ahmed/sideproj/CWS-main/cws2_0/misc/joblist.txt", swo)
            if res == False:

                print("Found a job at: " + fulllocation)
                driver.find_element_by_xpath(
                    f'//*[@id="availOrders"]/tbody/tr[{i}]/td[4]/a'
                ).click()
                driver.find_element_by_class_name("accept").click()
                windowSwitch(1)
                # Send the whatsapp message
                whatsappScript.sendMessage(
                    "Job found at "
                    + fulllocation
                    + "! "
                    + "Accept at: \n"
                    + driver.current_url
                )
                methods.dataentry("/home/ahmed/sideproj/CWS-main/cws2_0/misc/joblist.txt", swo)
                windowSwitch(0)
                driver.refresh()
                driver.get(
                    "https://vendor.choicehomewarranty.com/index.php?sec=cadsavail"
                )

                time.sleep(600)
                continue
            else:
                print("Job already in file , skipping... ==> " + location)
                continue
        else:
            print(f"{job} => NO || {location} => NO")


def redirect():
    windowSwitch(0)
    driver.get("https://vendor.choicehomewarranty.com/index.php?sec=cadsavail")


login()
def main():
    redirect()
    count()


main()
sched.add_job(main, "interval", seconds=600)

sched.start()

