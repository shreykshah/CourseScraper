import csv
import time
import json
import argparse
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

r = requests.get('https://pages.cs.wisc.edu/~shrey/cc/ccoursescraperc')
ap = argparse.ArgumentParser(description='Sort classes by GPA')
ap.add_argument('-r', '--read', nargs='?', const='classes.csv',
                help='file to read course codes from')
ap.add_argument('-w', '--write', nargs='?', const='classes.csv',
                help='file to write course codes to')
ap.add_argument('-o', '--output', nargs='?', default='out.csv', help='output filename')
ap.add_argument('-p', '--print', nargs='*',
                help='print course grade pair from file')
args = ap.parse_args()

if args.print is None:
    if args.read is None:
        #get classes from Course Search and Enroll Page
        driver = webdriver.Firefox(executable_path="./geckodriver") #relative path
        url = "https://enroll.wisc.edu/search"

        driver.get(url) #navigate to the page
        input("Press Return to continue") #wait for user to indicate user has logged in/set settings as user wished

        #initialize variables needed
        classes = set()
        prev = ""
        course = " "
        actions = ActionChains(driver)
        actions.send_keys(Keys.PAGE_DOWN)
        ebreak = False

        print("getting courses")
        while True:
            prev = course
            #for each course "block"
            for course_path in driver.find_elements_by_xpath("/html/body/div[1]/div/div/div/div/md-card[2]/md-content/md-virtual-repeat-container/div/div[2]/md-list/md-list-item/div"):
                try: #last block is null so must put in try
                    #BeautifulSoup parses better than selenium
                    html = course_path.get_attribute('innerHTML')
                    soup = BeautifulSoup(html, "lxml") #only works after initialization
                    #find course code (ex. "CS 101")
                    course = soup.find('div', {"class":'result__name flex-80'}).strong.text.strip()
                    if course == " ":
                        time.sleep(1)
                        course = soup.find('div', {"class":'result__name flex-80'}).strong.text.strip()
                    #adding to set - set because repeats may happen as scroll may not scroll 1 view length
                    code = course.replace("&"," ")
                    #not adding empty strings
                    if code != "":
                        classes.add(code)
                except:
                    pass
             #have to click a card to scroll correct element of page
            driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/md-card[2]").click()
            actions.perform() #scroll PAGE_DOWN
            time.sleep(1) #have to wait or next cards won't load. havent tested lower settings than 1

            if ebreak and prev == course:
                break
            end_check = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/md-card[2]/md-toolbar/div/h4").text.strip().split(" ")
            if end_check[0] == end_check[2]:
                ebreak = True

        driver.quit()
        if args.write is not None:
            #write course codes to load later
            cw = csv.writer(open((args.write),'w'))
            cw.writerow(list(classes))
    else:
        #load course coads
        with open((args.read), newline='') as f:
            reader = csv.reader(f)
            classes = list(reader)[0]

    #initialize disctionary to store course GPA pair
    cg = dict()

    print("getting grades", end='\r')
    i=1
    for course_code in classes:
        #madgrades api query course code to get internal madgrades ID
        url = 'https://api.madgrades.com/v1/courses'
        auth = {'Authorization': 'Token token=930be378f74e4bc9aeba6d982586cfbf'}
        payload = {'query': course_code}
        r = json.loads(requests.get(url, params=payload, headers=auth).text)
        #madgrades api get grades using madgrades ID
        #checking only 0 because madgrades search pulls up the course first if
        #  given the course code and searching more might lead to finding an incorrect
        #  course, as can only check the course number
        try:
            if int(r["results"][0]["number"]) == int(course_code.split(" ")[-1]):
                url = r["results"][0]["url"] + "/grades"
                grade = json.loads(requests.get(url, headers=auth).text)
                #calculate average
                #not using certain values, contact registrar for more info
                tot = ((grade["cumulative"]["aCount"] * 4.0) + (grade["cumulative"]["abCount"] * 3.5) +
                       (grade["cumulative"]["bCount"] * 3.0) + (grade["cumulative"]["bcCount"] * 2.5) +
                       (grade["cumulative"]["cCount"] * 2.0) + (grade["cumulative"]["dCount"]))
                n = (grade["cumulative"]["aCount"] + grade["cumulative"]["abCount"] +
                     grade["cumulative"]["bCount"] + grade["cumulative"]["bcCount"] +
                     grade["cumulative"]["cCount"] + grade["cumulative"]["dCount"] +
                     grade["cumulative"]["fCount"])
                avg_gpa = tot / n
                sort_key = (tot) / (n+10) #adjusting for low class numbers
            else:
                avg_gpa = 0 #could not find course in MadGrades
                sort_key = 0
        except: #no previous data or error in data
            avg_gpa = 0
            sort_key = 0
        if avg_gpa == 0:
            #error where sort key may have value when avg_gpa has no value
            #not sure why this is occurring (not very reproducable), manually setting to 0
            sort_key = 0
        try:
            print(("getting grades: " + str('%.1f' % (i / len(classes) *100)) +
               "% complete"), end='\r')
        except:
            pass
        i=i+1
        cg[course_code] = [avg_gpa,sort_key] #adding pair to dictionary

    print("sorting\n")
    courses_inorder = {k: v for k, v in sorted(cg.items(), key=lambda item: item[1][1])}

    cw = csv.writer(open((args.output),'w'))
    npad = len(max(courses_inorder, key=len))
    for course in courses_inorder:
        print(course.ljust(npad) + "  " + str(round(cg[course][0],3)))
        #write output to csv to view later
        cw.writerow([course, cg[course][0], cg[course][1]])
else:
    #check arguments
    if args.print == []:
        args.print = ["out.csv",1000]
    if len(args.print) == 1:
        try:
            args.print = ["out.csv",int(args.print[0])]
        except:
            args.print = [str(args.print[0]),1000]

    # load course codes
    try: #try/except for if user inputs wrong way ("python scraper.py -p 1000 out.csv")
        with open((args.print[0]), newline='') as f:
            reader = csv.reader(f)
            plist = [[],[]]
            for rows in reader: #rows is array split by commas
                if int(rows[0].split(" ")[-1]) <= int(args.print[1]):
                    plist[0].append(rows[0])
                    plist[1].append(rows[1])
            npad = len(max(plist[0], key=len))
            for i in range(len(plist[0])):
                print(plist[0][i].ljust(npad) + "  " + str(round(float(plist[1][i]),3)))
    except Exception as e:
        try:
            with open((args.print[1]), newline='') as f:
                reader = csv.reader(f)
                plist = [[],[]]
                for rows in reader:
                    if int(rows[0].split(" ")[-1]) <= int(args.print[0]):
                        plist[0].append(rows[0])
                        plist[1].append(rows[1])
                npad = len(max(plist[0], key=len))
                for i in range(len(plist[0])):
                    print(plist[0][i].ljust(npad) + "  " + str(round(float(plist[1][i]),3)))
        except Exception as u:
            print("Please enter file and/or max course code")
            exit()
