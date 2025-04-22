from flask import Flask, render_template, jsonify
import boto3
from decimal import Decimal
from datetime import datetime
import random

app = Flask(__name__)

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('MachineHealthData')

@app.route('/')
def index():
    # Query DynamoDB for the most recent data
    response = table.scan()  # Or use a more efficient query if needed
    items = response.get('Items', [])

    # Convert Decimal back to float for display
    for item in items:
        item['temperature'] = float(item['temperature'])
        item['vibration'] = float(item['vibration'])
        item['power'] = float(item['power'])

    return render_template('index.html', items=items)

@app.route('/api/data')
def get_data():
    # Query DynamoDB for data
    response = table.scan()  # Scan or query based on the actual need
    items = response.get('Items', [])

    # Convert Decimal to float for JSON serialization
    for item in items:
        item['temperature'] = float(item['temperature'])
        item['vibration'] = float(item['vibration'])
        item['power'] = float(item['power'])

    return jsonify(items)  # Return the data as JSON for the frontend to use

@app.route('/insert_random_data', methods=['GET'])
def insert_random_data():
    # Generate random data for testing
    machine_id = f"M{random.randint(1, 5)}"
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    temperature = round(random.uniform(70, 100), 2)  # Random temperature between 70 and 100
    vibration = round(random.uniform(0.01, 0.1), 4)  # Random vibration between 0.01 and 0.1
    power = round(random.uniform(200, 400), 2)  # Random power between 200 and 400

    # Check if the data is critical
    is_critical = False
    if temperature > 90 or vibration > 0.05:
        is_critical = True

    # Data to insert
    item = {
        'machine_id': machine_id,
        'timestamp': timestamp,
        'temperature': Decimal(str(temperature)),
        'vibration': Decimal(str(vibration)),
        'power': Decimal(str(power)),
        'is_critical': is_critical  # Add the 'is_critical' field
    }

    # Insert the data into DynamoDB table
    table.put_item(Item=item)

    # Return a success response
    return jsonify({'status': 'success', 'message': 'Random data inserted successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)
