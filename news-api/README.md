# News API

## Introduction

In this section of the GenderPayGapHack, we explore the media coverage of gender paygap.

[News API](https://newsapi.org/) is an amazing source of information as it provides a single API that exposes breaking news headlines and older articles from over 3,000 news sources and blogs!

You can sign up to a free developer plan which allows 1,000 requets per day (with a limit of 250 requests per every 6 hours). This should be more than enough for the day of the hack. However, please be aware that it is possible to accidentally exceed the limit, e.g. by entering an infinite loop whilst making batch requests.

## Instructions

### Option 1: Use the dataset collected by GenderPayGap mentors

Mentors of the GenderPayGapHack joined force, analysed a large number of APIs, hand-picked ones that suited out purpose and have collected ready-to-use dataset in a form of JSON.

In case of News API, you can find it in [`news_api_data.txt`](./news_api_data.txt) - click the file name and it will take you to the file itself. You're welcome to download the file and explore the data. For a detailed explanation of the data structure, how to load the data from the file etc., pelase see the section [Working with the Data](#working-with-the-data).

### Option 2: Run a script to collect additional data

You can also use the script [`custom_query.py`](./custom_query.py) provided to make your own custom queries, should you wish so. In order to do this, you need a bit of preparation to get your local environment up and running.

#### Preparing your local environment

1. Clone the repository: `$ git clone git@github.com:paygaphack/mentors-repo.git`
2. Move into the `news-api` directory: `$ cd mentors-repo/news-api`
3. Create a virtual environment to manage local dependencies: `$ virtualenv venv`
4. Activate the virtual enviromnent just created: `$ source venv/bin/activate`
5. Install dependencies: `$ pip install -r requirements.txt`
6. Obtain a unique API key from [newsapi.org](https://newsapi.org/)
7. Create a `.env` file _within_ the `news-api` directory - it won't work otherwise!
    The file structure should look something like the diagram below.

    ```
    mentors-repo
    │   README.md
    │   LICENSE
    │   .gitignore  <-- any .env files are ignored here
    │   ...
    │
    └─── news-api
    │        .env  <-- here, not anywhere else!
    │        README.md
    │        custom_query.py
    │        generate_data.py
    │        load_data.py
    │        news_api_data.txt
    │        requirements.txt
    │      ...
    │
    └─── another-project
    │        ...
    │        ...
    │   ...
    ```

    **N.B.** The `.env` file is ignored in `.gitignore` file in the root of the project. This means that it will not get tracked by `git`, and hence will not be checked into your commits. This is important for security purposes, as you _never_ want to expose your credentials to publically available spaces!

8. Paste your API key to the `.env` file

    ```bash
    # .env

    API_KEY="YOUR API KEY"
    ```

9. Now you should be all ready to fire up a query: `$ python custom_query.py`
    If everything goes well, you should see the response printed out in the console and you should have a file called `data.txt` which stores the JSON data from the News API.

#### Customising a query

#### Endpoints

By default, `custom_query.py` makes a request to `/everthing` endpoint of News API. They provide two additional endpoints `/top-headlines` and `/sources`. [News API Endpoints](https://newsapi.org/docs/endpoints) explains what each endpoint provides.

You can change the endpoint to query by editing `base_url` variable inside `custom_query.py`.

```python
# custom_query.py

base_url = 'https://newsapi.org/v2/everything'
```

#### Parameters

You can also customise a query by changing parameters - this is where things get really exciting! So I encourage you to play around with it.

The default parameters in `custom_query.py` are below. You can add/remove parameters by adding/removing key-value pairs in the `params` dictionary.

```python
# custom_query.py

params = {
    'q': 'pay gap',
    'apiKey': API_KEY,
    'pageSize': 20,
    'page': 1
}
```

For each endpoint, there are a range of additional parameters you can specify, such as `sources`, `from`, `to`, `language`, `sortBy` etc. For example, for the list of parameters available for the `/everything` endpoint, check out the 'Request parameters' section on [News API Everything](https://newsapi.org/docs/endpoints/everything).

## Working with the Data

### 1. Data Structure

The typical JSON response from News API looks like this:

```json
{
    "status": "ok",
    "totalResults": 19,
    "articles": [
        {
            "source": {
                "id": null,
                "name": "Forbes.com"
            },
            "author": "Avivah Wittenberg-Cox, Contributor, Avivah Wittenberg-Cox, Contributor https://www.forbes.com/sites/avivahwittenbergcox/",
            "title": "Turning #PayGaps into #Potential",
            "description": "The UK legislates #PayGap reporting requirements while PEW Research publishes a new report about the #PromotionGap in the US. The push is on to #GenderBalance business.",
            "url": "https://www.forbes.com/forbes/welcome/?toURL=https://www.forbes.com/sites/avivahwittenbergcox/2018/05/06/turning-paygaps-into-potential/&refURL=https://t.co/e7844fec73&referrer=https://t.co/e7844fec73",
            "urlToImage": null,
            "publishedAt": "2018-05-06T20:27:00Z"
        },
        {
            "source": {
                "id": null,
                "name": "Forbes.com"
            },
            "author": "Avivah Wittenberg-Cox, Contributor, Avivah Wittenberg-Cox, Contributor https://www.forbes.com/sites/avivahwittenbergcox/",
            "title": "Turning #PayGaps into #Potential",
            "description": "The UK legislates #PayGap reporting requirements while PEW Research publishes a new report about the #PromotionGap in the US. The push is on to #GenderBalance business.",
            "url": "https://www.forbes.com/forbes/welcome/?toURL=https://www.forbes.com/sites/avivahwittenbergcox/2018/05/06/turning-paygaps-into-potential/&ss=business&refURL=https://t.co/dbd29f1cbc&referrer=https://t.co/dbd29f1cbc",
            "urlToImage": null,
            "publishedAt": "2018-05-06T20:27:00Z"
        }
    ]
}
```

### 2. Loading data from a text file

Here is an example of how you can load the file as a JSON object in Python.

```python
import json

with open('news-api.txt','r') as file:
    data = json.load(file)
```

### 3. Access information within the data

Now you can access each field as follows - the below uses `python-dateutil` package to parse the `publishedAt` attribute which is in ISO 8601 format.

```python
import dateutil.parser

for article in data['articles']:
    published_datetime = dateutil.parser.parse(article['publishedAt'])

    print('\n')
    print('Source: ', article['source']['name'])
    print('Title: ', article['title'])
    print('Written by: ', article['author'])
    print('Published at:', published_datetime)
    print('URL: ', article['url'])

>>>
Source:  Forbes.com
Title:  Turning #PayGaps into #Potential
Written by:  Avivah Wittenberg-Cox, Contributor, Avivah Wittenberg-Cox, Contributor https://www.forbes.com/sites/avivahwittenbergcox/
Published at: 2018-05-06 20:27:00+00:00
URL:  https://www.forbes.com/forbes/welcome/?toURL=https://www.forbes.com/sites/avivahwittenbergcox/2018/05/06/turning-paygaps-into-potential/&ss=business&refURL=https://t.co/dbd29f1cbc&referrer=https://t.co/dbd29f1cbc

Source:  Forbes.com
Title:  Turning #PayGaps into #Potential
Written by:  Avivah Wittenberg-Cox, Contributor, Avivah Wittenberg-Cox, Contributor https://www.forbes.com/sites/avivahwittenbergcox/
Published at: 2018-05-06 20:27:00+00:00
URL:  https://www.forbes.com/forbes/welcome/?toURL=https://www.forbes.com/sites/avivahwittenbergcox/2018/05/06/turning-paygaps-into-potential/&refURL=https://t.co/e7844fec73&referrer=https://t.co/e7844fec73

...
```

## Curated by

### Misa Ogura

Software Engineer @ [BBC R&D](https://www.bbc.co.uk/rd/blog)

Organiser @ [AI Club for Gender Minorities](https://www.meetup.com/en-AU/ai-club/)

[Github](https://github.com/MisaOgura) | [Twitter](https://twitter.com/misa_ogura) | [Medium](https://medium.com/@misaogura/latest)
