from ctes import AT_CONTEXT, AT_CONTEXT_LINK, URL_ENTITIES
import json
import requests

ENTITY_ID = 'urn:ngsi-ld:WaterConsumption:202D03'
MLMODEL_ID = 'urn:ngsi-ld:MLModel:d490e4ec-a007-493a-ba16-d00ed0ddd577'
DATASET_ID = 'urn:ngsi-ld:Dataset:d490e4ec-a007-493a-ba16-d00ed0ddd577'

HEADERS = {
    'Content-Type': 'application/json',
    'Link': AT_CONTEXT_LINK
}

r = requests.delete(URL_ENTITIES + ENTITY_ID + '/attrs/activeModels', params={'datasetId': DATASET_ID}, headers=HEADERS)
print(f'Response status code: {r.status_code}')
if (r.status_code != 204):
    print(f'Error response is {json.dumps(r.json(), indent=2)}')
