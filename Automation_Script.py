import requests
import yaml
import os
import json
from bs4 import BeautifulSoup

def fetch_metadata_from_url(url):
    try:
        
        response = requests.get(url)
        file_content = response.text        
        
        if 'metadata' in file_content.lower():
            yaml_data = yaml.safe_load(file_content)
            info = yaml_data.get("info", {})
            metadata = info.get('metadata', {})
            vendor = metadata.get('vendor')
            product = metadata.get('product')
            shodan_queries = metadata.get("shodan-query", [])
            fofa_queries = metadata.get("fofa-query", [])
            zoomeye_queries = metadata.get("zoomeye-query", [])
            hunter_queries = metadata.get("hunter-query", [])

            # Ensuring queries are always returned as lists
            shodan_queries = shodan_queries if isinstance(shodan_queries, list) else [shodan_queries]
            fofa_queries = fofa_queries if isinstance(fofa_queries, list) else [fofa_queries]
            zoomeye_queries = zoomeye_queries if isinstance(zoomeye_queries, list) else [zoomeye_queries]
            hunter_queries = hunter_queries if isinstance(hunter_queries, list) else [hunter_queries]
            
            return vendor, product, shodan_queries, fofa_queries, zoomeye_queries, hunter_queries
        else:
            print(f"No 'metadata' found in {url}")
            return None, None, [], [], [], []
    except Exception as e:
        print(f"An error occurred while fetching metadata from {url}: {str(e)}")
        return None, None, [], [], [], []

import json

def append_or_create_vendor_details(vendor, product, nuclei_template, shodan_queries, fofa_queries, zoomeye_queries, hunter_queries, filename):
    try:
        with open(filename, 'r') as file:
            existing_details = json.load(file)
    except FileNotFoundError:
        existing_details = {}

    vendors = existing_details.setdefault("vendors", {})
    
    if vendor in vendors:
        products = vendors[vendor]["products"]
        product_exists = False
        for prod in products:
            if prod["product"] == product:
                prod_shodan_queries = prod["shodan_queries"]
                for query in shodan_queries:                     # append shodan_queries that are not in the list
                    if query not in prod_shodan_queries:
                        prod_shodan_queries.append(query)
                prod["nuclei_templates"].append(nuclei_template)
                prod["fofa_queries"].extend(fofa_queries)
                prod["zoomeye_queries"].extend(zoomeye_queries)
                prod["hunter_queries"].extend(hunter_queries)
                product_exists = True
                break
        if not product_exists:
            products.append({
                "product": product,
                "nuclei_templates": [nuclei_template],
                "shodan_queries": shodan_queries,
                "fofa_queries": fofa_queries,
                "zoomeye_queries": zoomeye_queries,
                "hunter_queries": hunter_queries
            })
    else:
        vendors[vendor] = {
            "products": [{
                "product": product,
                "nuclei_templates": [nuclei_template],
                "shodan_queries": shodan_queries,
                "fofa_queries": fofa_queries,
                "zoomeye_queries": zoomeye_queries,
                "hunter_queries": hunter_queries
            }]
        }

    with open(filename, 'w') as file:
        json.dump(existing_details, file, indent=4)


def fetch_and_parse_yaml_files(repo_url, folder_path, filename):
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
                               vendor, product, shodan_queries, fofa_queries, zoomeye_queries, hunter_queries = fetch_metadata_from_url(final_url)
                               append_or_create_vendor_details(vendor, product, final_url, shodan_queries, fofa_queries, zoomeye_queries, hunter_queries, filename)
                               print("URL:", final_url)
                               print("Vendor:", vendor)
                               print("Product:", product)
                               print("-" * 50)
                               #print(final_url)
    #print(count_of_files)                                                                 #To know the number of files

#list of products that have not null shodan queries 
def save_products_with_non_null_shodan_queries(filename_in, filename_out):
    try:
        with open(filename_in, 'r') as file:
            existing_details = json.load(file)
    except FileNotFoundError:
        print("Input file not found.")
        return

    vendors = existing_details.get("vendors", {})
    products_with_non_null_shodan = []

    for vendor, vendor_details in vendors.items():
        products = vendor_details.get("products", [])
        for product in products:
            shodan_queries = product.get("shodan_queries")
            if shodan_queries:
                product_details = f"Product: {product['product']}\nShodan Queries: {', '.join(shodan_queries)}\n"
                products_with_non_null_shodan.append(product_details)

    try:
        with open(filename_out, 'w') as file_out:
            file_out.writelines(products_with_non_null_shodan)
        print("Products with non-null Shodan queries saved to", filename_out)
    except IOError:
        print("Error saving to file.")


repo_url = 'projectdiscovery/nuclei-templates/blob/'
folder_path = 'http/cves'
filename = "output_details_1(unique_shodan_queries).txt"
fetch_and_parse_yaml_files(repo_url, folder_path, filename)
save_products_with_non_null_shodan_queries("output_details.txt", "not_null_shodan_queries.txt")
