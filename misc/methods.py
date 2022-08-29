import re


def findCity(location):
    city = re.match(r".+?(?=,[^.])", location)
    city = city.group(0).strip()
    city = city.lower()
    city = city.title()
    return city


def searchforword(filename, str):
    file = open(filename, "r")
    print(f"\n searching for {str} in {filename}")
    if str in file.read():
        return True
    else:
        return False


def dataentry(filename, str):
    f = open(filename, "a")
    f.write(str + "\n")
    print(f"\n Added {str} to file")
