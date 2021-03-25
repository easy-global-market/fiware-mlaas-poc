# UUID
# MLMODEL
MLMODEL_1_UUID = 'urn:ngsi-ld:MLModel:redox-prediction:'\
    'd490e4ec-a007-493a-ba16-d00ed0ddd577'
SUBS_MLPROCESSING_UUID = 'urn:ngsi-ld:Subscription:MLModel'\
    ':redox-prediction:d490e4ec-a007-493a-ba16-d00ed0ddd577'
SUBS_DATA_UUID =\
    'urn:ngsi-ld:Subscription:62f5ebc1-0fcc-483b-acbf-2004a0671906'
AGRICROPRECORD_UUID =\
    'urn:ngsi-ld:AgriCropRecord:wheat:3913d09e-a082-4cda-b305-d203e04bb115'

# URL
URL_ENTITIES = 'https://stellio-dev.eglobalmark.com/ngsi-ld/v1/entities/'
URL_SUBSCRIPTION = 'https://stellio-dev.eglobalmark.com/ngsi-ld/v1/'\
    'subscriptions/'
URL_PATCH_AGRICROPRECORD = URL_ENTITIES + AGRICROPRECORD_UUID + '/attrs'
# Context
AT_CONTEXT = [
    'https://raw.githubusercontent.com/easy-global-market/ngsild-api-data-models/feature/mlaas-models/mlaas/jsonld-contexts/mlaas-compound.jsonld'
]

AT_CONTEXT_LINK = '<https://raw.githubusercontent.com/senseen/'\
    'ngsild-api-data-models/main/scanner/jsonld-contexts/'\
    'scanSmartMeter-compound.jsonld>; '\
    'rel=http://www.w3.org/ns/json-ld#context; type=application/json'

# ENDPOINTS
# Receiving notification with SubscriptionQuery
# local:
# ENDPOINT_SUBS_QUERY = 'http://127.0.0.1:5000/subscribe'
# AWS:
ENDPOINT_SUBS_QUERY = 'http://13.36.97.126/subscribe'

# Receiving notification of new data for making prediction
# local:
# ENDPOINT_PREDICT = 'http://127.0.0.1:5000/predict'
# AWS:
ENDPOINT_PREDICT = 'http://13.36.97.126/predict'
