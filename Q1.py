'''
Author: Gonzalo Sepulveda
Student Id: 29505445
Created: 17/07/2020
Lang: Python 3.7.6
'''

###### Question 1 ######

#%%
import re, os
import numpy as np

#%%

# Placeholder for frequencies
gender_count = {"male": 0, "female": 0, "other": 0}

# Use regex to get patient's gender across json files
pattern = 'Patient/.*?gender\": \"(.*?)\"'

# Iterate over files searching and storing patients' gender
for file in os.listdir('dataset/'):
    file_name = file
    bundle = open(f'dataset/{file_name}').read()
    
    # Match all occurrences
    genders = re.findall(pattern, bundle, re.DOTALL)

    # Use numpy to get classes frequency
    genders_array = np.asarray(genders)
    gender_freq = np.unique(genders_array, return_counts=True)
    
    # Check and store if any other gender category appears (only for generalisation. No such thing was found in the dataset)
    if np.any(np.isin(gender_freq[0], ['male', 'female'], invert=True)):
        
        # Get indexes of other categories
        gender_list = gender_freq[0].tolist()
        other_idx = [gender_list.index(other) for other in gender_list if other not in ['male', 'female']]
                
        # Sum values for all other possible categories
        other_total = 0
        for idx in other_idx:
            other_total += gender_freq[1][idx]
            
        # Update dictionary
        gender_count['Other'] = other_total

    # Store male/female values
    gender_count[gender_freq[0][0]] += gender_freq[1][0]
    gender_count[gender_freq[0][1]] += gender_freq[1][1]

# Pending: generate output file from gender_count dictionary

