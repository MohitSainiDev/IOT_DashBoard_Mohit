from decimal import Decimal
import boto3
from datetime import datetime
import time


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('MachineHealthData')


while True:

    data = {
        'machine_id': 'M1',
        'timestamp': str(datetime.now()),
        'temperature': Decimal('85.7'),
        'vibration': Decimal('0.041'),
        'power': Decimal('224.35')
    }


    print("Sending data:", data)

    try:

        table.put_item(Item=data)
        print("Data successfully inserted!")
    except Exception as e:
        print("Error inserting data:", e)


    time.sleep(5)
