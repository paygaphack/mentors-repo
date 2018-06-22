import json
import requests
from bs4 import BeautifulSoup

print('\nLoading data...')

# Load JSON data
with open('results.txt','r') as file:
    data = json.load(file)

for i, job in enumerate(data['results']):
    print('\nScraping a job summary for job no. ', i+1)

    res = requests.get(job['url'])
    soup = BeautifulSoup(res.text,'lxml')
    summary = soup.find(id='job_summary')
    job['jobsummary'] = str(summary)

with open('results_with_summary.txt', 'w') as file:
    json.dump(data, file, indent=4)
print('\nData saved as results_with_summary.txt!')
