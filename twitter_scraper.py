I# The standard library modules
import os
import sys
import time
import datetime

# The BeautifulSoup module
from bs4 import BeautifulSoup

# The selenium module
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# parameter
page = "https://twitter.com/search?f=tweets&vertical=default&q=sdgs%20"
#page = "https://twitter.com/search?f=tweets&vertical=default&q=%23E3%20lang%3Aen%20since%3A2016-06-15%20until%3A2016-06-16&src=typd" # change search path and conditions
filename = "aa.csv"                                                               # TBD: default output filename
driverpath = "d:/temp/chromedriver.exe" # TBD: chromedriver path, modify here
# print debug message
debug = 0

#### func: run ####
# filename output filename
# append: 0: newfile, 1 append
# date: data tag, ex: 2016-12-01

def run(filename, append, date):

    if debug:
        print filename, append, date;
        return 1;
I
    if date != "":
        date_end = date + datetime.timedelta(days=1)
        page_tmp = page + "since%3A" + str(date) + " until%3A" + str(date_end) +"&l=en&src=typd"       
    else:
        page_tmp = page

    if append:
        f = open(filename, "a")
    else:
        f = open(filename, "w")

    #f.write(page_tmp)
    #f.write("\n")
    
    # step2
    driver = webdriver.Chrome(driverpath) # assign chromedriver path
    driver.get(page_tmp) # load the web page
    
    # loop for scrolling
    #for cc in range(0,10): # TBD: loop 200 times
    #    print "wait"
    #    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #    time.sleep(1)

    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match = 0
    wait_num = 0
    while match==0 :
        lastCount = lenOfPage
        wait_num = wait_num + 1
        print "wait", wait_num 
        time.sleep(1)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match = 1
	if wait_num == 300:
            match = 1

    # step3
    src = driver.page_source # gets the html source of the page
    
    # step4
    parser = BeautifulSoup(src,"html.parser") # initialize the parser and parse the source "src"
    
    # step 5
    #print parser.html.head.title
    for hit in parser.findAll('div', attrs={'class':'content'}): # username
#        tmp = hit.find('span', attrs={'class':'username js-action-profile-name'})
#        if debug:
#           print tmp.text
#       f.write(tmp.text)
#        f.write(",")
    
        # time
        tmp = hit.find('small', attrs={'class':'time'}).a
        if debug:
            print tmp['title']
    
        text_ascii = tmp['title'].encode("big5", "replace")
        f.write(text_ascii)
        f.write(",")
    
        # content
        for tmp in hit.findAll('div', attrs={'class':'js-tweet-text-container'}):
            text = tmp.text
            if debug:
                print "----"
                # fix output encoding issue
                print(text.encode(sys.stdin.encoding, "replace").decode(sys.stdin.encoding))
    
            text_ascii = text.encode("ascii", "replace")
            text_ascii = text_ascii.replace('\r',' ')
            text_ascii = text_ascii.replace('\n',' ')
            f.write('"')
            f.write(text_ascii)
            f.write('"')
            f.write("\n")
    #    break
    
    # step6
    f.close()      # close file
    #driver.close() # closes the driver
    
#### end func:run ####

#### main ####

#run for one mounth
filename = "sdg_2016_01.csv" # TBD: filename, modify here
for i in range(31, 1, -1):   # TBD: day range, modify here, from 1 ~ 31
    year   = 2016           # TBD: 2016, modify here
    mounth = 1             # TBD: 1 ~ 12, modify here
    date = datetime.date(year, mounth, i)
    print "run", filename, date
    run(filename, 1 , date)

## run once without date condition
#filename = "aa2.csv"
#run(filename, 0 , "")

