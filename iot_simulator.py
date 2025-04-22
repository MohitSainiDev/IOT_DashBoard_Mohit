from decimal import Decimal
import boto3
from datetime import datetime
import time

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('MachineHealthData')

# Simulate and send data every few seconds
while True:
    # Example of simulated data (replace this with your actual data generation)
    data = {
        'machine_id': 'M1',
        'timestamp': str(datetime.now()),  # Current time as timestamp
        'temperature': Decimal('85.7'),  # Convert float to Decimal
        'vibration': Decimal('0.041'),  # Convert float to Decimal
        'power': Decimal('224.35')  # Convert float to Decimal
    }

    # Print the data being sent (for debugging purposes)
    print("Sending data:", data)

    try:
        # Insert data into DynamoDB
        table.put_item(Item=data)
        print("Data successfully inserted!")
    except Exception as e:
        print("Error inserting data:", e)

    # Sleep for a few seconds before sending next data
    time.sleep(5)  # Adjust the sleep time as needed
