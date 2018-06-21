import os
import json
import requests
from time import sleep

from dotenv import load_dotenv
from pathlib import Path

# Load environmental variables from .env file - you have to create one yourself!
env_path = Path('./') / '.env'
load_dotenv(dotenv_path=env_path)

# Load the value of PUBLISHER_ID
PUBLISHER_ID = os.getenv('PUBLISHER_ID')

# Set some constants
PAGE_SIZE = 25
BASE_URL = 'http://api.indeed.com/ads/apisearch'

def run():
    # Construct parameters to send, pagination starts from 0
    current_page = 0
    params = {
        'publisher': PUBLISHER_ID,
        'v': 2,
        'userip': '1.2.3.4',
        'useragent': 'Mozilla/%2F4.0%28Firefox%29',
        'q': '*',
        'sort': 'date',
        'format': 'json',
        'co': 'gb',
        'start': 0,
        'limit': PAGE_SIZE
    }

    # Get the first set of data from News API with the parameters set above
    print('\nGrabbing the first page...')
    response = requests.get(BASE_URL, params=params)

    # Printing status for debugging
    print('Received a response with status code: ', response.status_code)

    # Extract the JSON representation of the response data
    data = response.json()

    # Calculate total number of pages to paginate through
    total_results = data['totalResults']
    total_pages = calculate_total_pages(PAGE_SIZE, total_results)
    print('Total number of pages to paginate: ', total_pages, '\n')

    # Grab the rest of the articles by paginating 25 results at a time
    while current_page < total_pages:
        # Increment current_page and set it to the page param
        current_page += 1
        params['start'] = current_page * 25

        # Obtain next page from the API
        print('\nGrabbing page: ', current_page, '...')
        response = requests.get(BASE_URL, params=params)

        # Printing status for debugging
        print('Received a response with status code: ', response.status_code)

        # Breaks out from the while loop if the request fails
        new_data = response.json()
        if 'results' not in new_data:
            break

        # Merge new articles to the obtained list of articles
        new_articles = new_data['results']
        data['results'].extend(new_articles)

    print('\nTotal number of articles obtained: ', len(data['results']))

    # Save the data into a file
    print('\nSaving the data into a file...')
    with open('example.txt', 'w') as file:
        json.dump(data, file, indent=4)
    print('\nData saved as example.txt!')


def calculate_total_pages(page_size, total_results):
    if total_results <= 100:
        return 1
    elif total_results % PAGE_SIZE == 0:
        return int(total_results / PAGE_SIZE)
    else:
        return int(total_results / PAGE_SIZE) + 1


if __name__ == '__main__':
    run()
