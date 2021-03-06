from ctes import AT_CONTEXT, AT_CONTEXT_LINK, URL_ENTITIES
import json
import requests

ENTITY_ID = 'urn:ngsi-ld:WaterConsumption:202D03'

HEADERS = {
    'Content-Type': 'application/json',
    'Link': AT_CONTEXT_LINK
}

json_d = {
    'value': 126,
    'observedAt': '2021-03-25T15:35:00Z'
}

r = requests.patch(URL_ENTITIES + ENTITY_ID + '/attrs/litres', json=json_d, headers=HEADERS)
print(f'Response status code: {r.status_code}')
if (r.status_code != 204):
    print(f'Error response is {json.dumps(r.json(), indent=2)}')
