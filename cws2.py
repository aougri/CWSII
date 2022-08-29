# ARCHIVED VERSION OF cws2.py TO GET PROUD OF THE WORKING OF THE PROGRAM


# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
#
# import methods
# import whatsappScript
#
# options = Options()
# options.add_argument("--headless")
# options.add_argument("--disable-gpu")
#
# import datetime
# import time
#
#
# def refresh():
#     print(f"[{loggingTime}] In n Out... \n")
#     driver.get("https://vendor.choicehomewarranty.com/index.php?sec=cadsavail")
#     rows = driver.find_elements_by_xpath("//*[@id='availOrders']/tbody/tr")
#     print(rows)
#     print(len(rows))
#     return rows
#
#
# def browserQuit():
#     print("Quitting browser...", end="\n")
#     driver.quit()
#
#
# now = datetime.datetime.now()
# loggingTime = now.strftime("%Y-%m-%d %H:%M")
#
# acceptableCities = [
#     "Lakeland",
#     "Winter Haven",
#     "Auburndale",
#     "Plant City",
#     "Seffner",
#     "Valrico",
#     "Brandon",
#     "Mango",
#     "Fish Hawk",
#     "Riverview",
#     "Gibsonton",
#     "Tampa",
#     "Temple Terrace",
#     "Clearwater",
#     "Dunedin",
#     "Belleair",
#     "Belleair Bluffs",
#     "Largo",
#     "Indian Rocks Beach",
#     "Indian Shores",
#     "Seminole",
#     "Oldsmar",
#     "Feather Sound",
#     "Gandy",
#     "Pinellas Park",
#     "Lealman",
#     "St. Petersburg",
#     "Bardmoor",
#     "Treasure Islands",
#     "Gulfport",
#     "Historic Old Northeast",
#     "Tierra Verde",
#     "Greater Pinellas Point",
#     "Gandy",
#     "Palm Harbor",
#     "Tarpon Springs",
#     "Winston",
#     "Crystal Lake",
#     "Lithia",
#     "The Villages",
# ]
# now = datetime.datetime.now()
# loggingTime = now.strftime("%Y-%m-%d %H:%M")
# print(f"[{loggingTime}] " + "pulling out chrome in headless mode\n")
# now = datetime.datetime.now()
# loggingTime = now.strftime("%Y-%m-%d %H:%M")
# driver = webdriver.Chrome(options=options)
# now = datetime.datetime.now()
# loggingTime = now.strftime("%Y-%m-%d %H:%M")
# print(f"[{loggingTime}] going to choice\n")
# driver.get("https://vendor.choicehomewarranty.com/index.php?sec=cadsavail")
# now = datetime.datetime.now()
# loggingTime = now.strftime("%Y-%m-%d %H:%M")
# print(f"[{loggingTime}] logging in \n")
# driver.find_element_by_name("email").send_keys("Hvac5218@gmail.com")
# driver.find_element_by_name("password").send_keys("bradkin525")
# driver.find_element_by_name("Submit").click()
#
# window = driver.window_handles[0]
# driver.switch_to.window(window)
#
# rows = refresh()
# jobs = 0
#
# currentSWOS = []
# while jobs < 4:
#     refresh()
#
#     if len(rows) == 0:
#         now = datetime.datetime.now()
#         print(
#             f"[{loggingTime}] There are no job listings at the moment, reattempting after 30 seconds\n"
#         )
#         time.sleep(600)
#         refresh()
#
#     else:
#
#         while jobs < 4:
#             for i in range(1, (len(rows) + 1)):
#                 now = datetime.datetime.now()
#                 content = driver.find_element_by_xpath(
#                     f'//*[@id="availOrders"]/tbody/tr[{i}]/td[2]'
#                 ).text
#                 if content == "Air Conditioning":
#                     location = driver.find_element_by_xpath(
#                         f'//*[@id="availOrders"]/tbody/tr[{i}]/td[3]'
#                     ).text
#                     city = methods.findCity(location)
#                     print(city)
#                     if city not in acceptableCities:
#                         now = datetime.datetime.now()
#                         print(
#                             f"[{loggingTime}]"
#                             + city
#                             + " isn't an accepted city, reattempting \n"
#                         )
#                         time.sleep(2)
#                         browserQuit()
#                         refresh()
#                         continue
#                     else:
#                         SWO = driver.find_element_by_xpath(
#                             f'//*[@id="availOrders"]/tbody/tr[{i}]/td[1]'
#                         ).text
#                         if SWO in currentSWOS:
#                             now = datetime.datetime.now()
#                             print(
#                                 f"[{loggingTime}] Already Stored and sent this job... \n"
#                             )
#                             browserQuit()
#                         else:
#                             currentSWOS.append(SWO)
#                             print(f"[{loggingTime}] Found a job at: " + city + "\n")
#                             # if the city is in the acceptableCities list, click the "See Details" link in the same row
#                             time.sleep(5)
#                             driver.find_element_by_xpath(
#                                 f'//*[@id="availOrders"]/tbody/tr[{i}]/td[4]/a'
#                             ).click()
#                             # Click on the  button which class name is Accept
#                             time.sleep(1)
#                             driver.find_element_by_class_name("accept").click()
#                             # switch to the new tab
#                             window = driver.window_handles[1]
#                             driver.switch_to.window(window)
#                             # check the first radio button with the value '1660388400_1660402800_0'
#                             time.sleep(3)
#                             print(f"[{loggingTime}] Sending the message w whatsapp \n")
#                             whatsappScript.sendMessage(
#                                 "I found a job at "
#                                 + city
#                                 + "! Accept at: "
#                                 + driver.current_url
#                             )
#
#                             jobs += 1
#                             # switch back to the first tab
#                             window = driver.window_handles[0]
#                             driver.switch_to.window(window)
#                             # go back
#                             driver.back()
#
#                             browserQuit()
#
#                             refresh()
#
#                             time.sleep(5)
#
#                             # add to the resume.txt file the city and the zipcode and the date and the Air Conditioning job
#                             with open("resume.txt", "a") as myfile:
#                                 myfile.write(
#                                     "Job at "
#                                     + city
#                                     + " from "
#                                     + "7 AM to 11 AM"
#                                     + " for Air Conditioning\n"
#                                 )
#                                 myfile.write("\n\n")
#
#                             time.sleep(600)
#                             continue
#
#                 else:
#                     continue
#
# exit(0)
