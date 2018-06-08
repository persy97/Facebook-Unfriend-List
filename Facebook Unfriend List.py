#You need to pip install selenium and beautifulSoup4 to run this script
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import sqlite3
import getpass


#Username and Password of Facebook required for scrapping the data.
mail = input("Username: ")
while '@' in mail:
    print("Enter facebook username")
    mail = input("Username(only): ")
password = getpass.getpass("Password: ")
li=[]

#establishing connection with the existing Database
conn = sqlite3.connect('friendlist.db')

#incase the user is logging in for the first time on the machine using this script, create new table.
conn.execute('''CREATE TABLE IF NOT EXISTS USERS
(EMAIL BLOB NOT NULL PRIMARY KEY);''')

browser=webdriver.Firefox()
browser.get('https://mbasic.facebook.com/login')

#scrapping information from the html page source and performing clicks to go from on page to another.
mailbox = browser.find_element_by_name('email')
mailbox.clear()
mailbox.send_keys(mail)
pswd = browser.find_element_by_name('pass')
pswd.send_keys(password)
login = browser.find_element_by_name('login')
login.click()
browser.get('https://mbasic.facebook.com/profile.php')
frnd = browser.find_element_by_xpath('//*[@id="m-timeline-cover-section"]/div[3]/a[2]')
frnd.click()
html1 = browser.page_source
soup = bs(html1,"lxml")
out = soup.find('html')
out = out.find('body')
out = out.find('div')
out = out.find('div')
out = out.find('div')
out = out.next_sibling
out = out.find('div')
out = out.find('div')
out = out.find('div')
out = out.next_sibling
out = out.find('div')
out = out.next_sibling


#scrapping friendlist
for x in out.find_all('a'):
    li.append(x.text)
more = browser.find_element_by_xpath('//*[@id="m_more_friends"]/a/span')
more.click()
while True:
    html1 = browser.page_source
    soup = bs(html1,"lxml")
    out=soup.find('html')
    out = out.find('body')
    out = out.find('div')
    out = out.find('div')
    out = out.find('div')
    out = out.next_sibling
    out = out.find('div')
    out = out.find('div')
    out = out.find('div')
    out = out.next_sibling
    for x in out.find_all('a'):
        li.append(x.text)
    try:
        more = browser.find_element_by_xpath('//*[@id="m_more_friends"]/a/span')
        more.click()
    except:
        break

#inserting the list in a database
try:
    conn.execute('INSERT INTO USERS(EMAIL) VALUES(?);',(mail,))
    conn.execute('CREATE TABLE {} (Friends BLOB)'.format(mail))
    for x in li:
        conn.execute('INSERT INTO {}(Friends) VALUES({})'.format(mail,"'"+x+"'"))
except Exception as e:
    uf = []
    nf = []
    cursor = conn.execute('SELECT * FROM {}'.format(mail))
    for row in cursor:
        if row[0] not in li:
            uf.append(row[0])
            conn.execute('DELETE FROM {} WHERE Friends={}'.format(mail,"'"+row[0]+"'"))
    print("Unfriended:")
    print(uf)
    tl=[]
    cursor = conn.execute('SELECT * FROM {}'.format(mail))
    for x in cursor:
        tl.append(x[0])
    for x in li:
        if x not in tl:
            nf.append(x)
            conn.execute('INSERT INTO {}(Friends) VALUES({})'.format(mail,"'"+x+"'"))
    print("New Friends:")
    print(nf)
conn.commit()
conn.close()
browser.quit()
