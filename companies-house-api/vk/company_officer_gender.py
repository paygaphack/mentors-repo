import json

data = []
with open('company-officers.json') as f:
    for line in f:
        data.append(json.loads(line))
        
#%% REFORMATTING DATA FOR SIMPLER MANIPULATION

all_company_numbers_lst = []
all_officer_names_lst = []
all_first_names_lst = []
all_active_inactive_flags = []

for row in range(len(data)):
    #capture the company number of each
    company_no = list(data[row].keys())[0]
    print(company_no)
    
    company_officers = list(list(data[row].values())[0].values())
    company_officers = company_officers[1]
    
    names_lst = []
    first_names_lst = []
    resignation_date_lst = []
    
    for o in range(len(company_officers)):
        officer_name = company_officers[o]['name']
        names_lst.append(officer_name)
        #isolate the first (first name) for inferring gender
        try:
            first_name = officer_name.split(',')[1].split()[0]
            first_names_lst.append(first_name)
        except IndexError:#suggesting no comma was found ~ probably not a person't name then...
            first_names_lst.append(None)
        
        
        try:
            officer_resign_date = company_officers[o]['resigned_on']
            resignation_date_lst.append(officer_resign_date)
        except KeyError:
            resignation_date_lst.append(None)
            
    #creating flags for active/inactive officers
    active_inactive_lst = []
    for date in range(len(resignation_date_lst)):
        if resignation_date_lst[date] == None:
            value = 1#flag as active
        else:
            value = 0#flag as inactive
        active_inactive_lst.append(value)
    
    num_officers = len(active_inactive_lst)
    
    company_nos = [company_no]* num_officers
    
    all_company_numbers_lst.extend(company_nos)
    all_officer_names_lst.extend(names_lst)
    all_first_names_lst.extend(first_names_lst)
    all_active_inactive_flags.extend(active_inactive_lst)

# making a pandas dataframe
import pandas as pd

df = pd.DataFrame( {'company_no' : all_company_numbers_lst,
                    'full_name' : all_officer_names_lst,
                    'first_name':all_first_names_lst,
                    'active_flag':all_active_inactive_flags },
            columns=['company_no','full_name', 'first_name', 'active_flag'])
    
        
#%% INFERRING GENDER OF THE OFFICER

#dictionary somebody created from US census...
from names import names

gender_lst = []

for row in range(len(df)):
    try:
        key = str.lower(df['first_name'][row])
        if key in names:
            gender_lst.append(names[key])
    except TypeError:
        gender_lst.append('Unknown')

df['gender'] = gender_lst  
     
df.to_csv('all_company_officers_incl_gender.csv', index = False)
