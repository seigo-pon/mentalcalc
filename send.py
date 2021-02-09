import boto3
import json
import os
from boto3.dynamodb.types import TypeDeserializer
from datetime import datetime, timedelta, timezone

deserializer = TypeDeserializer()

def deserialize(image):
    d = {}
    for key in image:
        d[key] = deserializer.deserialize(image[key])
    return d

def lambda_handler(event, context):
    topic_arn = os.environ['SNS_TOPIC_ARN']
    JST = timezone(timedelta(hours=+9), 'JST')

    try:
        if event['Records'][0]['eventName'] != 'INSERT':
            return {
                'statusCode': 403
            }

        newData = deserialize(event['Records'][0]['dynamodb']['NewImage'])

        uid = newData['uid']
        created_at = datetime.fromtimestamp((newData['created_at'] / 1000), JST)
        result = json.loads(newData['result'])

        operate = '足し算' if result['operate'] == '足す' else '引き算'
        max_number = result['max_number']
        correct_question_list = list(filter(lambda x: x['is_correct'], result['question_list']))

        sns_client = boto3.client('sns')
        sns_client.publish(
            TopicArn=topic_arn,
            Subject='【Alexa】暗算太郎で新着の計算がありました',
            Message='{}に計算されました。\n計算は{}でした。\n最大値は{}でした。\n10問中{}問が正解でした。'.format(
                created_at.strftime('%Y/%m/%d %H:%M:%S'),
                operate,
                max_number,
                len(correct_question_list)
            )
        )
        return {
            'statusCode': 200
        }

    except Exception as e:
        print('error', e)
        return {
            'statusCode': 400
        }
