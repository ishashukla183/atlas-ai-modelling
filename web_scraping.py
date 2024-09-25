import requests
from bs4 import BeautifulSoup
import re
import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('names')  # Optional for checking names
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')
# URL of the website

# Send a GET request to the website
def classify_locations(tagged_words):
    locations = []
    for word, tag in tagged_words:
        if tag == 'NNP':  # Proper Noun, Singular
            # A simple heuristic to differentiate cities and countries
            if word in ['Pune', 'Paris', 'New York', 'Tokyo']:
                locations.append((word, 'city'))
            elif word in ['India', 'France', 'China', 'Japan']:
                locations.append((word, 'country'))
    return locations

locations = []
def get_data(place):
    base_url = "https://www.holidify.com/"
    country = 'country/'
    city = 'places/pune'
    response = requests.get(base_url + city + place)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract all text from the page
        div_container = soup.find('div', class_='col-lg-8 pr-lg-2')
        
        if div_container:
            # Extract all text from the found div
            div_text = div_container.get_text(separator='\n', strip=True)
            text = re.sub(r'Read more', '', div_text)
            text = re.sub(r'Places To Visit', '', div_text)
            # Step 2: Remove text between "Top Stories about Pune" and "FAQs on Pune"
            text = re.sub(r'Top Stories about*?FAQs', '', text, flags=re.DOTALL)

            # Print the cleaned text
            return text.strip()
    else:
        return "Failed to retrieve the webpage: {response.status_code}"
