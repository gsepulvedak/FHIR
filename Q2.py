'''
Author: Gonzalo Sepulveda
Student Id: 29505445
Created: 18/07/2020
Lang: Python 3.7.6
'''

###### Question 2 ######


# Largest file (625501 lines):
# practitioner26c419ce-a137-417b-90ef-8da89cacc8e3_organization48d0bbb2-ffb1-47db-aadb-f1624d27252b.json

# Patient test id: 8fb8f7d8-5e15-4a29-9d9a-67f0df262286

#%%
import pandas as pd
import re, os


#%%
# Entity substring function
def entity_by_id(id, entity, file_data):
    pattern = entity + '/' + id + '.*?(?={\s+\"fullUrl)'
    data_string = re.search(pattern, file_data, re.DOTALL)[0]
    return data_string

#%%

# Placeholder dict for organization data
org_dict = {}

# Get organisations' id from json filenames
file_names = os.listdir('dataset/')
org_id_pattern = '(?<=organization).*?(?=.json)'
org_ids = set(re.findall(org_id_pattern, ' '.join(file_names))) # unique org ids

# Get sublist of files for each organization
for org_id in ['edfbd832-fb71-427d-97c7-e9b100acff44']:
    org_files = [file_name for file_name in file_names if org_id in file_name]
    
    # Open file and get organization substring
    file_data = open('dataset/' + org_files[0]).read()
    org_string = entity_by_id(id=org_id, entity='Organization', file_data=file_data)
    
    # Get organization name, postal code and state
    org_name = re.search('(?<=name\": \").*?(?=\",)', org_string, re.DOTALL)[0]
    org_post_code = re.search('(?<=postalCode\": \").*?(?=\",)', org_string, re.DOTALL)[0]
    org_state = re.search('(?<=state\": \").*?(?=\"\\n)', org_string, re.DOTALL)[0]
    
    # Count how many patients are there in the file
    pat_number = len(re.findall('Patient/.*?,', file_data))
    
    # Get data from subset of files
    for org_file in org_files[1:]:
        file_data = open('dataset/' + org_file).read()
        pat_number += len(re.findall('Patient/.*?,', file_data))
    
    # Update organization dictionary
    org_dict[org_id] = {'post_code':org_post_code, 'name':org_name, 'patients':pat_number, 'state':org_state}
    

# Transform dictionary to pandas data frame 


# Sort dataframe

#%%
re.search(org_id_pattern, 'practitioner26c419ce-a137-417b-90ef-8da89cacc8e3_organization48d0bbb2-ffb1-47db-aadb-f1624d27252b.json')[0]



#%%
# Method to get a whole patient bundle based on patient id
# Regex pattern 
# id = '8fb8f7d8-5e15-4a29-9d9a-67f0df262286'
# entity = 'Patient'
# pattern = entity + '/' + id + '.*?Bundle.*?}'

# # Get whole patient bundle
# patient_bundle = re.search(pattern, bundle, re.DOTALL)