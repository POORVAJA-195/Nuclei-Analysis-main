

import yaml
import re
import json
import requests


output_list = []
def extract_cve_id_from_url(url):
    parts = url.split('/')
    filename = parts[-1]
    match = re.search(r"CVE-\d{4}-\d{0,7}", filename)
    if match:
        return match.group(0)
    else:
        return None

nuclie_template_cve_ids = []  

with open("output_details.txt", "r") as file:
    data = yaml.safe_load(file)

for vendor, details in data["vendors"].items():
    for product_detail in details["products"]:
        for i,url in enumerate(product_detail["nuclei_templates"]):
            cve_id = extract_cve_id_from_url(url)
            if cve_id:
                shodan_query = product_detail["shodan_queries"][i]
                if shodan_query != 'null':
                        output = 'yes'
                else:
                        output = 'no'
                output_list.append((cve_id,output))
                nuclie_template_cve_ids.append(cve_id)  

nuclie_template_cve_ids.sort()
# print(f"total nuclie template cve id:" , len(nuclie_template_cve_ids))
output_list.sort()
# print(output_list)

with open("nuclie_template_cve.txt","w") as file:
    for cve_id in nuclie_template_cve_ids:
       file.write(cve_id + "\n")



# URL of the JSON file
url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
response = requests.get(url)
data = response.json()
cisa_cve_ids = [vuln["cveID"] for vuln in data["vulnerabilities"]]
cisa_cve_ids.sort()
print(f"total cisa cve id:" , len(cisa_cve_ids))
with open("cisa_cves.txt","w") as file:
    for cisa_cve_id in cisa_cve_ids:
        file.write(cisa_cve_id + "\n")


# PERCENTAGE of CISA KEVs with Nuclei templates, that have shodan queries.
set2 = set(output_list)
count_of_cisa_cve_in_nuclie_with_shordan_queries = sum(1 for cve_id in cisa_cve_ids if (cve_id, 'yes') in set2)
percentage = (count_of_cisa_cve_in_nuclie_with_shordan_queries/cisa_cve_ids) * 100
print(percentage)

# COUNT OF CISA KEVs WITH NUCLEI TEMPLATE 
# set1 = set(cisa_cve_ids)
# set2 = set(nuclie_template_cve_ids)
# common_cves = set1.intersection(set2)
# common_cves_list = list(common_cves)
# common_cves_list.sort()
# print(f"total cisa cves in nuclie template:" , len(common_cves_list))
# with open("cisa_cves_in_nuclie.txt","w") as file:
#     for cve in common_cves_list:
#         file.write(cve + "\n")
# # cve_count = len(cve_ids)




# import yaml
# import re
# import json
# import requests

# def extract_cve_id_from_url(url):
#     parts = url.split('/')
#     filename = parts[-1]
#     match = re.search(r"CVE-\d{4}-\d{0,7}", filename)
#     if match:
#         return match.group(0)
#     else:
#         return None

# def process_nuclei_templates(data):
#     output_list = []
#     nuclie_template_cve_ids = []  

#     for vendor, details in data["vendors"].items():
#         for product_detail in details["products"]:
#             for i, url in enumerate(product_detail["nuclei_templates"]):
#                 cve_id = extract_cve_id_from_url(url)
#                 if cve_id:
#                     shodan_queries = product_detail["shodan_queries"]
#                     if i < len(shodan_queries):
#                         shodan_query = shodan_queries[i]
#                         if shodan_query != 'null':
#                             output = 'yes'
#                         else:
#                             output = 'no'
#                         output_list.append((cve_id, output))
#                     else:
#                         print(f"Warning: No corresponding shodan_query for URL {url}")
#                     nuclie_template_cve_ids.append(cve_id)  

#     nuclie_template_cve_ids.sort()
#     with open("nuclie_template_cve.txt", "w") as file:
#         for cve_id in nuclie_template_cve_ids:
#             file.write(cve_id + "\n")

#     return output_list, nuclie_template_cve_ids


# def process_cisa_cves():
#     url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
#     response = requests.get(url)
#     data = response.json()
#     cisa_cve_ids = [vuln["cveID"] for vuln in data["vulnerabilities"]]
#     cisa_cve_ids.sort()

#     with open("cisa_cves_1.txt","w") as file:
#         for cisa_cve_id in cisa_cve_ids:
#             file.write(cisa_cve_id + "\n")

#     return cisa_cve_ids

# def main():
#     with open("output_details_1(unique_shodan_queries).txt", "r") as file:
#         data = yaml.safe_load(file)

#     output_list, nuclie_template_cve_ids = process_nuclei_templates(data)
#     cisa_cve_ids = process_cisa_cves()

#     set2 = set(output_list)
#     count_of_cisa_cve_in_nuclie_with_shordan_queries = sum(1 for cve_id in cisa_cve_ids if (cve_id, 'yes') in set2)
#     percentage = (count_of_cisa_cve_in_nuclie_with_shordan_queries/len(cisa_cve_ids)) * 100
#     print("Percentage:", percentage)

#     # Save the count and percentage to a file
#     with open("cisa_cves_statistics.txt", "w") as stats_file:
#         stats_file.write(f"Total CISA CVEs: {len(cisa_cve_ids)}\n")
#         stats_file.write(f"Count of CISA CVEs in nuclei with Shodan queries: {count_of_cisa_cve_in_nuclie_with_shordan_queries}\n")
#         stats_file.write(f"Percentage of CISA CVEs in nuclei with Shodan queries: {percentage}%\n")

# if __name__ == "__main__":
#     main()
