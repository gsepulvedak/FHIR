'''
Author: Gonzalo Sepulveda
Student Id: 29505445
Created: 18/07/2020
Lang: Python 3.7.6
Approximated runtime: 3 min
'''

###### Question 2 ######

#%%
import pandas as pd
import numpy as np
import re, os

#%%
### Helper function ###

# Get entity substring
def entity_by_id(id, entity, file_data):
    pattern = entity + '/' + id + '.*?(?={\s+\"fullUrl)'
    data_string = re.search(pattern, file_data, re.DOTALL)[0]
    return data_string

#%%
### Create patient location index data frame (40 seconds approx) ###

# Placeholder
index = {}

# Impute placeholder
file_names = os.listdir('dataset/')
for file_name in file_names:
    file_handler = open('dataset/' + file_name)
    data = file_handler.read()
    pat_ids = re.findall('(?<=Patient/).*?(?=\")', data, re.DOTALL)
    file_list = np.resize([file_name], len(pat_ids))
    partial_dic = dict(zip(pat_ids, file_list))
    index.update(partial_dic)

# Close last opened file
file_handler.close()

# Remove not needed variables
del data, pat_ids, file_list, partial_dic, file_name, file_handler

#%%
### Create organizations data frame ###

# Placeholder dict for organization data
org_df = pd.DataFrame(columns=['org_id', 'org_name', 'org_post_code', 'pat_number'])

# Get organisations' id from json filenames
org_id_pattern = '(?<=organization).*?(?=.json)'
org_ids = set(re.findall(org_id_pattern, ' '.join(file_names))) # unique org ids

# Get sublist of files for each organization
for org_id in org_ids:
    org_files = [file_name for file_name in file_names if org_id in file_name]
    
    # Open file and get organization substring
    file_handler = open('dataset/' + org_files[0])
    file_data = file_handler.read()
    org_string = entity_by_id(id=org_id, entity='Organization', file_data=file_data)
    
    # Get organization name, postal code and state
    org_name = re.search('(?<=name\": \").*?(?=\",)', org_string, re.DOTALL)[0]
    org_post_code = re.search('(?<=postalCode\": \").*?(?=\",)', org_string, re.DOTALL)[0]
    
    # Count how many patients are there in the file
    pat_number = len(re.findall('Patient/.*?,', file_data))
    
    # Get data from subset of files
    for org_file in org_files[1:]:
        file_handler = open('dataset/' + org_file)
        file_data = file_handler.read()
        pat_number += len(re.findall('Patient/.*?,', file_data))
    
    # Update organization dataframe
    df_row = pd.Series([org_id, org_name, org_post_code, pat_number], 
                        index = ['org_id', 'org_name', 'org_post_code', 'pat_number'])
    org_df = org_df.append(df_row, ignore_index=True)
    
# Close last opened file
file_handler.close()

# Remove not needed variables
del org_files, file_data, org_string, org_name, org_post_code, pat_number, df_row, org_ids, org_file, org_id, file_names, file_handler

# Sort dataframe
org_df.sort_values(by = ['org_post_code', 'pat_number', 'org_name'], ascending=True, inplace=True)

#%%
### Generate output file (2.5 min approx) ###

# Read patient ids from queries
file_handler = open('queries/Q2_input.txt')
patient_ids = file_handler.readlines()

# Initialize output data string
output_data = ''

# Iterate over patient ids
for patient_id in patient_ids:
    
    patient_id = patient_id.replace('\n', '')

    # Filter by patient id and get file name
    patient_file = index[patient_id]
    
    # Search org id in file name
    patient_org_id = re.search(org_id_pattern, patient_file)[0]
    
    # Get post code of organization and search for replacement candidates
    org_post_code = org_df[org_df.org_id == patient_org_id].org_post_code.to_list()[0]
    
    # Filter candidates by post code
    org_candidates = org_df[org_df.org_post_code == org_post_code]
    
    # Get best org replacement
    org_rplc_id = org_candidates.iloc[0].org_id
    
    # Store patient id
    output_data += 'Patient ' + patient_id + ':\n'

    # Pick top 1 organization only if it is a different one 
    if org_rplc_id != patient_org_id:
        output_data += org_rplc_id + '\n\n'
    else:
        output_data += 'None\n\n'

# Close last opened file
file_handler.close()

# Save output data to file
out_handler = open('output/Q2_output.txt', mode = 'w')
out_handler.writelines(output_data)

# Close handler
out_handler.close()