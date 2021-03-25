from ctes import AT_CONTEXT
from ctes import URL_ENTITIES
import json
import requests

HEADERS = {
    'Content-Type': 'application/ld+json'
}

# Sample WaterConsumption entity for tests purposes
json_d = {
    '@context': AT_CONTEXT,
    'id': 'urn:ngsi-ld:WaterConsumption:202D03',
    'type': 'WaterConsumption',
    'dma': {
        'type': 'Property',
        'value': '202D03'
    },
    'litres': {
        'type': 'Property',
        'value': 6662.5,
        'observedAt': '2021-03-21T23:00:00.000Z',
        'unitCode': 'LTR'
    },
    '@context': [
        'https://raw.githubusercontent.com/easy-global-market/ngsild-api-data-models/feature/mlaas-models/mlaas/jsonld-contexts/mlaas-compound.jsonld'
    ]
 }

r = requests.post(URL_ENTITIES, json=json_d, headers=HEADERS)
print(f'Status code creation of WaterConsumption entity: {r.status_code}')
if (r.status_code != 201):
    print(f'Error response is {json.dumps(r.json(), indent=2)}')

