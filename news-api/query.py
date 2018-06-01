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

# Construct base_url and parameters to send
base_url = 'https://newsapi.org/v2/everything'
params = {
    'q': 'paygap',
    'apiKey': API_KEY
}

# Get data from News API with the parameters set above
response = requests.get(base_url, params=params)

# Save the JSON representation of the response data into a file
with open('news-api.txt', 'w') as file:
    json.dump(response.json(), file, indent=4)

# Load JSON data
with open('news-api.txt','r') as file:
    data = json.load(file)

# Print the data
print(json.dumps(data, indent=4))
