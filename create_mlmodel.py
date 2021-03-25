from ctes import AT_CONTEXT
from ctes import URL_ENTITIES
import requests
import json

MLMODEL_UUID = 'urn:ngsi-ld:MLModel:d490e4ec-a007-493a-ba16-d00ed0ddd578'
MLMODEL_NAME = "Consumption prediction"
MLMODEL_DESCRIPTION = "Consumption prediction from litres information on a specific DMA"
MLMODEL_ALGORITHM = "Multi-Layer Perceptron"
MLMODEL_VERSION = 0.2
MLMODEL_PREDICT_URL = "http://127.0.0.1:5000/predict"

HEADERS = {
    'Content-Type': 'application/ld+json'
}

# Template for a MLModel entity, adapt the variables above
json_d = {
    '@context': AT_CONTEXT,
    'id': MLMODEL_UUID,
    'type': 'MLModel',
    'name': {
        'type': 'Property',
        'value': MLMODEL_NAME
    },
    'description': {
        'type': 'Property',
        'value': MLMODEL_DESCRIPTION
    },
    'algorithm': {
        'type': 'Property',
        'value': MLMODEL_ALGORITHM
    },
    'version': {
        'type': 'Property',
        'value': MLMODEL_VERSION
    },
    'inputAttributes': {
        'type': 'Property',
        'value': ['litres']
    },
    'outputAttributes': {
        'type': 'Property',
        'value': 'consumption'
    },
    'bentoPredictUrl': {
        'type': 'Property',
        'value': MLMODEL_PREDICT_URL
    }
}

r = requests.post(URL_ENTITIES, json=json_d, headers=HEADERS)
print(f'Status code creation of MLModel entity: {r.status_code}')
if (r.status_code != 201):
    print(f'Error response is {json.dumps(r.json(), indent=2)}')
