'''
AWS Lambda function
Create a new DynamoDB table and then write JSON file into the DynamoDB table
after trigged by CloudWatch event when JSON file is loaded into S3
python script, runtime:Python 3.6
handler info: lambda_function.mynewdynamo
'''
import boto3
import json

# Get the service resource.
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

def mynewdynamo(event, context):

#Event trigger from S3 bucket upload

    print(str(event))

    bucket = event['Records'][0]['s3']['bucket']['name']
    print(bucket)

    json_file_name = event['Records'][0]['s3']['object']['key']
    print(json_file_name)

    json_object = s3_client.get_object(Bucket=bucket, Key=json_file_name)

    jsonFileReader = json_object['Body'].read()

    jsonDict = json.loads(jsonFileReader)

# Create the DynamoDB table.
    table = dynamodb.create_table(
        TableName='mycustomers5',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'email',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'email',
                'AttributeType': 'S'
        }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

# Wait until the table exists.
    table.meta.client.get_waiter('table_exists').wait(TableName='mycustomers5')

# Put items into talbe
    table.put_item(Item = jsonDict)

# Print out some data about the table.
    print(table.item_count)

    return 'Hello from Lambda'
