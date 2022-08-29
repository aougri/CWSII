import datetime
import time

import pywhatkit


def sendMessage(message):
    now = datetime.datetime.now()

    pywhatkit.sendwhatmsg("+1(727)296-7027", message, now.hour, now.minute + 2, 15, True, 5)
    print("\n Sent! \n")
    
