from __future__ import print_function
import boto3
import json

print('Loading function')
with open('aws.creds') as f:
	creds = f.read().strip().split(',')
session = boto3.Session(aws_access_key_id=creds[0], aws_secret_access_key=creds[1])
dynamo = session.resource('dynamodb')



def respond(err, res=None):
	return {
		'statusCode': '400' if err else '200',
		'body': err.message if err else json.dumps(res),
		'headers': {
			'Content-Type': 'application/json',
			'Access-Control-Allow-Origin': '*'            
		},
	}


def get_database():
	table = dynamo.Table('disasterdata')
	items = table.scan()
	return respond(None, items)


def lambda_handler(event, context):
	'''Demonstrates a simple HTTP endpoint using API Gateway. You have full
	access to the request and response payload, including headers and
	status code.

	To scan a DynamoDB table, make a GET request with the TableName as a
	query string parameter. To put, update, or delete an item, make a POST,
	PUT, or DELETE request respectively, passing in the payload to the
	DynamoDB API as a JSON body.
	'''
	print("Received event: " + json.dumps(event, indent=2))

	# operations = {
	#     'DELETE': lambda dynamo, x: dynamo.delete_item(**x),
	#     'GET': lambda dynamo, x: dynamo.scan(**x),
	#     'POST': lambda dynamo, x: dynamo.put_item(**x),
	#     'PUT': lambda dynamo, x: dynamo.update_item(**x),
	# }


	operation = event['httpMethod']
	res = get_database()
	print(res)
	return res
	#return respond(None, "Hello World")
	# if operation in operations:
	#     payload = event['queryStringParameters'] if operation == 'GET' else json.loads(event['body'])
	#     return respond(None, operations[operation](dynamo, payload))
	# else:
	#     return respond(ValueError('Unsupported method "{}"'.format(operation)))
