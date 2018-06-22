import os
import json
from pathlib import Path

import requests

from dotenv import load_dotenv


# Load environmental variables from .env file - you have to create one yourself!
ENV_PATH = Path('./') / '.env'
load_dotenv(dotenv_path=ENV_PATH)

# Load the value of API_KEY
API_KEY = os.getenv('API_KEY')

# Set some constants
BASE_URL = 'https://api.companieshouse.gov.uk/company/'

# Each CRN needs to be 8 characters long.
#The first two characters might be SC, which designates Scotland
#Example company number:
COMPANY_NUM = '00000006'

def pretty_print(data, indent=4):
    """Format data to be more readable."""
    if isinstance(data, dict):
        print(json.dumps(data, indent=indent, sort_keys=True))
    else:
        print(data)


def query_company_name(company_num):
    """
    Query Companies House API to get the company name for a given company registration number.
    A company registration number is a unique number issued by Companies House
    when a limited company or Limited Liability Partnership (LLP) is incorporated.
    INPUT: company registration number: string
    OUTPUT: company's registered name: string
    """
    # print("\nRetrieving name for company:{} ...".format(company_num))
    response = requests.get(BASE_URL + company_num, auth=(API_KEY, ''))
    # print("\nRetrieving name for company:{} ...".format(company_num))

    if response.status_code == requests.codes.ok:
        data = response.json()
        company_name = data["company_name"]
        # print(company_name)
        # print('Received a response with status code: ', response.status_code)
        return company_name
    else:
        return 'No name listed'
        # response.raise_for_status()

def query_officers_info(company_num):
    """
    Query Companies House API to get the officers' information for a company
    with a given company registration number.
    A company registration number is a unique number issued by Companies House
    when a limited company or Limited Liability Partnership (LLP) is incorporated.
    INPUT: company registration number: string
    OUTPUT: all officers' information for that company: JSON
    """
    response = requests.get(BASE_URL + company_num + '/officers', auth=(API_KEY, ''))
    # print("\nRetrieving officers' info for company:{} ...".format(company_num))

    if response.status_code == requests.codes.ok:
        # print('Received a response with status code: ', response.status_code)
        # pretty_print(response.json())
        return response.json()
    else:
        return 'CRN not listed with Companies House'
        # response.raise_for_status()

def format_active_officers_info(query_comp_name, query_off_info, company_num):
    """
    Format active officer information for one company into dictionary.
    INPUT:
    query_company_name: function
    query_officers_info: function
    company_num: string
    OUTPUT:
    Dictionary with following keys: 'Company_Name',
    'Company_Registration_Number', 'Number_Active_Officers',
    'Names_Active_Officers', 'Officers_Active_Full_Info'
    """
    company_name = query_comp_name(company_num)
    officers_data = query_off_info(company_num)
    if officers_data != 'CRN not listed with Companies House':
        num_active = int(officers_data["active_count"])
        # pretty_print(officers_data)
        # num_total = int(officers_data["total_results"])
        # print("\nTotal number of officers in company's history: ", num_total)
        # print("\nNumber of currently active officers: ", num_active)

        active_officer_names = []
        active_officer_info = []

        active_officers = list(
            filter(lambda officer: "resigned_on" not in officer, officers_data["items"])
            )
        for officer in active_officers:
            active_officer_names.append(officer["name"])
            active_officer_info.append(officer)
            # pretty_print(officer)

        company = {
            'Company_Name': company_name,
            'Company_Registration_Number': company_num,
            'Number_Active_Officers': num_active,
            'Names_Active_Officers': active_officer_names,
            'Officers_Active_Full_Info': active_officer_info,
        }
    else:
        company = '{} not registered with Companies House'.format(company_num)

    pretty_print(company)
    # Save the dictionary of active officer's information into a file

    # print('\nSaving active officers\' information for {}:{} into file {}.txt ...'
    #       .format(company_name, company_num, company_num))
    # with open(company_num + '.txt', 'w') as file:
    #     json.dump(company, file, indent=4)
    # return company
    # print('\nSaving active officers\' information...')
    with open('all_officers_information.txt', 'a') as file:
        json.dump(company, file, indent=4)
    return company



if __name__ == '__main__':
    format_active_officers_info(query_company_name, query_officers_info, COMPANY_NUM)
