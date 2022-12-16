from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import urllib
from urllib.parse import urljoin
import pandas as pd
from urllib.request import urlopen
import requests


# us to configure Headless Chrome
options = Options()
# this parameter tells Chrome that
# it should be run without UI (Headless)
options.headless = True
options.add_argument("start-maximized")
browser = webdriver.Chrome(options=options)


def get_first_search_result(url):
    # Try checks if error
        try:
            rso = WebDriverWait(browser, 3).until(
                EC.presence_of_element_located((By.ID, "rso"))
            )
            results = browser.find_elements(By.CSS_SELECTOR, 'div.g')
            link = results[0].find_element(By.TAG_NAME, "a")
            href = link.get_attribute("href")
            #print(href)
            return href

        except:
            print("in loop")
            time.sleep(200)
            return ("No JMC")
            browser.quit()


#loops through list of urls

#function that gets the url result of a google search from a list
def results_list(list):
    url_list = []
    iterations = 0
    for i in list:
        # creates search_string
        search_string = ('https://www.google.com/search?q=' +
                         i[0] +
                         '+econ+job+market+candidates&rlz=1C1CHBD_enUS811US811&oq=harvard&aqs='
                         'chrome.0.69i59j46i433i512j69i59j0i433i512l2j69i60l3.1242j0j4&sourceid=chrome&ie=UTF-8')
        # does google search
        matched_elements = browser.get(search_string)
        url1 = get_first_search_result(search_string)
        url_list.append(url1)
        iterations +=1
        print(iterations, url1)
    return url_list

#gets a data frame with school names and urls
def get_url_df(df):
    # convert data frame to list
    school_name_list = df.values.tolist()
    # print(school_name_list)

    # get all urls from each school on list
    jmc_urls = results_list(school_name_list)
    print(jmc_urls)
    school_url_list = list(zip(school_name_list, jmc_urls))

    school_ur_df = pd.DataFrame(school_url_list, columns=['School', 'Url'])

    school_ur_df.to_csv('School_JMC_URLs.csv')
    return school_ur_df

def get_file_data_normal(file, cand_web):
    link = file.get('href')
    # gets full url, joins to make formatting right
    full_cand_url = urljoin(cand_web, link).replace(" ", "%20")
    # checks to see if request goes through
    try:
        urllib.request.urlretrieve(full_cand_url)
    except Exception as e:
        print("Normal Error:", e, full_cand_url)

    file_data = requests.get(full_cand_url).content
    return file_data, full_cand_url

def get_file_data_google(file, cand_web):
    link = file.get('href')
    # gets full url, joins to make formatting right
    website = urljoin(cand_web, link).replace(" ", "%20")
    # checks to see if request goes through
    try:
        urllib.request.urlretrieve(website)
    except Exception as e:
        print("Google Error:", e, website)

    redirectlink = requests.get(website).content
    actual_site = redirectlink.decode().split("to ")[-1].split("<")[0]
    file_data = requests.get(actual_site).content
    return file_data, actual_site
