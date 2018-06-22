#  🏢 Companies House API 🏦

## Table of Contents

1. [Introduction](#one-introduction)
2. [Instructions](#two-instructions)
    - Option 1 - Use the dataset prepared by GenderPayGap mentors
    - Option 2 - Run a script to collect additional data
        - Preparing your local environment
3. [Working with the Data](#three-working-with-the-data)
    - Data structure
4. [Contributions](#four-contributions)
5. [Author](#five-authour)

## :one: Introduction

In this section of the GenderPayGapHack, we explore the the 💷UK Gender Pay Gap Data 💷 and UK company information as returned by querying the UK Companies House API. We will initially be focusing on information regarding active company officers.

[Companies House API](https://developer.companieshouse.gov.uk/api/docs/index/gettingStarted/quickStart.html) is an authoritative source of company information: it provides a single API that exposes all company information delivered under the Companies Act and related legislation.

To be able to explore and query the Companies House API, you need to register a free [user account](https://account.companieshouse.gov.uk/oauth2/user/signin) with Companies House, and then generate an API key for use in each API request. 

Rate limiting is applied to the Companies House API: You can make up to 600 requests within a five-minute period. If you exceed this limit, you will receive a `429 Too Many Requests` HTTP status code for each request made within the remainder of the five-minute window. At the end of the period, your rate limit will reset back to its maximum value of 600 requests. This should be more than enough for you to play around on the day of the hack. However, please be aware that it _is_ possible to accidentally exceed the limit, e.g. by entering an infinite loop whilst making batch requests... :see_no_evil:

## :two: Instructions
There are two options for you to work on this topic.

### Option 1 - Use precollected dataset

Mentors of the GenderPayGapHack joined force :muscle::boom:

We analysed a large number of APIs, hand-picked ones that suited our purpose, and have created ready-to-use datasets.

In case of Companies House API, we collected officer information for each currently active officer of the 10,000+ companies that supplied the data that makes up the UK Gender Pay Gap Data. The exact query used to collect this data can be found in [`query_csv_for_all_CRNs.ipynb`](./query_csv_for_all_CRNs.ipynb), and you can find the data in the Google Drive of collected data that we have gathered for this data hack.

You're welcome to download the file from the Google Drive and explore the data. Alternatively, you can run the Jupyter notebook file, [`query_csv_for_all_CRNs.ipynb`](./query_csv_for_all_CRNs.ipynb), to run the scripts to collect the currently active officers data from Companies House and store that data in a file called `all_officers_information.txt`.

### Option 2 - Run a script to collect additional data

You can also use the script [`query_companies_house.py`](./query_companies_house.py) provided in this directory as well to query Companies House. An example script of how you could select a set of Company Registration Numbers to use to query the Companies House API can be found in [`demo_code_for_querying_csv.ipynb`](./demo_code_for_querying_csv.ipynb). The results of that demo query can be found in [`demo_officers_information.txt`](./demo_officers_information.txt).

We use [Requests](http://docs.python-requests.org/en/master/) to make HTTP GET requests to the Companies House API. This is a great opportunity to learn about Requests if you aren't familiar, as you can make HTTP to any APIs you can think of with Requests under your toolbelt. It's a really powerful tool :)

Right, in order to start making queries, you need a bit of preparation to get your local environment up and running.

#### :floppy_disk: Preparing your local environment

1. Clone the repository: `$ git clone git@github.com:paygaphack/mentors-repo.git`
2. Move into the `companies-house-api` directory: `$ cd mentors-repo/companies-house-api`
3. Create a virtual environment with the dependencies listed in `environment.yaml`: `$ conda env create -f environment.yaml`
4. Activate the virtual enviromnent just created: `$ source activate companies-house-api`
5. Obtain a unique API key from [Companies House API: Authorisation](https://developer.companieshouse.gov.uk/api/docs/index/gettingStarted/apikey_authorisation.html)
6. Create a `.env` file :exclamation:within:exclamation: the `companies-house-api` directory
    It won't work otherwise, unless you manually change the path to the `.env` file by modifying the `env_path` variable in `query_companies_house.py`. The file structure should look something like the diagram below.
    
    ```
    mentors-repo  <-- Project root
    │   README.md
    │   LICENSE
    │   .gitignore  <-- Any .env files are ignored here
    │   ...
    │
    └─── companies-house-api
    │        .env  <-- Here!
    │        README.md
    │        query_companies_house.py
    │        query_csv_for_all_CRNs.ipynb
    │        demo_code_for_querying_csv.ipynb
    |        demo_officers_information.txt
    │        environment.yaml
    |        UK_Gender_Pay_Gap_Data_2017_to_2018.csv
    │      ...
    │
    └─── another-project
    │        ...
    │        ...
    │   ...
    ```
    
      **:closed_book: N.B.** The `.env` file is ignored in `.gitignore` file in the root of the project. This means that it will not get tracked by `git`, and hence will not be checked into your commits. This is important for security purposes, as you _never_ want to expose your credentials to publically available spaces :no_good:

7. Paste your API key to the `.env` file

    ```bash
    # .env

    API_KEY="YOUR API KEY"
    ```

8. Now you should be all ready to fire up a query :boom: `$ python query_companies_house.py`
    If everything goes well, you should see the response printed out in the console and you should have a file called `all_officers_information.txt` which stores a dictionary of data holding active officers' information returned from the Companies House API for the company with the Company Registration Number "00000006".
    If you would like your file to match the company number, find the following commented out code in `all_officers_information.txt`:
    
    ``` python
    # with open(company_num + '.txt', 'w') as file:
    #     json.dump(company, file, indent=4)
    # return company
    ```
    
Uncomment that code and comment out the code (below) stating:

    ``` python
    with open('all_officers_information.txt', 'a') as file:
        json.dump(company, file, indent=4)
    return company
    ```
    
## :three: Working with the Data

### :page_with_curl: Data structure

For querying active officers information we have constructed a dictionary to structure the data we are gathering, which looks like this:

```python
{
    "Company_Name": "MARINE AND GENERAL MUTUAL LIFE ASSURANCE SOCIETY",
    "Company_Registration_Number": "00000006",
    "Number_Active_Officers": 3,
    "Names_Active_Officers": [
        "PRINGLE, Martin",
        "GALBRAITH, James",
        "WALKER, Michael John"
    ],
    "Officers_Active_Full_Info": [
        {
            "officer_role": "secretary",
            "links": {
                "officer": {
                    "appointments": "/officers/1UUfj2gDv9ZVoykvoy9hhEhXDcY/appointments"
                }
            },
            "address": {
                "premises": "Cms Cameron Mckenna Llp",
                "country": "England",
                "locality": "London",
                "address_line_2": "78 Cannon Street",
                "address_line_1": "Cannon Place",
                "postal_code": "EC4N 6AF"
            },
            "name": "PRINGLE, Martin",
            "appointed_on": "2016-09-13"
        },
        {
            "links": {
                "officer": {
                    "appointments": "/officers/I-4OI1Rt7bqjbeWflGDl_s6KG6s/appointments"
                }
            },
            "address": {
                "address_line_2": "78 Cannon Street",
                "locality": "London",
                "premises": "Cms Cameron Mckenna Llp",
                "address_line_1": "Cannon Place",
                "postal_code": "EC4N 6AF",
                "country": "England"
            },
            "occupation": "Company Director",
            "appointed_on": "2015-03-01",
            "country_of_residence": "United Kingdom",
            "officer_role": "director",
            "name": "GALBRAITH, James",
            "date_of_birth": {
                "month": 3,
                "year": 1963
            },
            "nationality": "British"
        },
        {
            "links": {
                "officer": {
                    "appointments": "/officers/Z7im4wk4V9mVRJ06XtXntHRjihI/appointments"
                }
            },
            "address": {
                "locality": "London",
                "country": "England",
                "postal_code": "EC4N 6AF",
                "address_line_2": "78 Cannon Street",
                "address_line_1": "Cannon Place",
                "premises": "Cms Cameron Mckenna Llp"
            },
            "occupation": "Company Director",
            "appointed_on": "2015-06-01",
            "country_of_residence": "United Kingdom",
            "officer_role": "director",
            "name": "WALKER, Michael John",
            "date_of_birth": {
                "year": 1952,
                "month": 10
            },
            "nationality": "British"
        }
    ]
}
```

The Companies House API itself returns a JSON data structure that is described in the `CompanySearch resource` section on [Companies House API](https://developer.companieshouse.gov.uk/api/docs/search-overview/CompanySearch-resource.html) :point_left:

Feel free to construct your own custom queries of the Companies House API. You can query for lots more data than just information on active officers!

## :four: Contributions

Please raise issues or pull requests as you see room for improvement :pray:

## :five: Author

### Kara de la Marck

[Github](https://github.com/MarkK) | [Twitter](https://twitter.com/karamarck) | [Medium](https://medium.com/@karadelamarck)

:rainbow: Organiser @ [codebar](https://codebar.io/)

