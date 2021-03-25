# URL of the context broker
URL_ENTITIES = 'http://localhost:8080/ngsi-ld/v1/entities/'
URL_SUBSCRIPTION = 'http://localhost:8080/ngsi-ld/v1/subscriptions/'

# JSON-LD @context to use for the requests to the context broker
AT_CONTEXT = [
    'https://raw.githubusercontent.com/easy-global-market/ngsild-api-data-models/feature/mlaas-models/mlaas/jsonld-contexts/mlaas-compound.jsonld'
]

AT_CONTEXT_LINK = '<https://raw.githubusercontent.com/easy-global-market/'\
    'ngsild-api-data-models/feature/mlaas-models/mlaas/jsonld-contexts/'\
    'mlaas-compound.jsonld>; '\
    'rel=http://www.w3.org/ns/json-ld#context; type=application/json'

# ENDPOINTS
# Receiving notification with SubscriptionQuery
# local:
# ENDPOINT_SUBS_QUERY = 'http://127.0.0.1:5000/subscribe'
# AWS:
# ENDPOINT_SUBS_QUERY = 'http://13.36.97.126/subscribe'

# Receiving notification of new data for making prediction
# local:
ENDPOINT_PREDICT = 'http://10.0.1.3:5000/predict'
# AWS:
#ENDPOINT_PREDICT = 'http://13.36.97.126/predict'
