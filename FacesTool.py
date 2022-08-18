#A. Schwartz
#8.17.22
#This code takes a list of WashU students names in a google spreadsheet

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.headless = True
driver = webdriver.Chrome('/Users/adamschwartz/Documents/PycharmProjects/WebAutomation/chromedriver', options=options)

#SETUP webdriver
driver = webdriver.Chrome(executable_path='/Users/adamschwartz/Documents/PycharmProjects/WebAutomation/chromedriver')


scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/adamschwartz/Documents/PycharmProjects/Other/tamid-fl-2021-b7d946a70f6a.json', scope)
client = gspread.authorize(creds)
print("gspread authorized")
sheet = client.open("faceTool").sheet1
names = sheet.col_values(2)
print(names)

def getStarted():
    driver.get('https://acadinfo.wustl.edu/apps/Faces/')
    time.sleep(2)
    driver.get(driver.current_url)

    txtUsername = driver.find_element(By.XPATH,'//*[@id="ucWUSTLKeyLogin_txtUsername"]')
    txtUsername.send_keys('a.m.schwartz')

    txtPassword = driver.find_element(By.XPATH,'//*[@id="ucWUSTLKeyLogin_txtPassword"]')
    txtPassword.send_keys('Orow2326')

    btnLogin = driver.find_element(By.XPATH,'//*[@id="ucWUSTLKeyLogin_btnLogin"]')
    btnLogin.click()

    time.sleep(8) #DUO time
def generateImg(i):
    img = driver.find_element(By.XPATH, '//*[@id="Body_repResults_picPhoto_0"]/img')
    srcLink = img.get_attribute("src")

    func = "=image(\"" + srcLink + "\")"
    print(func)
    cell = 'C' + str(i)
    
    print('replacing cell ' + cell)
    sheet.update_acell(cell, func)
    cell = 'C' + str(i)
    print('now moving onto cell ' + cell)
def getImage(name, i):
    
    driver.find_element(By.ID, "Body_txtNameSearch").send_keys(name)

    #manipulate name so it fits:    last, first
    
    # search name
    btnSearch = driver.find_element(By.XPATH,'//*[@id="Body_btnSearch"]')
    btnSearch.click()

    #get image src
    time.sleep(2)

    cell = 'C' + str(i)
    if driver.find_element(By.XPATH, '//*[@id="Body_lblResults"]').get_attribute("textContent") == '0 Results': 
        print('replacing cell ' + cell)
        sheet.update_acell(cell, 'no picture could be found')
        print('no results found for ' + name)
        exit

    elif driver.find_element(By.XPATH, '//*[@id="Body_lblResults"]').get_attribute("textContent") != '1 Results': 
        print('multiple results found for ' + name)
        sheet.update_acell(cell, 'multiple images found, find one yourself')
        #generateImg(i)
    else:
        generateImg(i)



getStarted() 
iterate = 1

for name in names: 
    print(name)
    getImage(name, iterate)
    iterate = iterate + 1
    time.sleep(1)
#list_of_hashes = sheet.row_values(2)
#tColumn = ["This", "is", "a test"]
#index = 14 - 14 is pictures


