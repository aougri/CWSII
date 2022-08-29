import re


def findCity(location):
    city = re.match(r".+?(?=,[^.])", location)
    city = city.group(0).strip()
    city = city.lower()
    city = city.title()
    return city
