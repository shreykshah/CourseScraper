import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import csv

driver = webdriver.Firefox(executable_path="./geckodriver") #relative path
url = "https://enroll.wisc.edu/search"

driver.get(url) #navigate to the page
input() #wait for user to indicate user has logged in/set settings as user wished

#initialize variables needed
classes = set()
prev = ""
course = " "
actions = ActionChains(driver)
actions.send_keys(Keys.PAGE_DOWN)

while prev != course:
    prev = course
    #for each course "block"
    for course_path in driver.find_elements_by_xpath("/html/body/div[1]/div/div/div/div/md-card[2]/md-content/md-virtual-repeat-container/div/div[2]/md-list/md-list-item/div"):
        try: #last block is null so must put in try
            html = course_path.get_attribute('innerHTML') #BeautifulSoup parses better than selenium
            soup = BeautifulSoup(html, "lxml") #only works after initialization
            #find course code (ex. "CS 101")
            course = soup.find('div', {"class":'result__name flex-80'}).strong.text.strip()
            #add to set - set because repeats may happen as scroll may not scroll 1 view length
            classes.add(course)
        except:
            pass
     #have to click a card to scroll correct element of page
    driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/md-card[2]").click()
    actions.perform() #scroll PAGE_DOWN
    time.sleep(1) #have to wait or next cards won't load. havent tested lower settings than 1
print(sorted(classes))

cw = csv.writer(open("classes.csv",'wb'))
cw.writerow(list(classes))
