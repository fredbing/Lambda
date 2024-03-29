'''
AWS Lambda function
write JSON file into DynamoDB table after trigged by CloudWatch event when
  JSON file is loaded into S3.
python script, runtime:Python 3.6
handler info: lambda_function.s3_json_dynamo
'''
import boto3
import json

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

def s3_json_dynamo(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    json_file_name = event['Records'][0]['s3']['object']['key']
    json_object = s3_client.get_object(Bucket=bucket, Key=json_file_name)

    jsonFileReader = json_object['Body'].read()
    jsonDict = json.loads(jsonFileReader)
    table = dynamodb.Table('myemployees')
    table.put_item(Item = jsonDict)

#   print(bucket)
#   print(json_file_name)
#   print(str(event))
    return 'Hello from Lambda'
