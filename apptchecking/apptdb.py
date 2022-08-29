import sqlite3

# Connect to the database
conn = sqlite3.connect("appttable.db")

# Create a cursor object
c = conn.cursor()


def createappttable():
    print("Creating appointment table...", end="\n")
    c.execute(
        "CREATE TABLE IF NOT EXISTS appttable (swo_num TEXT, job_type TEXT, location TEXT, appt_date TEXT)"
    )


def datacheck(swo_num):
    print("Checking if SWO number exists in the database...", end="\n")
    c.execute("SELECT swo_num FROM appttable where swo_num = (?)", (swo_num,))
    res = c.fetchone()
    return res


def addappt(SWO_num, job_type, location, appt_date):
    res = datacheck(SWO_num)
    if res is None:
        print(
            "SWO number not found in the database, adding to the database...", end="\n"
        )
        c.execute(
            "INSERT INTO appttable VALUES (?, ?, ?, ?)",
            (SWO_num, job_type, location, appt_date),
        )
        print(
            "The appointment with the SWO: "
            + SWO_num
            + " and "
            + job_type
            + " in "
            + location
            + " scheduled at "
            + location
            + "==> database",
            end="\n",
        )
        conn.commit()
    else:
        print("SWO number already exists in the database", end="\n")


def countappts():
    c.execute("SELECT COUNT(*) FROM appttable")
    res = c.fetchone()
    return res[0]


createappttable()
