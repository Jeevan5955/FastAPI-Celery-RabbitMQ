import json

import httpx


#Get example to call external API
def callGetApi(data: str) -> dict:
    url = 'http://universities.hipolabs.com/search'
    params = {}
    client = httpx.Client()
    response = client.get(url, params=params)
    response_json = json.loads(response.text)
    pass

#Post example to call external API
def callPostApi(data: str) -> dict:
    url = 'http://universities.hipolabs.com/search'
    params = {}
    client = httpx.Client()
    response = client.post(url, params=params)
    response_json = json.loads(response.text)
    pass
