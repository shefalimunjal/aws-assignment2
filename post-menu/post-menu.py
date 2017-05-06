from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal


def handler(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', aws_access_key_id='AKIAIDNWS6UHSPMUZOXA' , aws_secret_access_key='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')
    table = dynamodb.Table('pizzashop')

    body = event['body-json']
    response = table.put_item(Item=body)
    return "200 OK"


