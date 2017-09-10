import boto3

with open('aws.creds') as f:
	creds = f.read().strip().split(',')
session = boto3.Session(aws_access_key_id=creds[0], aws_secret_access_key=creds[1])
dynamodb = dynamodb = session.resource('dynamodb', region_name='us-east-1')

# ['address', 'username', 'tweet', 'timestamp', 'region']

def init_table():	

	table = dynamodb.create_table(
	    TableName='disasterdata',
	    KeySchema=[
	        {
	            'AttributeName': 'address',
	            'KeyType': 'HASH'  #Partition key
	        },
	       
	        
	    ],
	    AttributeDefinitions=[
	        {
	            'AttributeName': 'address',
	            'AttributeType': 'S'
	        },
	    ],
	    ProvisionedThroughput={
	        'ReadCapacityUnits': 10,
	        'WriteCapacityUnits': 10
	    }
	)

class DBWriter(object):

	def __init__(self):
		self.items = []

	def add_item(self, address, username, tweet, timestamp, region):
		item = {}
		item['address'] = address
		item['username'] = username
		item['tweet'] = tweet
		item['timestamp'] = timestamp
		item['region'] = region
		self.items.append(item)

	def write_to_db(self):
		table = dynamodb.Table('disasterdata')
		with table.batch_writer() as batch:
		    for item in items
		        batch.put_item(
		            item
		        )