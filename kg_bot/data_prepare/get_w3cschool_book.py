# -*- coding: utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
import codecs

base_url = "https://www.w3cschool.cn"
aim_url = "/software_testing/software_testing-scap37us.html"
f = codecs.open("./w3cschool_data/text.txt","a","utf-8")

while aim_url:
    url = base_url + aim_url
    data = urlopen(url).read().decode('utf-8')
    # print(data)
    soup = BeautifulSoup(data,"lxml")
    contents = soup.find_all("div",{"class":"content-intro"})
    for c in contents:
        f.write(c.get_text())
        print(c.get_text())
    next = soup.find("div",{"class":"next-link"})
    if next:
        aim_url = next.find("a")['href']
    else:
        aim_url = None

f.close()