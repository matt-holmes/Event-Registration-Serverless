import hashlib
from database_connector import get_table_connection
from abc import ABCMeta, abstractproperty

class AbstractModel(metaclass=ABCMeta):
    @abstractproperty
    def table_name(self):
        pass

    @abstractproperty
    def primary_key(self):
        pass

    @abstractproperty
    def global_secondary_index(self):
        pass

    @abstractproperty
    def global_secondary_name(self):
        pass



class Model(AbstractModel):
    attributes = {}

    table_name = ''

    primary_key = ''

    global_secondary_index = ''

    global_secondary_name = ''

    def __init__(self, attributes = {}):
        self.attributes = attributes

    def set_attributes(self, attributes):
        self.attributes = attributes

    def set_attribute(self, attribute, value):
        self.attributes[attribute] = value

    def get_attributes(self):
        return self.attributes

    def get(self, attribute):
        if attribute in self.get_attributes():
            return self.attributes[attribute]
        else:
            return None

    def set(self, attribute, value):
        self.attributes[attribute] = value

    def find(self, key = False, gsi = False):
        try:
            ClientError
        except NameError:
            from botocore.exceptions import ClientError
            from boto3.dynamodb.conditions import Key, Attr
        try:
            if key and gsi == False:
                attributes = get_table_connection(self.table_name).get_item(
                    Key={
                        self.primary_key : key,
                    }
                )
                if 'Item' in attributes:
                    attributes = attributes['Item']
            elif key and gsi == True:
                attributes = get_table_connection(self.table_name).query(
                    IndexName=self.global_secondary_name,
                    KeyConditionExpression=Key(self.global_secondary_index).eq(key)
                )
                if 'Items' in attributes and len(attributes['Items']) == 1:
                    attributes = attributes['Items'][0]
                else:
                    return False

            self.set_attributes(attributes)
        except ClientError:
            self.set_attributes({})

    def save(self):
        get_table_connection(self.table_name).put_item(Item=self.get_attributes())



class User(Model):
    table_name = 'usersTable'

    primary_key = 'id'

    global_secondary_index = 'username'

    global_secondary_name = 'userName'

    def check_password(self, request_password):
        password, salt = self.get('password').split(':')
        return password == hashlib.sha256(salt.encode() + request_password.encode()).hexdigest()
