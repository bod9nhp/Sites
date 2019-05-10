import sqlite3
db = sqlite3("finance.db")


name = db.execute("select name from user_stocks ")
print(name)

# z = []

# for z in a:
#     z.append(a)

