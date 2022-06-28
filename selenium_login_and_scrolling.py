'''
Залогиниться при помощи Selenium на сайт https://scrapingclub.com/exercise/basic_login/
После логина перейти на страницу https://scrapingclub.com/exercise/list_infinite_scroll/ и спарсить:
* картинку
* ссылку на товар
* название товара
* цену

Данные сохранить в .json

(Для логина и сбора данных использовать Selenium)
'''
import json
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = Service('./chromedriver.exe')
driver = webdriver.Chrome(service=service)

# Login script
driver.get('https://scrapingclub.com/exercise/basic_login')

WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'id_name')))

time.sleep(3)

name_input = driver.find_element(by=By.ID, value='id_name').send_keys('scrapingclub')
psw_input = driver.find_element(by=By.ID, value='id_password').send_keys('scrapingclub')

time.sleep(3)

submit_btn = driver.find_element(by=By.XPATH, value='//button[@type="submit"]')
submit_btn.click()

time.sleep(5)

# Scrolling script
driver.get('https://scrapingclub.com/exercise/list_infinite_scroll')

WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//div[@class="card"]')))

initial_height = driver.execute_script('return document.body.scrollHeight')
print(initial_height)

while 1:
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    
    pause_t = random.randint(3, 5)
    time.sleep(pause_t)
    
    new_height = driver.execute_script('return document.body.scrollHeight')
    print(new_height)
    
    if initial_height == new_height:
        break
    
    initial_height = new_height
        
all_cards = driver.find_elements(by=By.XPATH, value="//div[@class='card']")
cards_lst = []

for c in all_cards:
    item_img = c.find_element(by=By.XPATH, value=".//img[contains(@class, 'card-img-top')]").get_attribute('src')
    item_link = c.find_element(by=By.XPATH, value=".//h4[@class='card-title']/a").get_attribute('href')
    item_name = c.find_element(by=By.XPATH, value=".//h4[@class='card-title']/a").text
    item_price = c.find_element(by=By.XPATH, value=".//div[@class='card-body']/h5").text
    
    cards_lst.append({
        'image': item_img,
        'link': item_link,
        'name': item_name,
        'price': item_price
    })

with open('cards.json', 'w', encoding='utf-8') as jf:
    json.dump(cards_lst, jf)
    
driver.quit()