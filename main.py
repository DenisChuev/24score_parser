from bs4 import BeautifulSoup
import requests
import lxml

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tkinter import *

unplayed_matches = []
played_matches = []


def search():
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-dev-sh-usage')
    driver = webdriver.Chrome(options=option)
    driver.get(txt.get())
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "table.standings")))
    table = driver.find_elements(By.CSS_SELECTOR, "table.standings")[0]
    # print(table.text)
    commands = table.find_elements(By.TAG_NAME, "a")
    for command in commands:
        print(command.get_attribute("href"))

    driver.get(commands[0].get_attribute("href"))
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "table.datatable")))
    matches = driver.find_elements(By.CSS_SELECTOR, "table.datatable tr")

    for match in matches:
        td = match.find_elements(By.CSS_SELECTOR, "td")
        if len(td) == 1 and td[0].get_attribute("class") == "null":
            break
        # print(match.text)
        if len(td) > 3 and td[3].text == "— —":
            unplayed_matches.append(td[0])
        elif len(td) > 3:
            played_matches.append(td[0])

    print("Несыгранные матчи:")
    for un in unplayed_matches:
        print(un.text)

    print("Cыгранные матчи:")
    for pl in played_matches:
        print(pl.text)


window = Tk()
window.title("24score.pro/football")
window.geometry('1000x500')
txt = Entry(window, width=100)
txt.grid(column=2, row=2)
btn = Button(window, text="Поиск", command=search)
btn.grid(column=3, row=2)
window.mainloop()
