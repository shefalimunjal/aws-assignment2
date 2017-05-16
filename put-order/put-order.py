from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from botocore.exceptions import ClientError
from time import gmtime, strftime

AWS_KEY = '****'
AWS_SECRET = '****'

def handler(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', aws_access_key_id=AWS_KEY , aws_secret_access_key=AWS_SECRET)

    # get parameters from request
    order_id = event['params']['path']['order-id']
    input = int(event['body-json']["input"])

    #get order from database
    table = dynamodb.Table('orders')

    response = table.get_item(
            Key={
                'order_id': order_id,
            }
        )
    order = response['Item']

    # get menu from database
    menu_id = order['menu_id']
    table = dynamodb.Table('pizzashop')

    response = table.get_item(
            Key={
                'menu_id': menu_id,
            }
        )
    menu = response['Item']


    table = dynamodb.Table('orders')

    input_for_selection = False
    input_for_size = False

    if "ord" not in order or 'selection' not in order['ord']:
        input_for_selection = True
    elif 'size' not in order['ord']:
        input_for_size = True


    if input_for_selection:
        update_expression = "set ord = :o"
        expression_attribute_values = {":o" : {'selection': menu['selection'][input - 1]}}
        response = table.update_item(
        Key={
           'order_id': order_id,
        },
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues="UPDATED_NEW"
        )
        index = 0
        all_items = ''
        for item in menu['size']:
            index +=1
            all_items += str(index) + '. ' + item + ','
        all_items = all_items[:-1]


        message =  "Which size do you want? " +  all_items
        return {"message" : message}
    elif input_for_size:
        ord = order['ord']
        ord['size'] = menu['size'][input -1]
        ord['costs'] = menu['price'][input - 1]
        ord['order_time'] = strftime("%Y-%m-%d@%H:%M:%S", gmtime())

        update_expression = "set ord = :o, order_status = :o_s"
        expression_attribute_values = {":o" : ord, ":o_s" : "processing"}
        response = table.update_item(
        Key={
           'order_id': order_id,
        },
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues="UPDATED_NEW"
        )

        return {"Message": "Your order costs $" + str(ord['costs']) + ". We will email you when the order is ready. Thank you!"}
    else:
        return "200 OK"


    #update_expression = "set "
    #expression_attribute_values = {}
    #for key in body:
    #    update_expression += key + " = :" + key + ","
    #    expression_attribute_values[":" + key] = body[key]

    #update_expression = update_expression[:-1]

    #response = table.update_item(
    #Key={
    #    'menu_id': menu_id,
    #},
    #UpdateExpression=update_expression,
    #ExpressionAttributeValues=expression_attribute_values,
    #ReturnValues="UPDATED_NEW"
    #)
    return event
