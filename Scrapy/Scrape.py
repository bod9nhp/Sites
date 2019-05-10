import urllib3
from urllib.request import urlopen
import sqlite3
from bs4 import BeautifulSoup

http = urllib3.PoolManager()
url = 'http://quotes.toscrape.com'
r = http.request("GET", url)
conn = sqlite3.connect("Scrap")
cur = conn.cursor()

Save = open("Webs.txt", "w")
soup = BeautifulSoup(r.data, 'html.parser')
url1 = url
url2 = " "
page = 1
print(" " * 70 + "*" * 6 + "Title" + "*" * 6)
cur.execute("Delete  from authors where id !=0")
while 1 != 0:
    Save.write(str(" " * 35) + "/ \ " * 5 + "Title " + "/ \ " * 5 + "\n")
    Save.write(str(" " * 35) + "\ / " * 5 + "Page " + str(page) + "\ / " * 5 + "\n")
    http = urllib3.PoolManager()
    r = http.request("GET", url)
    soup = BeautifulSoup(r.data, 'html.parser')

    rez = soup.find_all("div", attrs={"class": "quote"})
    authors = soup.find_all("div", attrs={"class": "quote"})
    for i, quote in enumerate(rez):
        take_text = quote.find("span", attrs={'class': "text"})
        authors_text = authors[i].find("small", attrs={'class': "author"})
        print(i + 1, " )", take_text.text[1:-1], "\n", "By:", authors_text.text)
        a = Save.write(str(i + 1) + ". " + take_text.text[1:-1] + "\n" "By: " + authors_text.text + "\n")

        cur.execute("INSERT INTO authors values (null , ?)", [take_text.text[1:-1]])
        # cur.execute("Delete from authors where id=0")
        conn.commit()
    url2 = soup.find("li", attrs={"class": "next"})
    if url2 is None:
        break
    url = url1 + url2.a['href']
    page += 1

Save.close()