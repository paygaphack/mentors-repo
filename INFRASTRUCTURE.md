# Infrastructure 

Proposals for computing infrastructure to use during the PayGap hackathon.

## Key Questions

1. How will we distribute hackathon data for attendees (csv files on Github, shared cloud based SQL/non-SQL database, files hosted on S3 or another cloud provider)?
2. Do we need to store data in a database? Where will this database be hosted?
3. Is everyone comfortable using Python for data analysis?
4. Where will the final results of the project be stored? Github or another service? What format should the final presentation be in?

## Colaboratory
(Colaboratory)[https://colab.research.google.com] is an interactive, browser-based computing environment that supports Python 2 and Python 3 and also provides free GPU time. 

Pros:
* can connect to a user's Google Drive
* can easily upload notebooks to Github from Colaboratory UI
* can collaborativey edit notebooks with other users
* can install new packages using pip and apt

Cons:
* maximum notebook size is 20Mb (not sure if anyone will exceed this)
* can only use Python (no R or Scala etc programming environments)


## mybinder.org

(MyBinder)[https://mybinder.org/] computing environment that creates a Jupyter notebook from a Github repo

Pros:
* can create a computing environment based on a Github repo - so there is no need for each user to install packages using package manager separately 

Cons:
* can we upload/provide csv files for users (for example via Github)?
* how do we save completed Jupyter notebooks to Github?
* do we know the CPU limits of this service?

## custom JupyterHub/Binderhub deployment 

It's possible to setup a custom JupyterHub service that will allow users to run Python/R/etc code in the cloud.

Pros:
* can have more than one language kernel for Jupyter notebooks (ie. R, Scala etc)
* more control over CPU and memory resources, but constrained by size of cloud cluster


Cons:
* no GPU access
* more limited computing resources (due to cloud compute cost)
* needs more management from the organizing team


## Recommendation

TODO
