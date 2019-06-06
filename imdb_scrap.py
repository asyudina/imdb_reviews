
import time

import requests
import pandas as pd
from pandas import ExcelWriter

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


# inputs
url_add = str(input("Paste URL,Hit Space and then Enter\n"))
filename = str(input("name your output file\n"))

# runtime
start_time = time.time()

# calculating maxclicks
source_code = requests.get(url_add)
plain_text = source_code.text
soup = BeautifulSoup(plain_text, 'html.parser')

for number_of_reviews in soup.findAll('div', {'class': 'header'}):
    c = number_of_reviews.text
    s = c.split()
    s = str(s[0])
    s = int(s.replace(",", ""))
    break
maxclicks = s//25
print('maxclicks='+str(maxclicks))


driver = webdriver.Chrome("/Users/a.yudina/Downloads/imdb-master/chromedriver")
wait = WebDriverWait(driver, 100)

driver.get(url_add)

# click more until no more results to load
clicks = 0
while True:
    clicks += 1
    if clicks <= maxclicks:
        more_button = wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "ipl-load-more__button"))).click()


    else:
        break
    print(str(clicks) + "click")
print('out of loop')
time.sleep(25)
source_code = driver.page_source

# not source_code.text since here source_code is obtained from selenium is string not a beautifulsoup object

plain_text = source_code
soup = BeautifulSoup(plain_text, 'html.parser')
# print(soup)

database = []
pageno = 1
rating_list = []
title_list = []
review_list = []


for item in soup.select(".review-container"):
    title = item.select(".title")[0].text
    review = item.select(".text")[0].text
    title_list.append(title)
    review_list.append(review)

df1 = pd.DataFrame(title_list, columns=['title'])
#df2 = pd.DataFrame(rating_list, columns=['rating'])
df3 = pd.DataFrame(review_list, columns=['review'])
df12 = df1
df = df12.join(df3)

df.to_excel(filename + '.xlsx')


elapsed_time = time.time() - start_time
print(elapsed_time)
