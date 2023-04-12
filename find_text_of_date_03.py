import requests
from bs4 import BeautifulSoup
import spacy

# Load the Spacy pipeline
nlp = spacy.load("en_core_web_sm")

# Make a request to the URL and get the HTML content
url = "https://www.hofstra.edu/admission/apply.html"
response = requests.get(url)
html_content = response.content

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Extract the text from the HTML
text = soup.get_text()

# Process the text using Spacy NER
doc = nlp(text)
for ent in doc.ents:
    if ent.label_ == "DATE":
        date_text = ent.text
        associated_text = ent.sent.text
        print(f"Date: {date_text}, Associated Text: {associated_text}")
