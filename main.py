from selenium import webdriver
import time
import datetime
import os
import pickle
import sqlite3
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

# def save(data, name):
#     with open(name, 'a') as f:
#         f.write(data + "\n")

def save(name, status, duration):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Status(Name varchar(40), Time datetime, Status varchar(7), Duration varchar(15))")
    c.execute("INSERT INTO Status VALUES(?, datetime('now', 'localtime'), ?, ?)", (name.capitalize(), status, duration))
    conn.commit()
    c.close()
    conn.close()

def main():
    print("!<--------------Press Ctrl+C to quit/terminate----------------->")
    name = input('Enter the name of the person to track: ').lower()
    browser = webdriver.Firefox() # Use webdriver.Chrome() if using google chrome or chromium-based browsers
    browser.get('https://web.whatsapp.com')
    time.sleep(14)
    flag = 0
    temp1 = None
    while True:
        try:
            elem = browser.find_element_by_class_name('_315-i')
            if elem.text == 'online' and flag != 1:
                mixer.init()
                mixer.music.load('C:/Users/Arnab/Music/cycle.mp3') #Path to your audio of choice
                mixer.music.play() 
                status = str(datetime.datetime.now().strftime('%B %d, %Y -- %r')) + ' : online'
                temp1 = datetime.datetime.now()
                flag = 1
                print(status)
                save(name, "online", None)
                
        except (NoSuchElementException, StaleElementReferenceException):
            if flag != 2:
                status = str(datetime.datetime.now().strftime('%B %d, %Y -- %r')) + ' : offline'
                temp2 = datetime.datetime.now()
                if temp1 != None:
                    duration = temp2 - temp1
                    print("Duration: ", duration.total_seconds()//60, "mins", duration.total_seconds()%60, "secs")
                    save(name, "offline", str(duration))
                flag = 2
                print(status)

if __name__ == "__main__":
    main()
