#!/usr/bin/python3
from selenium import webdriver
import time
from colorama import init, Fore
import pyfiglet
from config import audio
import datetime
import os
import pickle
import sqlite3
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

def save(name, status, duration):
    conn = sqlite3.connect('informer.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Status(Name varchar(40), Time datetime, Status varchar(7), Duration varchar(15))")
    c.execute("INSERT INTO Status VALUES(?, datetime('now', 'localtime'), ?, ?)", (name.capitalize(), status, duration))
    conn.commit()
    c.close()
    conn.close()

def main():
    try:
        print("!<--------------Press Ctrl+C to quit/terminate----------------->")
        ascii_banner = pyfiglet.figlet_format('INFORMER')
        print(Fore.CYAN + ascii_banner)
        print('By Arnab' + Fore.RESET)
        print()
        print()
        print('Enter the name of the person to track')
        name = input('> ').lower()
        browser = webdriver.Firefox() # Use webdriver.Chrome() if using google chrome or chromium-based browsers
        browser.get('https://web.whatsapp.com')
        time.sleep(14)
        flag = 0
        temp1 = None
        while True:
            try:
                elem = browser.find_element_by_css_selector('.O90ur')
                if elem.text == 'online' and flag != 1:
                    mixer.init()
                    mixer.music.load(audio) #Path to your audio of choice
                    mixer.music.play() 
                    status = str(datetime.datetime.now().strftime('%B %d, %Y -- %r')) + ' : online'
                    temp1 = datetime.datetime.now()
                    flag = 1
                    print(Fore.GREEN + status)
                    save(name, "online", None)
                    
            except (NoSuchElementException, StaleElementReferenceException):
                if flag != 2:
                    status = str(datetime.datetime.now().strftime('%B %d, %Y -- %r')) + ' : offline'
                    temp2 = datetime.datetime.now()
                    if temp1 != None:
                        duration = temp2 - temp1
                        print(Fore.YELLOW + "Duration: ", duration.total_seconds()//60, "mins", duration.total_seconds()%60, "secs")
                        save(name, "offline", str(duration))
                    flag = 2
                    print(Fore.RED + status)
    except KeyboardInterrupt:
        print()
        print(Fore.RED + 'Exiting......')

if __name__ == "__main__":
    main()
