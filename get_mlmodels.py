from ctes import AT_CONTEXT, AT_CONTEXT_LINK, URL_ENTITIES
import json
import requests

HEADERS = {
    # 'Authorization': 'Bearer ' + ACCESS_TOKEN,
    'Content-Type': 'application/ld+json',
    'Link': AT_CONTEXT_LINK
}

r = requests.get(URL_ENTITIES, params={'type': 'MLModel'}, headers=HEADERS)
print(json.dumps(r.json(), indent=2))