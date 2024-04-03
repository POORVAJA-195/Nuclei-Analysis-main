import requests
import yaml
import os
import json
from bs4 import BeautifulSoup
def fetch_and_parse_yaml_files(repo_url, folder_path):
    count_of_files=0
    base_url = 'https://github.com/'
    url = f'{base_url}{repo_url}/main/{folder_path}'
    # Fetching list of files in the folder
    response = requests.get(url)
    if response.status_code == 200:
        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find all folder elements
        folder_elements = soup.find_all('script', {'data-target':'react-app.embeddedData', 'type':'application/json'})
        # Extract folder data
        for folder_element in folder_elements:
            folder_name = folder_element.get_text()
            files = json.loads(folder_name)
            keys=["payload","tree","items"]          #from the response traversed upto the folder
            for key in keys:
                files = files[key]
            for each in files:
                deep_url =  url+"/"+each['name']
                #print(deep_url)                       #traversed upto each folder Eg:starts from http/cves/2000/  and upto http/cves/2024/
                response1 = requests.get(deep_url)
                if response1.status_code == 200:
                    # Parse HTML content
                    soup = BeautifulSoup(response1.content, 'html.parser')
                    # Find all folder elements
                    folder_elements1 = soup.find_all('script', {'data-target':'react-app.embeddedData', 'type':'application/json'})
                    # Extract folder data
                    for folder_element1 in folder_elements1:
                         folder_name1 = folder_element1.get_text()
                         files1 = json.loads(folder_name1)
                         keys1=["payload","tree","items"]          #from the response traversed upto the files
                         for key in keys1:
                             files1 = files1[key]
                         for each1 in files1:
                               count_of_files=count_of_files+1
                               final_url = deep_url+"/"+each1['name']+"?raw=true"          #convert website url to raw ffile url
                               print(final_url)
    #print(count_of_files)                                                                 #To know the number of files


repo_url = 'projectdiscovery/nuclei-templates/blob/'
folder_path = 'http/cves'
fetch_and_parse_yaml_files(repo_url, folder_path)
