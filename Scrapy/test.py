import sqlite3 as lite
con = None

texts = open("Webs.txt",'r')


try:
    con = lite.connect('Scrap')
    cur = con.cursor()
    cur.execute('SELECT SQLITE_VERSION()')
    data = cur .fetchone()
    # cur.execute("INSERT INTO authors values (null , 'adsa')")
    # cur.execute("Delete  from authors where id !=0")
    # cur.execute("INSERT INTO authors values (null , ?)", [texts])
    cur.execute("SELECT authors FROM authors")
    print(cur.fetchone())

    con.commit()
    a = cur.execute("Select * from authors")
    print ("SQLite version: %s" % data)

finally:
    if con:
        con.close()
