import urllib
from urllib.parse import urljoin
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import os
import re
from pathlib import Path

url_df = pd.read_csv(r'C:\Users\15the\Documents\NLP Projects\Selenium_JMC\School_JMC_URLs.csv')

url = url_df['Url'][4]
print(url)
school = url_df['School'][4]
# requests data from url
html = requests.get(url).content
soup = BeautifulSoup(html, features="lxml")


def get_card_content(candidate_card_content_class):
    name_element = candidate_card_content_class.find("h2", class_="field-content").text
    website_element = candidate_card_content_class.find('a',
                                                          attrs={'href': re.compile("^http")}).get('href')
    email_element = candidate_card_content_class.find("div",
                                                      class_="views-field views-field-field-hs-person-email").text
    jmp_element = candidate_card_content_class.find("div",
                                                    class_="views-field views-field-custm-hs-job-market-paper").text
    fos_element = candidate_card_content_class.find("div",
                                                    class_="views-field views-field-field-hs-person-interests").text
    advisors_element = candidate_card_content_class.find("div", class_="views-field views-field-custm-advisors").text
    d = {'Name': [name_element],"Website": [website_element], "Email": [email_element], "Job Market Paper": [jmp_element],
         'Field of Study': [fos_element], "Advisors": [advisors_element]}
    df = pd.DataFrame(data=d)
    return df


def get_candidate_image(candidate_card_img_class):
    # images
    candidate_card_img = candidate_card_img_class.find('img')
    candidate_img = candidate_card_img.attrs['src']
    full_url = urljoin(url, candidate_img)
    urllib.request.urlretrieve(full_url)
    #print(full_url)
    img_data = requests.get(full_url).content
    return img_data


def create_folder(path):
    # Check whether the specified path exists or not
    if not os.path.exists(path):
        # if the demo_folder directory is not present
        # then create it.
        os.makedirs(path)
    return path


candidate_card_content_classes = soup.find_all('div', class_='hb-card__content')
candidate_card_img_classes = soup.find_all('div', class_='hb-card__graphics')

card_df = []
img_df = []

#parent_dir = "C:\Users\\15the\Documents\NLP Projects\Selenium_JMC\\"


school_folder = create_folder(school)
os.chdir(school_folder)
#print("current dir:", os.getcwd())
# print(school)

#loops through all candidates
for card, image in zip(candidate_card_content_classes, candidate_card_img_classes):
    card_data = get_card_content(card)
    name = card_data['Name'].to_string().replace("0    ", "")
    #print(name)
    path = os.getcwd() + '\\' + name
    #gets folder if exists, creates it if it does not
    candidate_folder = create_folder(path)
    card_data.to_csv(candidate_folder+'\\'+name+".csv")
    img_data = get_candidate_image(image)
    with open(f"{path}\{name}_picture.jpg", 'wb') as handler:
        handler.write(img_data)
    #CV
    cand_web = card_data['Website'].iloc[0]
    cand_htm = requests.get(cand_web).content
    cand_soup = BeautifulSoup(cand_htm, features="lxml")
    cand_files = cand_soup.find_all('a',
                                    attrs={'href': re.compile(".pdf|.doc|.txt")})

    for val in cand_files:
        link = val.get('href')
        #gets full url, joins to make formatting right
        full_cand_url = urljoin(cand_web, link).replace(" ", "%20")
        #print(full_cand_url)
        #checks to see if request goes through
        try:
            urllib.request.urlretrieve(full_cand_url)
        except Exception as e:
            print("Error:", e, full_cand_url)
            continue
        # print(full_url)
        #gets content of file
        file_data = requests.get(full_cand_url).content
        file_ending = full_cand_url.title().split('/')[-1].split('&')[0]
        print("full URL:", full_cand_url, "file ending:", file_ending)
        try:
            with open(f"{path}\{name}_{file_ending}", 'wb') as handler:
                handler.write(file_data)
        except Exception as e:
            print("We are in exception now")
            print(e)
            try:
                file_ending = full_cand_url.title().split('.')[-1].split('&')[0]
                print("file ending 2:", file_ending[:3])
                with open(f"{path}\{name}_{file_ending[:3]}", 'wb') as handler:
                    handler.write(file_data)
            except Exception as e:
                print("Error:", e, full_cand_url)

    card_df.append(card_data)

candidate_info = pd.concat(card_df)
candidate_info.to_csv(school_folder+".csv")

#print(candidate_info['Website'])

# cand_web = candidate_info['Website'].iloc[0]
# cand_htm = requests.get(cand_web).content
# cand_soup = BeautifulSoup(cand_htm, features="lxml")
# cand_files = cand_soup.find_all('a',
#                                                           attrs={'href': re.compile(".pdf|.doc|.txt")})
#
# for val in cand_files:
#     link = val.get('href')
#     with open(path + '\\'+name +'_CV.{}'.format(link[-3:]), 'wb') as handler:
#         handler.write(link)

#array of acceptable cv types
#on each website look through each link and see if it has an extension (contains)
