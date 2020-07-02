import time
from selenium import webdriver

driver = webdriver.Firefox(executable_path="./geckodriver") #relative path
url = "https://enroll.wisc.edu/search?term=1212" #local varibale is all caps
WAITTIME = 10 # seconds

driver.get(url) #navigate to the page
input()
time.sleep(2)
classes = set()

prev = ""
prev_counter = 0


while prev_counter < 30:
    fir = True
    for course_path in driver.find_elements_by_xpath("/html/body/div[1]/div/div/div/div/md-card[2]/md-content/md-virtual-repeat-container/div/div[2]/md-list/md-list-item"):
        classes.add(course_path.find_element_by_xpath("//div/div[2]/div/div[1]/strong").get_attribute('innerHTML'))
        if fir is True:
            new = course_path.find_element_by_xpath("//div/div[2]/div/div[1]/strong").get_attribute('innerHTML')
        fir = False
    if new == prev:
        prev_counter = prev_counter+1
    else:
        prev = new
        prev_counter = 0
print(classes)



# /html/body/div[1]/div/div/div/div/md-card[2]/md-content/md-virtual-repeat-container/div/div[2]/md-list/md-list-item[7]/div/div[2]/div/div[1]/strong
# /html/body/div[1]/div/div/div/div/md-card[2]/md-content/md-virtual-repeat-container/div/div[2]/md-list/md-list-item[4]/div/div[2]/div/div[1]/strong

# /html/body/div[1]/div/div/div/div/md-card[2]/md-content/md-virtual-repeat-container/div/div[2]/md-list/md-list-item[6]/div/div[2]/div/div[1]
# /html/body/div[1]/div/div/div/div/md-card[2]/md-content/md-virtual-repeat-container/div/div[2]/md-list/md-list-item[3]/div/div[2]/div/div[1]/strong

# cw = csv.writer(open("classes.csv",'wb'))
# cw.writerow(list(cols))
