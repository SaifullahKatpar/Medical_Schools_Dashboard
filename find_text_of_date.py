from dateutil import parser
import spacy
from spacy.matcher import Matcher
from spacy.lang.en import English
from bs4 import BeautifulSoup
import re
import requests

nlp = spacy.load("en_core_web_sm")

url = 'https://www.hofstra.edu/admission/apply.html'
response = requests.get(url)
html = response.content
# Extract text content from HTML using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
text = soup.get_text()
unique_matches = ['November 15, 2023','May 1, 2023']

# Convert matches to datetime objects
date_objs = [nlp(match)[0] for match in unique_matches]

# Use spaCy's named entity recognition (NER) to find associated text labels
doc = nlp(text)
labels = []
for ent in doc.ents:
    if ent.label_ == "DATE" and ent in date_objs:
        # Find the sentence containing the date
        sent = ent.sent
        # Find the text associated with the date label
        label = sent.text.replace(str(ent), "").strip()
        labels.append(label)

# Return a list of tuples containing the matched dates and their associated text labels
results = list(zip(unique_matches, labels))
print(results)