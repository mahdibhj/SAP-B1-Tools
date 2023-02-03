#You need to download chromedriver that has the same version as your chrome browser https://chromedriver.chromium.org/downloads
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd


website = 'https://blogs.sap.com/2016/01/14/sap-business-one-tables/'

web_driver=webdriver.Chrome()
web_driver.get(website)
sleep(5)
tables_bloc = web_driver.find_element(By.CLASS_NAME,"ds-blog-post__body.ds-editor-content")

strings_elements = tables_bloc.find_elements(By.TAG_NAME,'p')
print(len(strings_elements))

header_element = strings_elements[0].text.split('    ')
print(header_element)
print('other values')

strings_list = []
for string_element in strings_elements[2:]:
    #print(string_element)
    if len(string_element.text.replace(' ','').replace('   ',''))>0:
        strings_list.append( string_element.text.split('    ') )
        #print(string_element.text.split('   '))

print(len(strings_list))

print(strings_list)

tables_data = pd.DataFrame(strings_list, columns=header_element )

print(tables_data)

tables_data.to_excel('tables.xlsx',index=False)
tables_data.to_csv('tables.csv',index=False)
