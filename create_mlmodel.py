from ctes import AT_CONTEXT
from ctes import URL_ENTITIES
import requests

MLMODEL_UUID = 'urn:ngsi-ld:MLModel:d490e4ec-a007-493a-ba16-d00ed0ddd577'
MLMODEL_NAME = "Consumption prediction"
MLMODEL_DESCRIPTION = "Consumption prediction from litres information on a specific DMA"
MLMODEL_ALGORITHM = "Multi-Layer Perceptron"
MLMODEL_VERSION = 0.1
MLMODEL_PREDICT_URL = "https://some-provider/predict"


HEADERS_POST = {
    # 'Authorization': 'Bearer ' + ACCESS_TOKEN,
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

# POST REQUEST
# Expecting 201 response
r = requests.post(URL_ENTITIES, json=json_d, headers=HEADERS_POST)
print(f'Status code creation of MLModel entity: {r.status_code}')
