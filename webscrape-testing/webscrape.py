from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
my_url = 'https://u.demog.berkeley.edu/~andrew/1918/figure2.html'
#my_url = 'https://en.wikipedia.org/wiki/Special:AllPages'
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")
rows = page_soup.findAll("tr")
filename = "lifespans.csv"
f = open(filename, "w")

for i, row in enumerate(rows):
    if i < 3:
        continue
    current = row.findAll("p")
    for index, item in enumerate(current):
        if index != 2:
            f.write(item.text + ",")
        else:
            f.write(item.text)
    f.write("\n")

f.close()
