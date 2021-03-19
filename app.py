from flask import Flask, request
from mlpmodel import MLP_3hl_d2bn
from ctes import AT_CONTEXT, AT_CONTEXT_LINK
from ctes import MLMODEL_1_UUID, SUBS_MLPROCESSING_UUID
from ctes import SUBS_DATA_UUID, URL_PATCH_AGRICROPRECORD
from ctes import ENDPOINT_SUBS_QUERY, ENDPOINT_PREDICT
from ctes import URL_ENTITIES, URL_SUBSCRIPTION
import requests
import torch
import pickle
import numpy
from datetime import datetime
import pytz
import logging
import json


# Declare the redox model as a global variable, so that the model
# are instantiate once and not at each incoming request !
wheat_redox_model_3hl = None

# Same for the scaler
wheat_redox_scaler_3hl = None

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

        # Transform the spectrum string into an array of 256 float which is
        # the data type the ML algorithm is expecting
        spectrum = [float(item) for item in spectrum.split('-')]
        spectrum = numpy.array(spectrum).reshape(1, -1)
        logging.info(f'spectrum as numpy array: {spectrum}')

        # Round redox to 0 and transform to int to avoid displaying
        # values as 145.0 instead of 145
        spectrum_std = wheat_redox_scaler_3hl.transform(spectrum)
        redox_3hl = int(round(wheat_redox_model_3hl.predict(
            torch.Tensor(spectrum_std)), 0))
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

    # WHEAT #
    # loading scaler
    with open(
            './pytorch-models-wheat/wheat.redox.std.scaler.20210218.21h07.pickle',
            'rb') as f:
        wheat_redox_scaler_3hl = pickle.load(f)

    # Instantiate an empty model
    wheat_redox_model_3hl = MLP_3hl_d2bn()

    # Then load the models from file and set mode in eval mode (we're just
    # doing predictions, no training)
    wheat_redox_model_3hl.load_state_dict(
        torch.load(
            './pytorch-models-wheat/wheat.redox.model.20210218.21h07.pt'))
    wheat_redox_model_3hl.eval()

    # Run Flask server
    app.run(host='0.0.0.0', port=80)
