from ctes import AT_CONTEXT, AT_CONTEXT_LINK, URL_ENTITIES
import json
import requests

ENTITY_ID = 'urn:ngsi-ld:WaterConsumption:202D03'
MLMODEL_ID = 'urn:ngsi-ld:MLModel:d490e4ec-a007-493a-ba16-d00ed0ddd578'
DATASET_ID = 'urn:ngsi-ld:Dataset:d490e4ec-a007-493a-ba16-d00ed0ddd578'

HEADERS = {
    'Content-Type': 'application/json',
    'Link': AT_CONTEXT_LINK
}

json_d = {
    'activeModels': {
        'type': 'Relationship',
        'object': MLMODEL_ID,
        'datasetId': DATASET_ID
    }
}

r = requests.post(URL_ENTITIES + ENTITY_ID + '/attrs', json=json_d, headers=HEADERS)
print(f'Response status code: {r.status_code}')
if (r.status_code != 204):
    print(f'Error response is {json.dumps(r.json(), indent=2)}')
