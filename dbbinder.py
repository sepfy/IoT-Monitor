import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb', region_name="ap-northeast-1")
table = dynamodb.Table('THSensor')

response = table.query(
    KeyConditionExpression=Key('CN').eq('asb1q')
)

items = response["Items"]
print(items[0]["payload"]["t"])
