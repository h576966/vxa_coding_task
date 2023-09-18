#!/usr/bin/env python
# coding: utf-8

# In[3]:


from collections import defaultdict
import re
import pandas as pd


# In[30]:


def load_dat(filepath):
    animals_dat = pd.read_csv(filepath, header=None)
    
    regex = r"([A-C])"
    class_data = []
    
    datToDf = pd.DataFrame(columns=['id', 'morph', 'miff', 'xcam'])
    
    datToDf['id'] = animals_dat[0].str.slice(0,5)
    datToDf['morph'] = animals_dat[0].str.slice(5,8)
    datToDf['miff'] = animals_dat[0].str.slice(8,12)
    datToDf['xcam'] = animals_dat[0].str.slice(12,16)

    datToDf['valuesStr'] = animals_dat[0].str.slice(19).str.replace(" ", "")

    datToDf = datToDf.dropna().copy()

    for i in datToDf.index:
        
        #DefaultDict provides a default value for the key that does not exists, this to avoid raising KeyErrors.
        class_list = defaultdict(list)
        value_str = datToDf['valuesStr'][i]
        
        #re.split uses regex to find occurences of A,B,C in the classes String and splits the string into a list 
        split_list = re.split(regex, value_str)
        list_length = len(split_list)-1
    
        # iterate over every other item, where x corresponds to the value
        # and x+1 to the letter to which we add class in the column name
        for x in range(0, list_length, 2):
            class_list[f"class{split_list[x+1]}"].append(split_list[x])
        
        #iterate over both key and value in dict, this is to avoid lists in the classes columns
        for y, z in class_list.items():
                   class_list[y] = ', '.join(z)

            
        class_data.append(class_list)
    
    datToDf.drop(['valuesStr'], axis=1, inplace=True)
    class_df = pd.DataFrame(class_data)
    df=pd.concat([datToDf, class_df], axis=1, ignore_index=False, join='inner')
    df.sort_values(by=['id'], inplace=True, ignore_index=True)
    
    return df

