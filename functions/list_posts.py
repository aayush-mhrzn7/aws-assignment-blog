import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('s79010396-posts')

def handler(event, context):
    response = table.scan()
    items = response['Items']

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(items)
    }
