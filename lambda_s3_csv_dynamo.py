'''
AWS Lambda function
write csv file into DynamoDB table after trigged by CloudWatch event when
  csv file is loaded into S3.
python script, runtime:Python 3.6
handler info: lambda_function.csv_reader
'''

import boto3

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')


def csv_reader(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    print(str(event))

    obj = s3.get_object(Bucket=bucket, Key=key)

    rows = obj['Body'].read().decode().split('\n')
    # decode() added in the above because there was an byte-type error
    # print(len(rows))
    # print(rows[1])
    table = dynamodb.Table('EvaluationTest')

    with table.batch_writer() as batch:
        for i in range(1, len(rows)+1):
        # for row in rows:
            if rows[i] is not None:
                list = rows[i].split(',')

                batch.put_item(
                    Item={
                        'Test_ID' : list[0],
                        'Membrane ID' : list[1],
                        'Membrane Name' : list[2],
                        'Membrane Material' : list[3],
                        'Company Name' : list[4],
                        'MWCO' : list[5],
                        'Passthru at 1.5X (mg/ml)' : list[6],
                        'Passthru at 3X (mg/ml)' : list[7],
                        'Passthru at 6X (mg/ml)' : list[8]
                    }

                )
            else: continue
