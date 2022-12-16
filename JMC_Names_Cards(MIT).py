import pdb
import urllib
from urllib.parse import urljoin
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import os
import re
from Selenium_JMC_Functions import get_file_data_google
from Selenium_JMC_Functions import get_file_data_normal

url_df = pd.read_csv(r'C:\Users\15the\Documents\NLP Projects\Selenium_JMC\School_JMC_URLs.csv')

url = url_df['Url'][3]
print(url)
school = url_df['School'][3]
# requests data from url
html = requests.get(url).content
soup = BeautifulSoup(html, features="lxml")


candidate_card_content_classes = soup.find_all('div', class_='col-12 col-md-4')
#print(candidate_card_content_classes)
candidate_card_img_classes = soup.find_all('figure', class_='caption caption-img')
# print(candidate_card_content_classes)
#print(candidate_card_img_classes)
card_df = []
img_df = []
#print(soup)


def get_card_content(candidate_card_content_class):
    print("get_card_content entered")
    name_element = candidate_card_content_class.find('a').text
    print("Name:", name_element)
    website_element = candidate_card_content_class.find('a').get('href')
    full_url = urljoin(url, website_element)
    print("Website:", full_url)
    email_element = candidate_card_content_class.find("a").text
    #print("Email:", email_element)
    # jmp_element = candidate_card_content_class.find('a',
    #                                                       attrs={'href': re.compile("^http")}).get('href')
    #print("JMP:", jmp_element)
    fos_element = candidate_card_content_class.find_all("br")
    print("Field:", fos_element)
    #advisors_element = candidate_card_content_class.find_all("p")[2].text
    #print("Advisors:", advisors_element)
    d = {'Name': [name_element],"Website": [full_url], "Email": [email_element],
         'Field of Study': [fos_element]}
    df = pd.DataFrame(data=d)
    print(name_element)
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

#parent_dir = "C:\Users\\15the\Documents\NLP Projects\Selenium_JMC\\"
school_folder = create_folder(school)
os.chdir(school_folder)
print("current dir:", os.getcwd())
for card, image in zip(candidate_card_content_classes, candidate_card_img_classes):
    card_data = get_card_content(card)
    name = card_data['Name'].to_string().replace("0    ", "").replace("\\n","")
    #print("Name:",name)
    path = os.getcwd() + '\\' + name
    #print("Path:")
    #gets folder if exists, creates it if it does not
    candidate_folder = create_folder(path)
    #print(candidate_folder)
    card_data.to_csv(f"{candidate_folder}\{name}.csv")
    img_data = get_candidate_image(image)
    with open(f"{path}\{name}_picture.jpg", 'wb') as handler:
        handler.write(img_data)
    #CV
    cand_web = card_data['Website'].iloc[0]
    cand_htm = requests.get(cand_web).content
    cand_soup = BeautifulSoup(cand_htm, features="lxml")
    cand_files = cand_soup.find_all('a',
                                    attrs={'href': re.compile(".pdf|.doc|.txt")})
    count = 0
    for file in cand_files:
        link = file.get('href')

        if('google' in link):
            file_data, full_cand_url = get_file_data_google(file, cand_web)
            file_ending = full_cand_url.split('/')[-1].split('?')[0]
            print('google url:', file_ending)
        else:
            file_data, full_cand_url = get_file_data_normal(file, cand_web)
            file_ending = full_cand_url.title().split('/')[-1].split('&')[0]
            print('normal url:', file_ending)
        try:
            with open(f"{path}\{name}_{file_ending}", 'wb') as handler:
                handler.write(file_data)
        except Exception as e:
            print("We are in exception now")
            print(e)

            # if re.search("google", full_cand_url):
            #     print("google thing")
            #     file_ending = full_cand_url.title().split('%2F')[-1].split('&')[0]
    card_df.append(card_data)
candidate_info = pd.concat(card_df)
candidate_info.to_csv(school_folder+".csv")


# print(school)
#
# #loops through all candidates
# for card, image in zip(candidate_card_content_classes, candidate_card_img_classes):
#     card_data = get_card_content(card)
#     name = card_data['Name'].to_string().replace("0    ", "").replace("\\n","")
#     #print("Name:",name)
#     path = os.getcwd() + '\\' + name
#     #print("Path:")
#     #gets folder if exists, creates it if it does not
#     candidate_folder = create_folder(path)
#     #print(candidate_folder)
#     card_data.to_csv(f"{candidate_folder}\{name}.csv")
#     img_data = get_candidate_image(image)
#     with open(f"{path}\{name}_picture.jpg", 'wb') as handler:
#         handler.write(img_data)
#     #CV
#     cand_web = card_data['Website'].iloc[0]
#     cand_htm = requests.get(cand_web).content
#     cand_soup = BeautifulSoup(cand_htm, features="lxml")
#     cand_files = cand_soup.find_all('a',
#                                     attrs={'href': re.compile(".pdf|.doc|.txt")})
#     count = 0
#     for val in cand_files:
#         link = val.get('href')
#         #gets full url, joins to make formatting right
#         full_cand_url = urljoin(cand_web, link).replace(" ", "%20")
#         #print(full_cand_url)
#         #checks to see if request goes through
#         try:
#             urllib.request.urlretrieve(full_cand_url)
#         except Exception as e:
#             print("Error:", e, full_cand_url)
#             continue
#         # print(full_url)
#         #gets content of file
#         file_data = requests.get(full_cand_url).content
#         file_ending = full_cand_url.title().split('/')[-1].split('&')[0]
#         print("full URL:", full_cand_url, "file ending:", file_ending)
#         try:
#             with open(f"{path}\{name}_{file_ending}", 'wb') as handler:
#                 handler.write(file_data)
#         except Exception as e:
#             print("We are in exception now")
#             #print(e)
#             try:
#                 file_ending = full_cand_url.title().split('%2F')[-1].split('%3F')[0]
#                 file_ending = file_ending.split('&')[0].replace("%","")
#                 print("full URL2:", full_cand_url, "\nfile ending2:", file_ending)
#                 with open(f"{path}\{name}_{file_ending}", 'wb') as handler:
#                     #pdb.set_trace()
#                     handler.write(file_data)
#             except Exception as e:
#                 print("Error:", e, full_cand_url)
#
#             # if re.search("google", full_cand_url):
#             #     print("google thing")
#             #     file_ending = full_cand_url.title().split('%2F')[-1].split('&')[0]
#     card_df.append(card_data)
#





