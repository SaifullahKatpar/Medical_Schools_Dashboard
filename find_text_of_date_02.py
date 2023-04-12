import requests
import spacy
from spacy.matcher import Matcher

# Load the small English NLP model
nlp = spacy.load("en_core_web_sm")

# Define a pattern to match dates in various formats
#  date_pattern = [{"TEXT": {"REGEX": r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{1,2}\s+[A-Za-z]+\s+\d{2,4}|\d{1,2}[/-]\d{1,2}"}}]
date_pattern = [{"TEXT": {"REGEX": "November 15th"}}]

# Define a pattern to match text associated with dates
text_pattern = [{"LOWER": {"IN": ["deadline", "apply by", "application deadline", "closing date", "submission deadline"]}}]

# Initialize the matcher
matcher = Matcher(nlp.vocab)

# Add the date and text patterns to the matcher
matcher.add("DATE", [date_pattern])
matcher.add("TEXT", [text_pattern])

# Example usage

url = "https://www.hofstra.edu/admission/apply.html"
response = requests.get(url)
html_doc = ""
if response.status_code == 200:
    html_doc = response.text

doc = nlp(html_doc)
print(doc)
# Create a dictionary to store the results
results = {}

# Iterate over the matches and find the most suitable associated text
for match_id, start, end in matcher(doc):
    print(match_id, start, end)
    if nlp.vocab.strings[match_id] == "DATE":
        # Get the text of the matched span
        date_text = doc[start:end].text
        print(date_text)
        # Find the most suitable associated text
        max_similarity = -1
        associated_text = ""
        for sent in doc.sents:
            similarity = nlp(date_text).similarity(sent)
            if similarity > max_similarity:
                max_similarity = similarity
                associated_text = sent.text.strip()
        
        # Add the date and associated text to the results dictionary
        results[date_text] = associated_text

        # Stop if we've found 5 results
        if len(results) == 5:
            break

# Print the results
print(results)
