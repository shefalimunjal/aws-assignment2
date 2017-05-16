from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal

AWS_KEY = '****'
AWS_SECRET = '****'

def handler(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', aws_access_key_id=AWS_KEY , aws_secret_access_key=AWS_SECRET)
    table = dynamodb.Table('orders')

    body = event['body-json']
    response = table.put_item(Item=body)

    menu_id = body['menu_id']
    table = dynamodb.Table('pizzashop')
    menu = table.get_item(
            Key={
                'menu_id': menu_id,
            }
    )

    selection = menu['Item']['selection']
    index = 0
    all_items = ''
    for item in selection:
        index +=1
        all_items += str(index) + '. ' + item + ','
    all_items = all_items[:-1]


    message =  "Hi " +  body['customer_name'] + ', please choose one of these selection: ' +  all_items
    return {"message" : message}
    #return menu





