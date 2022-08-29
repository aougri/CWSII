import sqlite3

# Connect to the database
conn = sqlite3.connect("cwsdb.db")

# Create a cursor object
c = conn.cursor()


# Create a table that contains SWO number, JOB type text , and location text


def datacheck(swo_num):
    print(
        "Checking if SWO number exists in the database...",
        end="\n" + " " + "||" + swo_num + "||",
    )
    c.execute("SELECT swo_num FROM cwsdb where swo_num = (?)", (swo_num,))
    res = c.fetchone()
    return res


def create_table():
    print("Creating table...", end="\n")
    c.execute(
        "CREATE TABLE IF NOT EXISTS cwsdb (swo_num TEXT, job_type TEXT, location TEXT, appt_)"
    )


def data_entry(SWO_num, job_type, location):
    res = datacheck(SWO_num)
    if res is None:
        print(
            "SWO number not found in the database, adding to the database...",
            end="\n" + " " + "||" + SWO_num + "||" + job_type + "||" + location,
        )
        c.execute("INSERT INTO cwsdb VALUES (?, ?, ?)", (SWO_num, job_type, location))
        print(
            "SWO number added to the database...",
            end="\n" + " " + "||" + SWO_num + "||" + job_type + "||" + location,
        )
        conn.commit()
    else:
        print(
            "SWO number already exists in the database",
            end="\n" + " " + "||" + SWO_num + "||" + job_type + "||" + location,
        )

        conn.close()
