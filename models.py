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
    ''' Acts as a mini ORM for getting model properties and saving to a database'''
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
        """
        Performs a looks of a primary key (hash) or GSI (username) and sets the
        database attributes into the model object
        ----------
        arg1 : key
            hash for the item
        arg2 : gsi
            global secondary Index

        Returns
        -------
        mixed
            Only makes a boolean return when something goes wrong

        """
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
        """
        Saves to the database

        Returns
        -------
        None

        """
        get_table_connection(self.table_name).put_item(Item=self.get_attributes())



class User(Model):
    table_name = 'usersTable'

    primary_key = 'id'

    global_secondary_index = 'username'

    global_secondary_name = 'userName'

    def check_password(self, request_password):
        """
        validates password against the database
        ----------
        arg1 : request_password
            password passed in on the request

        Returns
        -------
        boolean
            Returns the result of the password check
        """
        password, salt = self.get('password').split(':')
        return password == hashlib.sha256(salt.encode() + request_password.encode()).hexdigest()

    def get_current_step(self):
        """
        Pulls up the current registation step

        Returns
        -------
        String
            Returns link of to the current registation step
        """
        if self.get('rsvp_step_status') == None:
            return 'register-rsvp'
        elif self.get('profile_step_status') == None:
            return 'register-profile'
        elif self.get('activities_step_status') == None:
            return 'register-activities'
        elif self.get('hotel_step_status') == None:
            return 'register-hotel'
        else:
            return 'register-complete'
