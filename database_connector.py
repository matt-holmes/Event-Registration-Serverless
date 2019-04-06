def get_table_connection(table_name):
    """
    Returns a database connection for a given table
    ----------
    arg1 : table_name
        Table name for the connection

    Returns
    -------
    boto3 object
        a connection for the given table

    """
    try:
        boto3
    except NameError:
        import boto3

    dynamodb = boto3.resource('dynamodb',
                region_name='us-east-2',
                endpoint_url='https://dynamodb.us-east-2.amazonaws.com')
    return dynamodb.Table(table_name)
