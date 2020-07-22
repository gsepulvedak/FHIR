'''
Author: Gonzalo Sepulveda
Student Id: 29505445
Created: 18/07/2020
Lang: Python 3.7.6
Approximated runtime: 5 min
'''

###### Question 3 ######

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
        
        # Get corresponding data type
        if obs_type == 'Low Density Lipoprotein Cholesterol':
            obs_data = re.search(data_pattern, item, re.DOTALL)
            
            if obs_data is not None:
                obs_data = obs_data[0]
                data_tuples.append((obs_date, obs_data))
            else:
                data_tuples.append((obs_date, 0))
                
        elif obs_type == 'Blood Pressure':
            obs_data = re.findall(data_pattern, item, re.DOTALL)
            
            if len(obs_data) != 0:
                data_dias = obs_data[0]
                data_sys = obs_data[1]
                data_tuples.append((obs_date, data_dias, data_sys))
            else:
                data_tuples.append((obs_date, 0, 0))
   
    # Get last observation data
    last_data = max(data_tuples, key = lambda t: t[0])
    return last_data

# Compute BH
def compute_bh(data_bp, data_ldlc):
    
    if (0 in data_bp or 0 in data_ldlc):
        return 0
    
    diastolic, systolic = float(data_bp[1]), float(data_bp[2])
    ldlc = float(data_ldlc[1])
    result = (((systolic - 2) * diastolic)**2)/ldlc
    return result

# Get patient BH
def patient_bh(pat_id, file_data):
    
    # Strip patient bundle
    pat_bundle = patient_bundle_by_id(pat_id, file_data)
    
    # Get LDLC observations
    pat_ldlc_obs = obs_by_type('Low Density Lipoprotein Cholesterol', file_data=pat_bundle)
    
    # Get last data if any
    if len(pat_ldlc_obs) == 0:
        return 0
    pat_ldlc_data = last_obs_data(pat_ldlc_obs, 'Low Density Lipoprotein Cholesterol')
    
    # Get BP observations
    pat_bp_obs = obs_by_type('Blood Pressure', pat_bundle)
    
    # Get last data if any
    if len(pat_bp_obs) == 0:
        return 0
    pat_bp_data = last_obs_data(pat_bp_obs, 'Blood Pressure')
    
    # Compute and return patient BH
    pat_bh = compute_bh(pat_bp_data, pat_ldlc_data)
    return pat_bh

# Get patient's BH by practitioner id
def doc_patients_bh(doc_id, files_list):
    
    # Get practitioner files
    doc_files = [file_name for file_name in files_list if doc_id in file_name]
    
    # BH placeholder
    tuples_list = []

    # Get BH for each patient
    for file in doc_files:
        with open('dataset/' + file) as f:
            json_data = f.read()
        pat_ids = re.findall('(?<=Patient\/).*?(?=\")', json_data, re.DOTALL)
        
        # Store patients BH
        for pat_id in pat_ids:
            pat_bh = patient_bh(pat_id=pat_id, file_data=json_data)
            tuples_list.append((pat_id, pat_bh))
    
    return tuples_list
        
#%%
### Generate output file (5 min approx) ###

# Read practitioner ids from queries
with open('queries/Q3_input.txt') as q3:
    doc_ids = q3.readlines()

# Read dataset file names
file_names = os.listdir('dataset/')

# Initialize output data string
output_data = ''

# Iterate over practitioner ids
for doc_id in doc_ids:
    
    doc_id = doc_id.replace('\n', '')
    
    # Get patients' BH list
    doc_pat_bh = doc_patients_bh(doc_id, file_names)
    
    # Sort
    sorted_tuples = sorted(doc_pat_bh, key=lambda x: (-x[1], x[0]), reverse=False)
    
    # Get top 3
    top_patients = sorted_tuples[0:3]
    
    # Store in string
    doc_pats_bh = 'Practitioner '+ doc_id + ':\n1: ' + top_patients[0][0] + '\n2: ' + top_patients[1][0] + '\n3: ' + top_patients[2][0] + '\n\n'
    output_data += doc_pats_bh

# Save output data to file
out_handler = open('output/Q3_output.txt', mode = 'w')
out_handler.writelines(output_data)

# Close handler
out_handler.close()
