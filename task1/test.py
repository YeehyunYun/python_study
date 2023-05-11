import json
import sqlite3

import requests

from requests.auth import HTTPBasicAuth
from jira import JIRA

conn = sqlite3.connect('task1.db')

USERNAME = "yhyun@autocrypt.io"
API_TOKEN = "ATATT3xFfGF03ZA5qjVCpYtxRxtBMC74n-igGDDiyaeZrpqKPPl8fuZ-judzpkDuJryJdvUcKTjzcmfbI3vuF_Usvf1Qz9rZ4sdyZpDJGsb-FWwGk5gd0bAhTH1gAKOGtDhpK-Z7FciqFeIAPxTqOEGK0NPdEvLGM2itJXqBEsunXlTPosRNVTk=0733801A"
auth = HTTPBasicAuth(USERNAME, API_TOKEN)

def get_all_issues(jira_client, epic_key, fields):
    issues = []
    i = 0
    chunk_size = 50
    while True:
        chunk = jira_client.search_issues(f'parent = {epic_key}', startAt=i, maxResults=chunk_size, fields=fields)
        i += chunk_size
        issues += chunk
        if i >= chunk.total:
            break
    return issues

jira = JIRA(basic_auth=(USERNAME, API_TOKEN), options={'server':'https://auto-jira.atlassian.net'})
issues = get_all_issues(jira, "ASF-3", ["id"])


def insert_issue(issue_key, issue_content, table_name):
    heading2_num = 9999
    heading3_num = 9999
    heading4_num = 9999
    for i in range(len(issue_content)):
        if issue_content[i]['type'] == 'heading':
            try:    
                num = issue_content[i]['content'][0]['text'].split()[0]
                if issue_content[i]['attrs']['level'] == 2:
                    heading2_num = num.split('.')[1]
                elif issue_content[i]['attrs']['level'] == 3:
                    heading3_num = num.split('.')[2]
                elif issue_content[i]['attrs']['level'] == 4:
                    heading4_num = num.split('.')[3]
            except IndexError:
                pass    

    sql = f"INSERT INTO {table_name} (issue_key, heading2, heading3, heading4) VALUES (?,?,?,?)"

    params = (issue_key, heading2_num, heading3_num, heading4_num)
    try: 
        conn.execute(sql, params)
    except sqlite3.IntegrityError:
        pass


    conn.commit()


for issue in issues:
    issue_key = str(issue)
    issue_url = f"https://auto-jira.atlassian.net/rest/api/3/issue/{issue_key}"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    response = requests.get(issue_url, headers=headers, auth=(USERNAME, API_TOKEN))

    if response.status_code == 200:
        issue_all = response.json() 
        issue_summary = issue_all["fields"]["summary"]

        if issue_all["fields"]["description"] is not None:
            issue_content = issue_all["fields"]["description"]["content"]
        
        # [RS_ASF_UserInterface]_111001
        if issue_summary[1:3] == "RS":
            insert_issue(issue_key, issue_content, "RS_table")

        elif issue_summary[1:4] == "SRS":
            insert_issue(issue_key, issue_content, "SRS_table")


# name = RS | SRS
def sort_issue(name):

    query = f"""SELECT issue_key FROM {name}_table 
ORDER BY CAST(heading2 AS INTEGER),
CAST(heading3 AS INTEGER),
CAST(heading4 AS INTEGER);"""

    cursor = conn.execute(query)

    content = []

    for i in cursor:
        issue_key = i[0]
        issue_url = f"https://auto-jira.atlassian.net/rest/api/3/issue/{issue_key}"
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        response = requests.get(issue_url, headers=headers, auth=(USERNAME, API_TOKEN))

        if response.status_code == 200:
            issue_all = response.json() 

            if issue_all["fields"]["description"] is not None:
                issue_content = issue_all["fields"]["description"]["content"]
                content += issue_content 

    return content

RS_content_dup = sort_issue("RS")
SRS_content_dup = sort_issue("SRS")

def remove_duplicates(lst):
    seen = []
    result = []
    for item in lst:
        if item not in seen:
            seen.append(item)
            result.append(item)
    return result

RS_content = remove_duplicates(RS_content_dup)
SRS_content = remove_duplicates(SRS_content_dup)

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


update_page(auth, "1099170250", "RS", RS_content)
update_page(auth, "1103364100", "SRS", SRS_content)

conn.close()


