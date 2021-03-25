from ctes import AT_CONTEXT, AT_CONTEXT_LINK, URL_ENTITIES
import json
import requests

ENTITY_ID = 'urn:ngsi-ld:WaterConsumption:202D03'
MLMODEL_ID = 'urn:ngsi-ld:MLModel:1234'
DATASET_ID = 'urn:ngsi-ld:Dataset:1234'

HEADERS = {
    'Content-Type': 'application/json',
    'Link': AT_CONTEXT_LINK
}

r = requests.delete(URL_ENTITIES + ENTITY_ID + '/attrs/activeModels', params={'datasetId': DATASET_ID}, headers=HEADERS)
print(f'Response status code: {r.status_code}')

# Should reply with a 204 No Content
# In case there is an error, uncomment following lines to display the error response
# print('Response body:')
# print(json.dumps(r.json(), indent=2))
