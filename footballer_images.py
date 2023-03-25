import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time

PATH = "C:/Users/user/Downloads/chromedriver_win32/chromedriver.exe"
a = webdriver.Chrome(PATH)
players = pd.read_csv('./player_team.csv')
player_names = players['Player Name'].values.tolist()
players.insert(2, "image_url", True)
def get_images(players, p, a, time_delay):
    def scroll_down(a):
        a.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(time_delay)
    s = p.split()
    team = players[players['Player Name'] == p]['Team'].values
    if team[0] and p:
        url = "https://www.google.com/search?q=" + p +"+" + team[0] + "+png&gs_lcp=CgNpbWcQAzIHCAAQgAQQEzoHCAAQigUQQzoFCAAQgAQ6BggAEAcQHjoECAAQHjoGCAAQHhATUIsDWKsLYNIMaABwAHgAgAFMiAGzApIBATWYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=TSceZPmwNJ64nsEPkM25oAc&bih=752&biw=767"
    else:
        return ''
    a.get(url)
    thumbnails = a.find_elements(By.CLASS_NAME, 'uhHOwf')
    for img in thumbnails:
        try:
            img.click()
            time.sleep(time_delay)
        except:
            continue
        images = a.find_elements(By.CLASS_NAME, "n3VNCb")
        for image in images:
            print(image)
            if image.get_attribute('src'):
                return image.get_attribute('src')
            
    return players

l = []
for i in player_names:
    l.append(get_images(players, i, a, 1))
    time.sleep(2)
players.insert(2, "image_url", l, True)
players.to_csv('C:\\Users\\user\\Desktop\\Projet_Annuel\\player_team&photo.csv', index=False)

