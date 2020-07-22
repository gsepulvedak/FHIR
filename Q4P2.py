'''
Author: Gonzalo Sepulveda
Student Id: 29505445
Created: 18/07/2020
Lang: Python 3.7.6
Approximated runtime: 5 min
'''

###### Question 4 P2 ######

#%%
import re, os
from datetime import datetime

#%%
### Helper functions ###

# Get patient bundle
def patient_bundle_by_id(id, file_data):
    pattern = 'Patient/' + id + '.*?Bundle'
    data_string = re.search(pattern, file_data, re.DOTALL)[0]
    return data_string

# Get observations of interest
def obs_by_type(obs_type, file_data):
    '''
    input:
    obs_type : string of interest ("Low Density Lipoprotein Cholesterol" and "Blood Pressure")
    output:
    obs_list : list of all observations of obs_type type.
    '''

    pattern = obs_type + '.*?(?:fullUrl|Bundle)'
    obs_list = re.findall(pattern, file_data, re.DOTALL)
    return obs_list

# Get last observation id, date and data
def last_obs_data(obs_list, obs_type):
    date_pattern = '(?<=effectiveDateTime\". \").*?(?=\")'
    data_pattern = '(?<=value\": ).*?(?=\s.*?})'
    data_tuples = [] #data placeholder
    
    for item in obs_list:
        obs_date_str = re.search(date_pattern, item, re.DOTALL)[0]
        obs_date = datetime.strptime(obs_date_str, '%Y-%m-%dT%H:%M:%S%z')
        
        # Get corresponding data typ
        obs_data = re.search(data_pattern, item, re.DOTALL)
            
        if obs_data is not None:
            obs_data = obs_data[0]
            data_tuples.append((obs_date, obs_data))
        else:
            data_tuples.append((obs_date, 'NA'))
   
    # Get last observation data
    last_data = max(data_tuples, key = lambda t: t[0])
    return last_data

#%%
### Wrapping functions ###

# Get patient leukocytes value
def patient_leuko(pat_id, file_data):
    
    # Strip patient bundle
    pat_bundle = patient_bundle_by_id(pat_id, file_data)
    
    # Get Leukocytes observations
    pat_leuko_obs = obs_by_type('Leukocytes', file_data=pat_bundle)
    
    # Get last data if any
    if len(pat_leuko_obs) == 0:
        return 'NA'
    pat_leuko_data = last_obs_data(pat_leuko_obs, 'Leukocytes')
    
    # Return leukocytes count
    return float(pat_leuko_data[1])


# Get patient's BH by practitioner id
def doc_patients_leuko(doc_id, files_list):
    
    # Get practitioner files
    doc_files = [file_name for file_name in files_list if doc_id in file_name]
    
    # BH placeholder
    tuples_list = []

    # Get BH for each patient
    for file in doc_files:
        with open('dataset/' + file) as f:
            json_data = f.read()
        pat_ids = re.findall('(?<=Patient\/).*?(?=\")', json_data, re.DOTALL)
        
        # Store patients Leukocytes count
        for pat_id in pat_ids:
            pat_leuko = patient_leuko(pat_id=pat_id, file_data=json_data)
            tuples_list.append((pat_id, pat_leuko))
    
    # Remove patients with no Leukocytes readings
    tuples_clean = [tup for tup in tuples_list if tup[1] != 'NA']
    
    return tuples_clean

#%%
### Generate output file (5 min approx) ###

# Read practitioner ids from queries
with open('queries/Q4P2_input.txt') as q3:
    doc_ids = q3.readlines()

# Read dataset file names
file_names = os.listdir('dataset/')

# Initialize output data string
output_data = ''

# Iterate over practitioner ids
for doc_id in doc_ids:
    
    doc_id = doc_id.replace('\n', '')
    
    # Get patients' Leukocytes list
    doc_pat_leuko = doc_patients_leuko(doc_id, file_names)
    
    # Sort
    sorted_tuples = sorted(doc_pat_leuko, key = lambda x: x[1])
    
    # Store patient pairs in string
    pat_pairs = ''
    for i in range(0, len(sorted_tuples)-1, 2):
        first = sorted_tuples[i][0]
        second = sorted_tuples[i+1][0]
        pat_pairs += first + ' ' + second + '\n'
    
    # Generate output string
    output_data += '\nPractitioner ' + doc_id + ':\n' + pat_pairs

# Save output data to file
output_data = output_data[1:] # remove firsr blank line

# Write file
out_handler = open('output/Q4_P2_output.txt', mode = 'w')
out_handler.writelines(output_data)

# Close handler
out_handler.close()