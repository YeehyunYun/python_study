import json
import sqlite3

import requests

from requests.auth import HTTPBasicAuth
from jira import JIRA

conn = sqlite3.connect('task1.db')

USERNAME = "yhyun@autocrypt.io"
API_TOKEN = "ATATT3xFfGF03ZA5qjVCpYtxRxtBMC74n-igGDDiyaeZrpqKPPl8fuZ-judzpkDuJryJdvUcKTjzcmfbI3vuF_Usvf1Qz9rZ4sdyZpDJGsb-FWwGk5gd0bAhTH1gAKOGtDhpK-Z7FciqFeIAPxTqOEGK0NPdEvLGM2itJXqBEsunXlTPosRNVTk=0733801A"
auth = HTTPBasicAuth(USERNAME, API_TOKEN)


import ast

with open('output.txt', 'r') as f:
    contents = f.read()


my_str = contents
SRS_content = ast.literal_eval(my_str)


def remove_duplicates(lst):
    seen = []
    result = []
    for item in lst:
        if item not in seen:
            seen.append(item)
            result.append(item)
    return result

new = remove_duplicates(SRS_content)
print(new)

def get_version(auth_key, page_id):
    id = page_id
    url = f"https://auto-jira.atlassian.net/wiki/api/v2/pages/{id}"

    auth = HTTPBasicAuth(USERNAME, API_TOKEN)

    headers = {"Accept": "application/json"}

    response = requests.request("GET", url, headers=headers, auth=auth)
    return response.json()["version"]["number"]


def get_space_id(auth_key):
    spaceKey = "~642a5ea9551f476a04684fbd"
    url = f"https://auto-jira.atlassian.net/wiki/rest/api/space/{spaceKey}"

    headers = {
        "Accept": "application/json",
    }

    response = requests.request("GET", url, headers=headers, auth=auth)
    return json.loads(response.text)["id"]



def update_page(auth_key, id, title, content): 
    page_id = id
    page_url = f"https://auto-jira.atlassian.net/wiki/api/v2/pages/{page_id}"

    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    page_dic = {"type": "doc", "content": content }

    version = get_version(auth, page_id)

    page_payload = json.dumps(
        {
            "id": page_id,
            "status": "current",
            "title": title,
            "spaceId": get_space_id(auth),
            "body": {"representation": "atlas_doc_format", "value": json.dumps(page_dic) },
            "version": {"number": version + 1, "message": "new"},
        }
    )
    response = requests.request("PUT", page_url, data=page_payload, headers=headers, auth=auth)
    return response.status_code


update_page(auth, "1099170250", "RS", new)