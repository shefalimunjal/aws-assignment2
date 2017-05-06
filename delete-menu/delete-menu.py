from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', region_name='us-west-2', aws_access_key_id='AKIAIDNWS6UHSPMUZOXA' , aws_secret_access_key='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')


table = dynamodb.Table('pizzashop')

def handler(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', aws_access_key_id='AKIAIDNWS6UHSPMUZOXA' , aws_secret_access_key='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')
    table = dynamodb.Table('pizzashop')

    menu_id = event['params']['path']['menu-id']

    response = table.delete_item(
        Key={
            'menu_id': menu_id
        }
    )

    return "200 OK"




