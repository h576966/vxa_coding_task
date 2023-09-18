#!/usr/bin/env python
# coding: utf-8

# In[7]:


from xml.etree import ElementTree as et
from collections import defaultdict
import pandas as pd


# In[16]:


def load_xml(filepath):
    
    #Parsing the XML file
    tree = et.parse(filepath)
    root = tree.getroot()
    
    data = []
    
    animals = root.find('animals')
    
    for animal in animals.findall('a'):
        animal_data = animal.attrib
        
        # DefaultDict provides a default value for the key that does not exists, this to avoid raising KeyErrors.
        v_data = defaultdict(list)
        
        for v in animal.findall('v'):
            v_data[f"class{v.get('class')}"].append(v.text)
        
        # Iterate over both key and value in dict, this is to avoid lists in the classes columns
        for x, v in v_data.items():
                   animal_data[x] = ', '.join(v)
                   
        data.append(animal_data)
                   
    df = pd.DataFrame(data)
    df.sort_values(by=['id'], inplace=True, ignore_index=True)
    return df
        
   

