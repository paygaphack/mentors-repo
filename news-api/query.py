import os
import json
import requests

from dotenv import load_dotenv
from pathlib import Path

env_path = Path('./') / '.env'
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv('API_KEY')

base_url = 'https://newsapi.org/v2/everything'
params = {
    'q': 'paygap',
    'apiKey': API_KEY
}

response = requests.get(base_url, params=params)
data = response.json()

with open('news-api.txt', 'w') as file:
    json.dump(data, file, indent=4)

with open('news-api.txt','r') as file:
    data = json.load(file)
    print('Number of articles grabbed: ', data['totalResults'])
