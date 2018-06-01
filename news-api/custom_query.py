import os
import json
import requests
import dateutil.parser

from dotenv import load_dotenv
from pathlib import Path

# Load environmental variables from .env file - you have to create one yourself!
env_path = Path('./') / '.env'
load_dotenv(dotenv_path=env_path)

# Load the value of API_KEY
API_KEY = os.getenv('API_KEY')

# Construct base_url and parameters to send
base_url = 'https://newsapi.org/v2/everything'
params = {
    'q': 'pay gap',
    'apiKey': API_KEY
}

# Get data from News API with the parameters set above
response = requests.get(base_url, params=params)

# Extract the JSON representation of the response data
data = response.json()
print(len(data['articles']), 'articles found!')

# Save the JSON representation of the response data into a file
with open('data.txt', 'w') as file:
    json.dump(data, file, indent=4)

# Load the JSON data
with open('data.txt','r') as file:
    data = json.load(file)

# Access information within the data - showing first 5 for demo purposes
print('Displaying information on the first 5 articles...')
for article in data['articles'][:5]:
    published_datetime = dateutil.parser.parse(article['publishedAt'])

    print('\n')
    print('Source: ', article['source']['name'])
    print('Title: ', article['title'])
    print('Written by: ', article['author'])
    print('Published at:', published_datetime)
    print('URL: ', article['url'])
