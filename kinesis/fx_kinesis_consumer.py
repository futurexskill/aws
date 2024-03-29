# -*- coding: utf-8 -*-
"""fx_kinesis_consumer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zIuTu2TZ-Or4ElxeCk7imgLfOvusVImZ
"""

!pip install boto3 awscli

import getpass

# Input AWS credentials and region
aws_access_key_id = getpass.getpass('Enter AWS Access Key ID: ')
aws_secret_access_key = getpass.getpass('Enter AWS Secret Access Key: ')
aws_region = input('Enter AWS Region: ')

!aws configure set aws_access_key_id $aws_access_key_id
!aws configure set aws_secret_access_key $aws_secret_access_key
!aws configure set default.region $aws_region

stream_name = 'Fxweatherstream'

import boto3
import json
import time
# Initialize Kinesis client
kinesis_client = boto3.client('kinesis', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)

def get_shard_iterator():
    response = kinesis_client.get_shard_iterator(
        StreamName=stream_name,
        ShardId='shardId-000000000003',  # Replace with your shard ID
        ShardIteratorType='TRIM_HORIZON'
    )
    return response['ShardIterator']

def get_records(shard_iterator):
    response = kinesis_client.get_records(
        ShardIterator=shard_iterator,
        Limit=10
    )
    return response.get('Records', []), response.get('NextShardIterator')

def process_weather_data(data):
    print(f"Received Weather Data: {data}")

if __name__ == "__main__":
    shard_iterator = get_shard_iterator()

    while True:
        records, next_shard_iterator = get_records(shard_iterator)
        for record in records:
            data = json.loads(record['Data'])
            process_weather_data(data)

        if not next_shard_iterator:
            print("No more records in the shard. Exiting.")
            break

        shard_iterator = next_shard_iterator
        time.sleep(2)  # Add a delay between reads (adjust as needed)

!aws kinesis delete-stream --stream-name Fxweatherstream

