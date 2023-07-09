from selenium import webdriver
import re
import time
import mysql.connector
from selenium.webdriver.common.by import By


browser=webdriver.Firefox()
browser2=webdriver.Firefox()
browser.get("put the https of the website here!")
browser2.get("put another address here!")
for i in range(0,250):
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    browser2.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(8)

elem=browser.find_element(By.XPATH,"/html")
elem2=browser2.find_element(By.XPATH,"/html")

text=(elem.text)
text2=(elem2.text)

#these are sample regex which is used for my project, modify them to your target website
w=list()
w.append(re.findall("(.*)[،](.*)\n.*پیش.*\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)",text))
w.append(re.findall("(.*)[،](.*)\n.*\n(.*)\n.*\n(.*)\n.*\n(.*)\nنمایشگاه\n(.*)\n(.*)",text))
w.append(re.findall("(.*)[،](.*)\n.*\n(.*)\n.*\n(.*)\n.*\n.*\nنمایندگی\n.*\n(.*)",text))
w.append(re.findall("(.*)[،](.*)\n.*پیش.*\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)",text2))
w.append(re.findall("(.*)[،](.*)\n.*\n(.*)\n.*\n(.*)\n.*\n(.*)\nنمایشگاه\n(.*)\n(.*)",text2))
w.append(re.findall("(.*)[،](.*)\n.*\n(.*)\n.*\n(.*)\n.*\n.*\nنمایندگی\n.*\n(.*)",text2))

final=list()
for i in w:
    for j in i:
        final.append(list(j))

c=0
final2=list()
for i in final:
        try:
            txt=i[2]
            final[c][2]=int(txt)
            txt =i[3]
            txt=txt.replace("کیلومتر","")
            txt=txt.replace("کارکرد صفر","0")
            txt=txt.replace("کارکردصفر","0")
            txt=txt.replace(",","")
        except:
            final.pop(c)
            c+=1
            continue
        try:
            final[c][3]=int(txt.replace(" ",""))
        except:
            final.pop(c)
            c+=1
            continue


        try:
            txt =i[5].split(" ")
            txt =txt[0]
            final[c][5]=txt
        except:
            final.pop(c)
            c+=1
            continue
        txt=i[6]
        try:
            final[c][6]=int(txt.replace(",",""))
        except:
            final.pop(c)
            c+=1
            continue

        final2.append(final[c])
        c+=1

db=mysql.connector.connect(user='root',password='admin',host= 'localhost')
cursor=db.cursor()
cursor.execute('USE main_database;')
for i in final2:
    query = ("INSERT INTO scrape (`brand`, `model`, `prod_year`, `mileage`, `trim`, `location`, `price`) VALUES(\'%s','%s',%s,%s,'%s','%s',%s);"% (i[0],i[1],i[2],i[3],i[4],i[5],i[6]))
    cursor.execute(query)
db.commit()
db.close()
