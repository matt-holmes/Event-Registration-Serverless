def get_table_connection(table_name):
    try:
        boto3
    except NameError:
        import boto3

    dynamodb = boto3.resource('dynamodb',
                region_name='us-east-2',
                endpoint_url='https://dynamodb.us-east-2.amazonaws.com')
    return dynamodb.Table(table_name)
