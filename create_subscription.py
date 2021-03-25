from ctes import AT_CONTEXT, ENDPOINT_PREDICT, URL_ENTITIES, URL_SUBSCRIPTION
import requests

SUBSCRIPTION_UUID = 'urn:ngsi-ld:Subscription:62f5ebc1-0fcc-483b-acbf-2004a0671906'

HEADERS = {
    # 'Authorization': 'Bearer ' + ACCESS_TOKEN,
    'Content-Type': 'application/ld+json'
}

json_d = {
    '@context': AT_CONTEXT,
    'id': SUBSCRIPTION_UUID,
    'type': 'Subscription',
    'entities': [
        {
            'type': 'WaterConsumption'
        }
    ],
    'notification': {
        'endpoint': {
            'uri': ENDPOINT_PREDICT,
            'accept': 'application/json'
        }
    }
}

r = requests.post(URL_SUBSCRIPTION, json=json_d, headers=HEADERS)
print(f'Status code creation of subscription: {r.status_code}')
