import datetime
from dateutil.relativedelta import relativedelta
from settings.settings import Settings
import sqlite3

settings = Settings()
print(settings.DATABASE_PATH)

connection = conn = sqlite3.connect(settings.DATABASE_PATH)
db_cursor = connection.cursor()

#db_curso#r.execute('''CREATE TABLE settings
#             (name text, dob date, max_hr INTEGER)''')

db_cursor.execute("INSERT INTO settings VALUES ('Paul','1987-06-26', 198)")


connection.commit()

for row in db_cursor.execute('SELECT * FROM settings'):
        print(row)