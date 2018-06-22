# :mag: :mag_right: Indeed Job Search API :chart_with_upwards_trend:

## Table of Contents

1. [Introduction](#one-introduction)
2. [Instructions](#two-instructions)
    - Option 1 - Use the dataset prepared by GenderPayGap mentors
    - Option 2 - Run a script to collect additional data
        - Preparing your local environment
        - Customising a query - parameters
        - Web scraping to get job summaries
3. [Working with the Data](#three-working-with-the-data)
    - Data structure
    - Loading data from a text file
    - Access information within the data
4. [Contributions](#four-contributions)
5. [Authour](#five-authour)

## :one: Introduction

We've partnered up with [Indeed Open Source Team](https://opensource.indeedeng.io/) to provide you with an access to their [Job Search API](http://opensource.indeedeng.io/api-documentation/docs/job-search/) for the duration of the Hack :tada:

Please Note that you will have to sign the Data Agreement Form in order to use the Indeed API. Speak to the organisers for more details.

## :two: Instructions

There are two options for you to work on this topic.

### Option 1 - Use pre-collected dataset

Mentors of the Gender Pay Gap Hack have analysed a large number of APIs, hand-picked ones that suited our purpose and have collected ready-to-use dataset in a form of JSON.

In case of Indeed Job Search API, we collected data on the UK job advertisement. You can find two files, `job_ad_fulltime_with_summary.txt` and `job_ad_parttime_with_summary`, in the **Google Drive** (which is available to the participants of the Hack) under `Gender Pay Gap Hack Data > indeed_job_search_api`. Each file contains 1000 job ads for full/part-time positions in JSON format, collected on the 22nd June 2018.

You're welcome to download the files (~3MB each) and explore the data. For a detailed explanation of the data structure, how to load the data from the file etc., pelase see the section [:three: Working with the Data](#working-with-the-data).

### Option 2 - Run a script to collect your own data

You can also use the script [`make_query.py`](./make_query.py) provided in this directory as well to make your own custom queries, should you wish so.

We use [Requests](http://docs.python-requests.org/en/master/) to make HTTP GET requests to the Indeed API. This is a great opportunity to learn about Requests if you aren't familiar, as you can make HTTP to any APIs you can think of with Request. It really is a powerful tool to have under your toolbelt :)

Right, in order to start making queries, you need a bit of preparation to get your local environment up and running.

#### :floppy_disk: Preparing your local environment

1. Clone the repository: `$ git clone git@github.com:paygaphack/mentors-repo.git`
2. Move into the `indeed-api` directory: `$ cd mentors-repo/indeed-api`
3. Create a virtual environment to manage local dependencies: `$ virtualenv venv`
4. Activate the virtual enviromnent just created: `$ source venv/bin/activate`
5. Install dependencies: `$ pip install -r requirements.txt`
6. Obtain a publisher ID - You need this ID to make a query. We have a unique publisher ID provided by Indeed so please ask organisers to gain access.
7. Create a `.env` file :exclamation:within:exclamation: the `indeed-api` directory
    It won't work otherwise, unless you manually change the path to the `.env` file by modifying the `env_path` variable in `make_query.py`. The file structure should look something like the diagram below.

    ```
    mentors-repo  <-- Project root
    │   README.md
    │   LICENSE
    │   .gitignore  <-- Any .env files are ignored here
    │   ...
    │
    └─── indeed-api
    │        .env  <-- Here!
    │        README.md
    │        make_query.py
    │        requirements.txt
    │      ...
    │
    └─── another-project
    │        ...
    │        ...
    │   ...
    ```

    **:closed_book: N.B.** The `.env` file is ignored in `.gitignore` file in the root of the project. This means that it will not get tracked by `git`, and hence will not be checked into your commits. This is important for security purposes, as you _never_ want to expose your credentials to publically available spaces :no_good:

8. Paste your API key to the `.env` file

    ```bash
    # .env

    PUBLISHER_ID="INSERT THE PUBLISHER ID PROVIDED BY THE GENDER PAY GAP HACK"
    ```

9. Now you should be all ready to fire up a query :boom: `$ python make_query.py`
    If everything goes well, you should see the response printed out in the console and you should have a file called `results.txt` which stores the JSON data from the News API :100:

#### :wrench: Customising a query - parameters

You can also customise a query by changing parameters - this is where things get really exciting! So I encourage you to play around with it.

You can add/remove parameters by adding/removing key-value pairs in the `params` dictionary in `make_query.py`.

```python
# make_query.py

params = {
        'publisher': PUBLISHER_ID,
        'v': 2,
        'userip': '1.2.3.4',
        'useragent': 'Mozilla/%2F4.0%28Firefox%29',
        ...
}
```

There are a range of additional parameters you can specify. For the list of required and optional parameters available, check out the `Request parameters` section on [Indeed API](http://opensource.indeedeng.io/api-documentation/docs/job-search/#request_params) :point_left:

#### :scissors: Web scraping to get job summaries

The raw data from the Indeed API doesn't contain the full job summary, so I've made a little tool for you to perform a simple web scraping using [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)!

The command `$ python scrape_job_summary.py` will load the data from `results.txt` and create a new file `results_with_summary.txt` with provide an additional field `jobsummary` in each job listing.

Feel free to edit [`scrape_job_summary.py`](./scrape_job_summary.py) to explore other parts of the job ad page. For a details guide on how to search through the HTML tree, see [Searching the tree - BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#searching-the-tree).

## :three: Working with the Data

### :page_with_curl: Data structure

The typical JSON response from the Indeed API looks like this:

```json
{
    "version":2,
    "query":"java",
    "location":"austin, tx",
    "dupefilter":true,
    "highlight":false,
    "radius":25,
    "start":1,
    "end":10,
    "totalResults":547,
    "pageNumber":0,
    "results":[
        {
            "jobtitle":"Java Developer",
            "company":"XYZ Corp.,",
            "city":"Austin",
            "state":"TX",
            "country":"US",
            "formattedLocation":"Austin, TX",
            "source":"Dice",
            "date":"Mon, 02 Aug 2017 16:21:00 GMT",
            "snippet":"looking for an object-oriented Java Developer... Java Servlets,
              HTML, JavaScript, AJAX, Struts, Struts2, JSF) desirable. Familiarity with
              Tomcat and the Java...",
            "url":"http://www.indeed.com/viewjob?jk=12345&indpubnum=8343699265155203",
            "onmousedown":"indeed_clk(this, '0000');",
            "latitude":30.27127,
            "longitude":-97.74103,
            "jobkey":"12345",
            "sponsored":false,
            "expired":false,
            "indeedApply":true,
            "formattedLocationFull":"Austin, TX",
            "formattedRelativeTime":"11 hours ago"
        },
        ...
    ]
}
```

### :open_file_folder: Loading data from a text file

Here is an example of how you can load the file as a JSON object in Python.

```python
import json

with open('results.txt','r') as file:
    data = json.load(file)
```

### :mag: Access information within the data

In addition to the default fields included in the response from the Indeed API, we've scraped a job summary for each of the job listed in the pre-collected data. You can access this field by `jobsummary` key.

```python
import json

with open('results.txt','r') as file:
    data = json.load(file)

# Display the first 5 ad for the demo purposes
for job in data['results'][:5]:
    print('\n')
    print('Job title: ', job['jobtitle'])
    print('Company: ', job['company'])
    print('Published at:', job['date'])
    print('Ad URL: ', job['url'])
    # The jobsummary field is available only if you're using
    # the pre-collected data from Google Drive
    print('Job summary: ', job['jobsummary'])
```

`Console output:`

```bash
Job title:  2018/19 Harris Graduate Programme: Secondary
Company:  Harris Careers
Published at: Fri, 22 Jun 2018 04:02:55 GMT
Ad URL:  http://www.indeed.co.uk/viewjob?jk=5b20a1592d2070b8&qd=mHFQcpl_OaqIVTVGDYekBXV_4rg2L80VOjCoqhu_1AwgUjoGejpdjAy2DfIGiz8Rt4ktpMxAsqevVvnOQ1EQi1TxwzEI1cHxqPLo224HsqA&indpubnum=264110024291313&atk=1cgjblkqo1d5v4lg
Job summary:  <span class="summary" id="job_summary"><div><p>If you are a recent graduate who is passionate about helping children achieve their potential, our Graduate Programme is for you.</p> ... </div></span>

Job title:  Receptionist -Beckenham Beacon Hospital Outpatients
Company:  King\'s College Hospital NHS Foundation Trust
Published at: Fri, 22 Jun 2018 06:06:14 GMT
Ad URL:  http://www.indeed.co.uk/viewjob?jk=fa7b15055f716884&qd=mHFQcpl_OaqIVTVGDYekBXV_4rg2L80VOjCoqhu_1AwgUjoGejpdjAy2DfIGiz8Rt4ktpMxAsqevVvnOQ1EQi1TxwzEI1cHxqPLo224HsqA&indpubnum=264110024291313&atk=1cgjblkqo1d5v4lg
Job summary: ...

...
```

## :four: Contributions

Please feel free to raise issues or pull requests as you see room for improvement :pray:

## :five: Authour

### Misa Ogura

:computer: Software Engineer @ [BBC R&D](https://www.bbc.co.uk/rd/blog)

:rainbow: Organiser @ [AI Club for Gender Minorities](https://www.meetup.com/en-AU/ai-club/)

[Github](https://github.com/MisaOgura) | [Twitter](https://twitter.com/misa_ogura) | [Medium](https://medium.com/@misaogura/latest)
