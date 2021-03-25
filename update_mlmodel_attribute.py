from ctes import AT_CONTEXT, AT_CONTEXT_LINK, URL_ENTITIES
import json
import requests

ENTITY_ID = 'urn:ngsi-ld:MLModel:d490e4ec-a007-493a-ba16-d00ed0ddd577'
ATTRIBUTE_NAME = 'bentoPredictUrl'

HEADERS = {
    'Content-Type': 'application/json',
    'Link': AT_CONTEXT_LINK
}

json_d = {
    'value': 'http://127.0.0.1:5000/predict'
}

r = requests.patch(URL_ENTITIES + ENTITY_ID + '/attrs/' + ATTRIBUTE_NAME, json=json_d, headers=HEADERS)
print(f'Response status code: {r.status_code}')
if (r.status_code != 204):
    print(f'Error response is {json.dumps(r.json(), indent=2)}')
