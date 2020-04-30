import os
import sys
# Add vendor directory to module search path
PARENT_DIR = os.path.abspath(os.path.dirname(__file__))
VENDOR_DIR = os.path.join(PARENT_DIR, 'vendor')
sys.path.append(VENDOR_DIR)

import boto3
import json
from dynamodb_json import json_util as ddb_json
from dataclasses import dataclass, field

@dataclass
class Request:
    path: str
    http_method: str
    headers: dict
    query_string_parameters: dict
    path_parameters: dict
    stage_variables: dict
    request_context: dict
    body: str
    multi_value_headers: dict = field(default_factory=lambda: {})
    multi_value_query_string_parameters: dict = field(default_factory=lambda: {})

@dataclass
class Response:
    statusCode: int
    headers: dict = field(
        default_factory=lambda: {
            "Content-Type": 'application/json',
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        })
    isBase64Encoded: bool = False
    body: str = ""

    def set_header(self, key: str, value: str):
        self.headers[key] = value

def unmarshall_api_gateway_event(event: dict):
    return Request(path=event['path'],
                   http_method=event['httpMethod'],
                   headers=event['headers'],
                   multi_value_headers=event['multiValueHeaders'],
                   query_string_parameters=event['queryStringParameters'],
                   multi_value_query_string_parameters=event[
                       'multiValueQueryStringParameters'],
                   path_parameters=event['pathParameters'],
                   stage_variables=event['stageVariables'],
                   request_context=event['requestContext'],
                   body=event['body'])

def handler(event, _):
    request = unmarshall_api_gateway_event(event)
    response = None
    
    try:
        ddb = boto3.client('dynamodb')
        results = ddb.get_item(
            TableName='data-table',
            Key={
                'data':  {
                    'S': request.path_parameters['data']
                }
            }
        )
        if not results or not 'Item' in results:
            response = Response(400)
        else:
            json_ = ddb_json.loads(results['Item'])
            response = Response(200, body=json.dumps(json_))
    except Exception as err: 
        print(err)
        response = Response(500)
    
    return response.__dict__