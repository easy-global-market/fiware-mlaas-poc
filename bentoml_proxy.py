from flask import Flask, request
from ctes import AT_CONTEXT_LINK, URL_ENTITIES
from slugify import slugify
from datetime import datetime
import numpy
import requests
import pytz
import logging
import json


# Setting logs
logging.basicConfig(filename='./bentoml_proxy.log', level=logging.INFO)


app = Flask(__name__)

def getMlModel(mlModelId):
    HEADERS = {
        'Content-Type': 'application/json',
        'Link': AT_CONTEXT_LINK
    }

    r = requests.get(URL_ENTITIES + mlModelId, headers=HEADERS)
    if (r.status_code == 200):
        return r.json()
    else:
        logging.info(f'Unexpected response when retrieving MLModel entity: {r.status_code}')
        logging.info(f'Response is {json.dumps(r.json(), indent=2)}')
        return None

def sendPredictToBento(predictUrl, inputData):
    HEADERS = {
        'Content-Type': 'application/json'
    }

    r = requests.post(predictUrl, inputData, headers=HEADERS)
    if (r.status_code == 200):
        return r.json()
    else:
        logging.info(f'Unexpected response received from Bento: {r.status_code}')
        logging.info(f'Response is {json.dumps(r.json(), indent=2)}')
        return None

# If a transformation is needed before sending data to the ML model
# adapt this method
def transformInputValue(inputValue):
    return inputValue

@app.route('/predict', methods=['POST'])
def predict():
    '''
    Receive a notification from Context Broker (new data available for
    prediction) and predict.
    '''
    if request.method == 'POST':
        # Get the data entity that is inside the NGSI-LD notification
        data = json.loads(request.get_data(as_text=True))
        entity = data['data'][0]
        logging.info(f'Received entity: {entity}')

        # Loop through all the active models and send them the input value for a prediction
        mlmodels = entity['activeModels']
        for mlModelRel in mlmodels:
            logging.info(f'Dealing with MLModel: {mlModelRel}')

            # get the MLModel entity from the Context Broker
            mlModelEntity = getMlModel(mlModelRel['object'])
            if (mlModelEntity is None):
                continue
            logging.info(f'Retrieved MLModel entity: {mlModelEntity}')

            # get the info we need from the MLModel entity
            bentoPredictUrl = mlModelEntity['bentoPredictUrl']['value']
            inputAttributes = mlModelEntity['inputAttributes']['value']
            outputAttributes = mlModelEntity['outputAttributes']['value']
            logging.info(f'ML Model info: {bentoPredictUrl} / {inputAttributes} / {outputAttributes}')

            # get and prepare the input value using inputAttribute information
            inputValue = entity[inputAttributes]['value']
            preparedInputValue = transformInputValue(inputValue)
            outputValue = sendPredictToBento(bentoPredictUrl, preparedInputValue)
            if (outputValue is None):
                continue

            # publish the predicted value into the source entity

            HEADERS = {
                'Content-Type': 'application/json',
                'Link': AT_CONTEXT_LINK
            }

            json_d = {
                outputAttributes: {
                    'type': 'Property',
                    'value': outputValue,
                    'observedAt': datetime.now().astimezone(pytz.UTC).isoformat(),
                    'datasetId': 'urn:ngsi-ld:Dataset:' + slugify(mlModelEntity['name']['value']) + ':' + slugify(str(mlModelEntity['version']['value'])),
                    'computedBy': {
                        'type': 'Relationship',
                        'object': mlModelEntity['id']
                    }
                }
            }

            postUrl = URL_ENTITIES + entity['id'] + '/attrs/'
            logging.info(f'Sending update to URL: {postUrl}')
            logging.info(json.dumps(json_d, indent=2))
            r = requests.post(postUrl, json=json_d, headers=HEADERS)
            logging.info(f'Status code sending the result: {r.status_code}')
            if (r.status_code != 204):
                logging.info(f'Received response:')
                logging.info(json.dumps(r.json(), indent=2))

    # Finally return a 200 with no body to Context Broker
    return({})


if __name__ == '__main__':

    # Run Flask server
    app.run(host='0.0.0.0', port=5000)
