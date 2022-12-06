
#Imports packages
from urllib.request import urlopen
from bs4 import BeautifulSoup
from FunctionClass import *
#from polyglot.text import Text
import pandas as pd
import re
#download spacy and proper language
import spacy

#download english (works for pycharm) lg for large, sm for small; use large if you expect foreign names
#spacy.cli.download("en_core_web_lg")

#all languages
#spacy.cli.download("xx_sent_ud_sm")

#spacy.cli.download('xx_ent_wiki_sm')
nlp = spacy.load('en_core_web_lg')

# URL to scrape
url = "https://economics.harvard.edu/job-market-candidates"

# collect HTML dta
html = urlopen(url)

# create beautiful soup object from HTML
soup = BeautifulSoup(html, features="lxml")


#gets raw text for analysis
raw_text = remove_style(soup)
#print(raw_text)

#Spacy Code
spacy_ent = nlp(raw_text)
#Polygot Code
#poly_ent = Text(raw_text)

# Identify the persons
spacy_persons = [ent.text for ent in spacy_ent.ents if ent.label_ == 'PERSON']
#poly_persons = [ent.text for ent in poly_persons.ents if ent.label_ == 'PERSON']
#print("Num: ",len(spacy_persons)," ", spacy_persons)
print("Num: ",len(spacy_ent.ents)," ", spacy_ent.ents)
print(spacy_ent.ents[59]," ", spacy_ent.ents[59].label_)
#print(raw_text)



