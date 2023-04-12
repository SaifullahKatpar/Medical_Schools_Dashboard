import requests
import spacy
from spacy.matcher import Matcher
import re
# Load the English language model in spaCy
nlp = spacy.load("en_core_web_sm")

# Define a pattern to match dates in various formats
date_pattern = r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{1,2}\s+[A-Za-z]+\s+\d{2,4}|\d{1,2}[/-]\d{1,2}'
# date_pattern = r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\b(?:[ ./-]*\d{1,2}[ ./-]*(?:\d{2,4})?)?'        # Extract the HTML content from the response.

# Define a pattern to match associated text
text_pattern = r'.{0,50}(Submission|Deadline|Due Date|Application Deadline|Last Date to Apply).{0,50}'

# Define a spaCy matcher to find the date and associated text
matcher = Matcher(nlp.vocab)
matcher.add("Date", [{"TEXT": {"REGEX": date_pattern}}])
matcher.add("Text", [{"TEXT": {"REGEX": text_pattern}}])

# Define a function to find the most suitable phrase for a given date
def find_associated_text(html, date):
    # Parse the HTML with spaCy
    doc = nlp(html)

    # Find all matches of the date pattern using the matcher
    date_matches = matcher("Date", doc)

    # Iterate over the date matches and find the most suitable phrase
    best_match = None
    best_score = 0
    for _, start, end in date_matches:
        date_text = doc[start:end].text
        score = date_text.similarity(nlp(date))
        if score > best_score:
            # Find all matches of the text pattern within 50 characters of the date
            text_matches = matcher("Text", doc[start-50:end+50])
            for _, start_text, end_text in text_matches:
                text = doc[start_text:end_text].text
                if best_match is None or score > best_score:
                    best_match = text
                    best_score = score

    # Return the most suitable phrase
    return best_match

# Example usage
url = "https://www.hofstra.edu/admission/apply.html"
response = requests.get(url)
if response.status_code == 200:
    html = response.text
    dates = re.findall(date_pattern, html)
    for date in dates:
        text = find_associated_text(html, date)
        print(f"{date}: {text}")
else:
    print(f"Failed to retrieve HTML: {response.status_code}")
