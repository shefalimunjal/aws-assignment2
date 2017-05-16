from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from botocore.exceptions import ClientError


AWS_KEY = '****'
AWS_SECRET = '****'

def handler(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', aws_access_key_id=AWS_KEY , aws_secret_access_key=AWS_SECRET)
    table = dynamodb.Table('orders')

    order_id = event['params']['path']['order-id']

    response = table.get_item(
            Key={
                'order_id': order_id,
            }
        )
    order = response['Item']
    if 'ord' in order:
        order['order'] = order['ord']
        del order['ord']
    return order

