
#%%
import pandas as pd
import numpy as np
import re, os
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)
pd.set_option('display.width', 1000)

#%%
# Entity substring function
# def entity_by_id(id, entity, file_data):
#     pattern = entity + '/' + id + '.*?(?={\s+\"fullUrl)'
#     data_string = re.search(pattern, file_data, re.DOTALL)[0]
#     return data_string

#%%
### Create patient location index data frame ###

# Placeholder
index = pd.DataFrame()
# index = {}

# Impute placeholder
file_names = os.listdir('dataset/')
for file_name in file_names:
    file_handler = open('dataset/' + file_name)
    data = file_handler.read()
    pat_ids = re.findall('(?<=Patient/).*?(?=\")', data, re.DOTALL)
    file_list = np.resize([file_name], len(pat_ids))
    data_tuples = list(zip(pat_ids, file_list))
    # partial_dic = dict(zip(pat_ids, file_list))
    sub_df = pd.DataFrame(data_tuples, columns=['pat_id', 'file_name'])
    index = index.append(sub_df)
    # index.update(partial_dic)

# Close last opened file
file_handler.close()

# Remove not needed variables
# del data, pat_ids, file_list, partial_dic, file_name, file_handler