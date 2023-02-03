# it's the third file to be executed don't forget to create the folders or duplicate the structure of the .zip

import pandas as pd
import glob, os

os.chdir("tables-rel/")


data_containers = []
for file in glob.glob("*.csv"):
    if file != 'tables.csv':
        data_container = pd.read_csv(file)
        data_container['SAP_Table'] = file.split('.')[0]
        data_containers.append(data_container)        

        
relations_table = pd.concat(data_containers)
relations_table.to_excel('0tables-relations.xlsx',index=False)
relations_table.to_csv('0tables-relations.csv',index=False) 
