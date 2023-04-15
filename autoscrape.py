import requests
from autoscraper import AutoScraper
import spacy
from spacy.matcher import Matcher

# Define the URL and CSS selector for the submission date
url = 'https://www.hofstra.edu/admission/apply.html'
css_selector = 'table td:nth-of-type(2)'

# Use AutoScraper to extract the submission date
scraper = AutoScraper()
submission_date = scraper.build(url, css_selector)
submission_date = scraper.get_result_similar(url)[0]

print('Submission Date:', submission_date)

# Use a machine learning-based approach to extract the submission date
# Load the English language model
nlp = spacy.load('en_core_web_sm')

# Define the pattern to match the submission date
pattern = [{'LOWER': 'submission'}, {'IS_PUNCT': True, 'OP': '?'}, {'LOWER': 'date'}]

# Define a function to extract the submission date using the pattern
def extract_submission_date(text):
    doc = nlp(text)
    matcher = Matcher(nlp.vocab)
    matcher.add('Submission Date', [pattern])
    matches = matcher(doc)
    if len(matches) > 0:
        start, end = matches[0][1:3]
        submission_date = doc[start:end].text.strip()
        return submission_date

# Define the URL to scrape
url = 'https://www.hofstra.edu/admission/apply.html'

# Send a GET request to the URL and get the HTML content
response = requests.get(url)
html_content = response.text

# Extract the submission date from the HTML content using the function
submission_date = extract_submission_date(html_content)

print('Submission Date:', submission_date)
