import json
import uuid
from datetime import datetime, timezone
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('s79010396-posts')

def handler(event, context):
    try:
        body = json.loads(event.get('body') or '{}')
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Invalid JSON body'})
        }

    now = datetime.now(timezone.utc).isoformat()
    item = {
        'postId': str(uuid.uuid4()),
        'title': body.get('title', 'Untitled'),
        'content': body.get('content', ''),
        'author': body.get('author', 'Anonymous'),
        'created_at': now,
        'updated_at': now,
    }
    for optional in ('snippet', 'tags', 'feature_image', 'images'):
        if body.get(optional):
            item[optional] = body[optional]

    table.put_item(Item=item)

    return {
        'statusCode': 201,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(item)
    }
