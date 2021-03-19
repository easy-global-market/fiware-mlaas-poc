from flask import Flask, request
from ctes import AT_CONTEXT, AT_CONTEXT_LINK
from ctes import MLMODEL_1_UUID, SUBS_MLPROCESSING_UUID
from ctes import SUBS_DATA_UUID, URL_PATCH_AGRICROPRECORD
from ctes import ENDPOINT_SUBS_QUERY, ENDPOINT_PREDICT
from ctes import URL_ENTITIES, URL_SUBSCRIPTION
import requests
import numpy
from datetime import datetime
import pytz
import logging
import json
import pickle


# Setting logs
logging.basicConfig(filename='/data/predict-redox.log', level=logging.INFO)


app = Flask(__name__)


@app.route('/subscribe', methods=['POST'])
def create_subscription():
    '''
    Subscribe to the data that has to be used for predicting
    What is received here is notification of a new MLProcessing
    It contains a reference to the query that must be used to create
    a subscription to a data
    '''
    if request.method == 'POST':
        logging.info(f'content type: {request.content_type}')
        logging.info(f'content length: {request.content_length}')
        logging.info(f'content encoding: {request.content_encoding}')
        logging.info('Before request.get_json')
        data = json.loads(request.get_data(as_text=True))
        logging.info(f'Raw data json: {data}')

        # retrieve the subscription query:
        refSubscriptionQuery =\
            data['data'][0]['refSubscriptionQuery']['object']
        logging.info(f'SubscriptionQuery: {refSubscriptionQuery}')

        # GET REQUEST
        # Expecting 200 with body
        r = requests.get(URL_ENTITIES+refSubscriptionQuery,
                         headers=HEADERS_GET)
        logging.info(f'Status code GET SubscriptionQuery: {r.status_code}')
        logging.info(f'SubscriptionQuery: {refSubscriptionQuery}')

        # Retrieve the data that make up the query
        # This part is quite specific to this example, i.e. difficult to have a
        # view on how specific/generic the information contained in the
        # notification should/could be.
        data_entity_id = r.json()['entityID']['value']
        logging.info(f'data_entity_id: {data_entity_id}')

        # Subscribe to the data (only absorbance property is of interest)
        json_d = {
            '@context': AT_CONTEXT,
            'id': SUBS_DATA_UUID,
            'type': 'Subscription',
            'entities': [
                {
                    'type': 'AgriCropRecord',
                    'id': data_entity_id
                }
            ],
            'watchedAttributes': ['absorbance'],
            'notification': {
                'endpoint': {
                    'uri': ENDPOINT_PREDICT,
                    'accept': 'application/json'
                },
                'attributes': ['absorbance']
            }
        }

        # POST REQUEST
        # Expecting 201
        r = requests.post(URL_SUBSCRIPTION, json=json_d, headers=HEADERS_POST)
        logging.info(f'Status code creation of AgriCropRecord Subscription:\
                     {r.status_code}')

    # Finally return a 200 with no body to Context Broker
    return({})


@app.route('/predict', methods=['POST'])
def predict():
    '''
    Receive a notification from Context Broker (new data available for
    prediction) and predict.
    '''
    if request.method == 'POST':
        # Get the data, that would be a NGSI-LD format
        data = json.loads(request.get_data(as_text=True))
        logging.info(f'Raw data json: {data}')

        # We're taking the first spectrum in the list of spectra
        # IT MAY NOT BE THE ONE THAT HAS BEEN UPDATED (several datasetId)
        # So far no idea how to susbcribe to the datasetId that has been
        # updated in the absorbance property.
        spectrum = data['data'][0]['absorbance'][0]['value']
        logging.info(f'raw spectrum: {spectrum}')

        # Transform the spectrum string into an array of 256 float
        spectrum = [float(item) for item in spectrum.split('-')]
        spectrum = numpy.array(spectrum).reshape(1, -1)
        logging.info(f'spectrum as numpy array: {spectrum}')

        # 'Predict' redox, i.e. takes the first value of the absorbance,
        # multiply by 1000 and convert to an int!
        redox_3hl = int(spectrum[0][0]*1000)
        logging.info(f'Redox prediction: {redox_3hl}')

        # Then POST the redox predicted value into the AgriCropRecord entity
        # Set the observed_at property to the current time with the appropriate
        # timezone.
        timezone_France = pytz.timezone('Europe/Paris')
        observed_at = timezone_France.\
            localize(datetime.now().replace(microsecond=0)).isoformat()
        logging.info(f'observed_at: {observed_at}')

        json_d = {
            '@context': AT_CONTEXT,
            'redox': [
                {
                    'type': 'Property',
                    'value': redox_3hl,
                    'observedAt': observed_at,
                    'datasetId': 'urn:ngsi-ld:redox:predicted'
                }
            ]
        }

        # POST REQUEST
        # Expecting 204
        r = requests.post(URL_PATCH_AGRICROPRECORD, json=json_d,
                          headers=HEADERS_POST)
        logging.info(f'Status code updating value of redox:{r.status_code}')

    # Finally return a 200 with no body to Context Broker
    return({})


if __name__ == '__main__':
    '''
    main: Load the models and then run Flask!
    '''
    # Load access_token
    with open('./stellio-dev-access.token', 'rb') as f:
        ACCESS_TOKEN = pickle.load(f)

    # HEADERS
    # POST
    HEADERS_POST = {
        'Authorization': 'Bearer ' + ACCESS_TOKEN,
        'Content-Type': 'application/ld+json'
    }

    # GET
    HEADERS_GET = {
        'Authorization': 'Bearer ' + ACCESS_TOKEN,
        'Content-Type': 'application/ld+json',
        'Link': AT_CONTEXT_LINK
    }

    # Create an entity MLModel
    json_d = {
        '@context': AT_CONTEXT,
        'id': MLMODEL_1_UUID,
        'type': 'MLModel',
        'name': {
            'type': 'Property',
            'value': 'Redox pontential'
        },
        'description': {
            'type': 'Property',
            'value': 'Redox pontential prediction from NIR absorbance'
        },
        'algorithm': {
            'type': 'Property',
            'value': 'Multi-Layer Perceptron'
        },
        'version': {
            'type': 'Property',
            'value': 0.1
        },
        'inputAttributes': {
            'type': 'Property',
            'value': ['absorbance', 'temperature']
        },
        'outputAttributes': {
            'type': 'Property',
            'value': 'redox'
        }
    }

    # POST REQUEST
    # Expecting 201 response
    r = requests.post(URL_ENTITIES, json=json_d, headers=HEADERS_POST)
    logging.info(f'Status code creation of MLModel entity: {r.status_code}')

    # Subscribe to MLProcessing
    json_d = {
        '@context': AT_CONTEXT,
        'id': SUBS_MLPROCESSING_UUID,
        'type': 'Subscription',
        'entities': [
            {
                'type': 'MLProcessing'
            }
        ],
        'q': 'refMLModel=="'+MLMODEL_1_UUID+'"',
        'notification': {
            'endpoint': {
                'uri': ENDPOINT_SUBS_QUERY,
                'accept': 'application/json'
            },
            'attributes': ['refSubscriptionQuery']
        }
    }

    # POST REQUEST
    # Expecting 201 response
    r = requests.post(URL_SUBSCRIPTION, json=json_d, headers=HEADERS_POST)
    logging.info(f'Status code creation of MLModel subscription: \
                 {r.status_code}')

    # Run Flask server
    app.run(host='0.0.0.0', port=80)
