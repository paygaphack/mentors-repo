import os
import json
import requests

from dotenv import load_dotenv
from pathlib import Path

# Load environmental variables from .env file - you have to create one yourself!
env_path = Path('./') / '.env'
load_dotenv(dotenv_path=env_path)

# Load the value of API_KEY
API_KEY = os.getenv('API_KEY')

# Set some constants
PAGE_SIZE = 100

# Construct base_url and parameters to send
base_url = 'https://newsapi.org/v2/everything'
params = {
    'q': 'gender pay gap',
    'apiKey': API_KEY,
    'sortBy': 'publishedAt',
    'pageSize': PAGE_SIZE,
    'page': 1,
}

# Get the first set of data from News API with the parameters set above
response = requests.get(base_url, params=params)

# Extract the JSON representation of the response data
data = response.json()

# Calculate total number of pages to paginate through
total_results = data['totalResults']

if total_results <= 100:
    total_pages = 1
elif total_results % PAGE_SIZE == 0:
    total_pages = total_results / PAGE_SIZE
else:
    total_pages = int(total_results / PAGE_SIZE) + 1

print('Total number of pages to paginate: ', total_pages, '\n')
current_page = 1

# Grab the rest of the articles by paginating 100 articles at a time
while current_page < total_pages:
    # Increment current_page and set it to the page param
    current_page += 1
    params['page'] = current_page

    # Obtain next page from the API
    print('Grabbing page: ', current_page, '...')
    response = requests.get(base_url, params=params)
    new_data = response.json()

    if 'articles' not in new_data:
        break

    new_articles = new_data['articles']

    # Merge new articles to the obtained list of articles
    data['articles'].extend(new_articles)

print('\nTotal number of articles obtained: ', len(data['articles']))
print('\nSaving the data into a file...')

# Save the data into a file
with open('news_api_data.txt', 'w') as file:
    json.dump(data, file, indent=4)

print('\nData saved as news_api_data.txt!')
