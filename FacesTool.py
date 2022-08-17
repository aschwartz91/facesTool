import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

import time


#SETUP webdriver
driver = webdriver.Chrome(executable_path='/Users/adamschwartz/Documents/PycharmProjects/WebAutomation/chromedriver')


scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/adamschwartz/Documents/PycharmProjects/Other/tamid-fl-2021-b7d946a70f6a.json', scope)
client = gspread.authorize(creds)
print("gspread authorized")
# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("test").sheet1
# Extract and print all of the values
names = sheet.col_values(2)
#global i = 1
print(names)

def getStarted():
    driver.get('https://acadinfo.wustl.edu/apps/Faces/')
    time.sleep(2)
    driver.get(driver.current_url)  # connect to re-directed site - login

    #driver.navigate().refresh()
    #btnStart = driver.find_element(By.XPATH, '//*[@id="ctl00_cphBody_btnLogin"]')
    #btnStart.click()
    # log in

    time.sleep(3)
    txtUsername = driver.find_element(By.XPATH,'//*[@id="ucWUSTLKeyLogin_txtUsername"]')
    txtUsername.send_keys('a.m.schwartz')

    txtPassword = driver.find_element(By.XPATH,'//*[@id="ucWUSTLKeyLogin_txtPassword"]')
    txtPassword.send_keys('Orow2326')

    btnLogin = driver.find_element(By.XPATH,'//*[@id="ucWUSTLKeyLogin_btnLogin"]')
    btnLogin.click()

    time.sleep(8)
getStarted()    

def getImage(name, i):
    
    #driver.find_element(By.XPATH,'//*[@id="divHasAccess"]/div[1]/div/a[1]').click()
    
    driver.find_element(By.ID, "Body_txtNameSearch").send_keys(name)

    #manipulate name so it fits:    last, first
    
    # search name
    btnSearch = driver.find_element(By.XPATH,'//*[@id="Body_btnSearch"]')
    btnSearch.click()

    #get image src
    time.sleep(5)

    img = driver.find_element(By.XPATH, '//*[@id="Body_repResults_picPhoto_0"]/img')
    srcLink = img.get_attribute("src")

    print("THIS IS THE SRC: ")
    print(srcLink)
    func = "=image(\"" + srcLink + "\")"
    print(func)
    #driver.get(driver.current_url)  # connect to re-directed site - duo
    #=image(" + srcLink + ')'

    
    cell = 'C' + str(i)
    print('replacing cell ' + cell)
    sheet.update_acell(cell, func)
    #i = i + 1
    print(i)
    cell = 'C' + str(i)
    print('now moving onto cell ' + cell)
    #currentCell = sheet.acell('C1').value
    #sheet.update('C1', currentCell[0:])
iterate = 1
for name in names: 
    print(name)
    getImage(name, iterate)
    iterate = iterate + 1
    time.sleep(5)
#list_of_hashes = sheet.row_values(2)
#tColumn = ["This", "is", "a test"]
#index = 14 - 14 is pictures


