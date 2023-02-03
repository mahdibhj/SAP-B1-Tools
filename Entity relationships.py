#it's the second file to be executed, don't forget to create the necessary folders or use the same folders structure of the .zip
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd


def scrape_data_from_tbody():
    data_list_of_lists = []
    tbody_element = web_driver.find_element(By.CLASS_NAME,"blistit.dataTable.no-footer").find_element(By.TAG_NAME,'tbody')
    tbody_rows = tbody_element.find_elements(By.TAG_NAME,'tr')
    for row in tbody_rows:
        try:
            Field = row.find_elements(By.TAG_NAME,'td')[0].find_element(By.TAG_NAME,'em').find_element(By.TAG_NAME,'b').find_element(By.TAG_NAME,'u').text
        except:
            Field = row.find_elements(By.TAG_NAME,'td')[0].find_element(By.TAG_NAME,'em').find_element(By.TAG_NAME,'b').text
        Description = row.find_elements(By.TAG_NAME,'td')[1].text
        Type = row.find_elements(By.TAG_NAME,'td')[2].find_element(By.TAG_NAME,'em').text
        Constraints = row.find_elements(By.TAG_NAME,'td')[3].find_element(By.TAG_NAME,'div').text
        Size = row.find_elements(By.TAG_NAME,'td')[4].text
        Related = row.find_elements(By.TAG_NAME,'td')[5].find_element(By.TAG_NAME,'a').text
        Default = row.find_elements(By.TAG_NAME,'td')[6].text
        Primary_key = row.find_elements(By.TAG_NAME,'td')[7].text
        Unique = row.find_elements(By.TAG_NAME,'td')[8].find_element(By.TAG_NAME,'em').text
        data_list_of_lists.append([Field,Description,Type,Constraints,Size,Related,Default,Primary_key,Unique])
    return data_list_of_lists

def add_table_to_scraped_list(table_name):
    scraped_tables_data=pd.read_csv('tables-rel/tables.csv')
    scraped_tables_list=scraped_tables_data['Name'].tolist()
    print(scraped_tables_list)
    scraped_tables_list.append(table_name)
    print(scraped_tables_list)
    scraped_tables_df = pd.DataFrame(scraped_tables_list, columns=['Name'] )
    print(scraped_tables_df)
    scraped_tables_df.to_csv('tables-rel/tables.csv',index=False)
    pass

tables_data = pd.read_csv('tables-static.csv')
#print(tables_data)
tables_names_list = tables_data['Name'].tolist()
#print(len(tables_names_list))
#print(tables_names_list)
#tables_names_list=['OCRD']
website_base = 'https://biuan.com/'

tbody_headers = ['Field','Description','Type','Constraints','Size','Related','Default','Primary_key','Unique']



web_driver=webdriver.Chrome()

for table_name in tables_names_list:
    table_data_lists = []
    scraped_tables_data=pd.read_csv('tables-rel/tables.csv')
    scraped_tables_list=scraped_tables_data['Name'].tolist()
    print(scraped_tables_list)

    if table_name not in scraped_tables_list:

        website = website_base + table_name
        web_driver.get(website)
        paginate_element = web_driver.find_element(By.CLASS_NAME,"dataTables_paginate.paging_simple_numbers")
        sleep(5)
        try:
            max_paginate = int(paginate_element.find_element(By.TAG_NAME,'span').find_elements(By.TAG_NAME,'a')[-1].text)
            print(max_paginate)
            print(type(max_paginate))
            partial_data = scrape_data_from_tbody()
            print(len(partial_data))
            print(pd.DataFrame(partial_data, columns=tbody_headers ))

        except:
            max_paginate = 0
            partial_data = []



        for data in partial_data:
            table_data_lists.append(data)

        if max_paginate > 1:
            loop_variable = True
            while loop_variable:
                try:
                    next_element = paginate_element.find_element(By.CLASS_NAME,"paginate_button.next")
                    #print(next_element.text)
                    next_element.click()
                    print('clicked next')
                    sleep(3)
                    web_driver.execute_script("window.scrollTo(0, 0);")
                    partial_data = scrape_data_from_tbody()
                    print(len(partial_data))
                    print(pd.DataFrame(partial_data, columns=tbody_headers ))
                    for data in partial_data:
                        table_data_lists.append(data)
                except:
                    web_driver.execute_script("window.scrollTo(0, 540);")
                    print('scrolled')
                    sleep(3)
                actual_selected = int(paginate_element.find_element(By.CLASS_NAME,"paginate_button.current").text)
                print(str(actual_selected) + ' is selected now')
                if actual_selected == max_paginate:
                    loop_variable = False


        else:
            pass

        table_full_data = pd.DataFrame(table_data_lists, columns=tbody_headers )
        table_full_data.to_csv('tables-rel/'+table_name+'.csv',index=False)
        add_table_to_scraped_list(table_name)
        print(table_full_data)

    else:
        print(table_name + ' already scraped')
