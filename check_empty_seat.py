import sys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from tkinter import messagebox

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--safebrowsing-disable-download-protection")  # download에서 harmful message disable
chrome_options.add_argument("safebrowsing-disable-extension-blacklist")
chrome_options.add_argument("disable-extensions")
chrome_path = r"./chromedriver2.35.exe"
driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
print(sys.argv)
id = sys.argv[1]
pwd = sys.argv[2]
kind = sys.argv[3]
gu = sys.argv[4]
polling = sys.argv[5]

# 로그인 url
driver.get('http://www.q-net.or.kr/man001.do?id=man00103&gSite=Q&gId=03&login=Y')
driver.find_element_by_id('mem_id').send_keys(id)
driver.find_element_by_id('mem_pswd').send_keys(pwd)
driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div[1]/div[2]/button').click()
time.sleep(1)
driver.get('http://www.q-net.or.kr/rcv003.do?id=rcv00301&gSite=Q&gId=')
if '산업기사' in kind:
    driver.find_element_by_xpath('//*[@id="content"]/div[2]/form[1]/div[2]/div[1]/table/tbody/tr[1]/td[3]/button').click()
else:
    driver.find_element_by_xpath('//*[@id="content"]/div[2]/form[1]/div[2]/div[1]/table/tbody/tr[1]/td[3]/button').click()

select = Select(driver.find_element_by_xpath('//*[@id="content"]/div[2]/form/div/table/tbody/tr[2]/td/select'))
if '산업기사' in kind:
    select.select_by_visible_text('정보처리산업기사')
else:
    select.select_by_visible_text('정보처리기사')
time.sleep(1)
driver.find_element_by_xpath('//*[@id="btnGoNext"]').click()


select = Select(driver.find_element_by_id('sido'))
select.select_by_visible_text('서울특별시')
time.sleep(3)
select = Select(driver.find_element_by_id('sigungu'))
select.select_by_visible_text(gu)

select = Select(driver.find_element_by_id('recptCd'))
select.select_by_visible_text('일반응시자')
time.sleep(1)
select = Select(driver.find_element_by_id('recptDtlCd'))
select.select_by_visible_text('일반응시자')

flag = True
while flag:
    # 검색 버튼 클릭
    driver.find_element_by_xpath('//*[@id="content"]/div[3]/div/form/div/table/tbody/tr[4]/td/button').click()
    html = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="DIV1"]/div[2]/span'))).get_attribute('innerHTML')

    soup = BeautifulSoup(html, 'html.parser')
    button = soup.findAll('button')

    if not button:
        button = ['1']

    for i in range(0, len(button)):
        data = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="DIV1"]/div[1]/table/tbody'))).get_attribute('innerHTML')
        soup = BeautifulSoup(data, 'html.parser')
        trs = soup.findAll('tr')

        for tr in trs:
            tds = tr.findAll('td')
            if '마감' not in tds[7].get_text():
                messagebox.showinfo(tds[3].get_text(), tds[5].get_text())
        driver.execute_script("goPage("+str(i+2)+",'ddd');")
        time.sleep(2)
    time.sleep(int(polling))



