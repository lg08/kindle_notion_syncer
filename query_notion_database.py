import requests
import json
import os

database_ID = os.environ.get("database_ID")
secret_Key = os.environ.get("secret_Key")

def get_pageid_for_title(title):
    url = f"https://api.notion.com/v1/databases/{database_ID}/query"
    payload = {
        "page_size": 100,
        "filter": {
            "property": "Title",
            "rich_text": {
                "equals": title
            }
        }
    }
    headers = {
        "Accept": "application/json",
        "Notion-Version": "2022-02-22",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {secret_Key}"
    }

    response = requests.post(url, json=payload, headers=headers)

    # print(response.text)

    data = json.loads(response.text)
    print("RIGHT BEFORE RESULSTS-----------------")
    print(data)
    if len(data['results']) == 0:
        return None
    page_id = data['results'][0]['id']
    return page_id



def get_list_of_paragraphs_for_page_with_title(title):
    page_id = get_pageid_for_title(title)
    print(page_id)


    url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100"

    headers = {
        "Accept": "application/json",
        "Notion-Version": "2022-02-22",
        "Authorization": f"Bearer {secret_Key}"
    }

    response = requests.get(url, headers=headers)

    paragraphs = []
    data = json.loads(response.text)
    for item in data['results']:
        if 'quote' in item.keys():
            for words in item['quote']['rich_text']:
                stringer = (words['plain_text'], "highlight")
        elif 'callout' in item.keys():
            for words in item['callout']['rich_text']:
                stringer = (words['plain_text'], "note")

        paragraphs.append(stringer)

    return paragraphs


def append_items_to_page(title, items):
    children_list = []
    for item in items:
        if item[1] == "highlight":
            children_list.append(
                {
                    "type": "quote",
                    "quote": {
                        "rich_text": [{
                            "type": "text",
                            "text": {
                                "content":item[0],
                            },
                        }],
                        "color": "default"
                    }
                }
            )
        else:
            children_list.append(
                {
                    "type": "callout",
                    "callout": {
                        "rich_text": [{
                            "type": "text",
                            "text": {
                                "content":item[0],
                            },
                        }],
                        "icon": {
                            "emoji": "⭐"
                        },
                        "color": "default"
                    }
                }
            )

    page_id = get_pageid_for_title(title)

    url = f"https://api.notion.com/v1/blocks/{page_id}/children"

    payload = {
        "children": children_list
    }
    headers = {
        "Accept": "application/json",
        "Notion-Version": "2022-02-22",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {secret_Key}"
    }

    response = requests.patch(url, json=payload, headers=headers)

    #print(response.text)



def create_page(title, author, paragraph_list):
    url = "https://api.notion.com/v1/pages"
    children_list = []
    for text in paragraph_list:
        if text[1] == "highlight":
            children_list.append(
                {
                    "type": "quote",
                    "quote": {
                        "rich_text": [{
                            "type": "text",
                            "text": {
                                "content":text[0],
                            },
                        }],
                        "color": "default"
                    }
                }
            )
        else:
            children_list.append(
                {
                    "type": "callout",
                    "callout": {
                        "rich_text": [{
                            "type": "text",
                            "text": {
                                "content":text[0],
                            },
                        }],
                        "icon": {
                            "emoji": "⭐"
                        },
                        "color": "default"
                    }
                }
            )


    payload = {
        "children": children_list ,
        "parent": {
            "type": "database_id",
            "database_id": database_ID
        },
        "properties": {
            "Title": {
                "title": [
                    {
                        "type": "text",
                        "text": {
                                "content": title
                        }
                    }
                ]
            },
            "Author": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": author
                        }
                    },
                ]
            }
        }
    }
    headers = {
        "Accept": "application/json",
        "Notion-Version": "2022-02-22",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {secret_Key}"
    }

    response = requests.post(url, json=payload, headers=headers)

