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

# Should reply with a 204 No Content
# In case there is an error, uncomment following lines to display the error response
# print('Response body:')
# print(json.dumps(r.json(), indent=2))
