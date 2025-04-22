from flask import Flask, render_template, jsonify
import boto3
from decimal import Decimal
from datetime import datetime
import random

app = Flask(__name__)


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('MachineHealthData')

@app.route('/')
def index():

    response = table.scan()
    items = response.get('Items', [])


    for item in items:
        item['temperature'] = float(item['temperature'])
        item['vibration'] = float(item['vibration'])
        item['power'] = float(item['power'])

    return render_template('index.html', items=items)

@app.route('/api/data')
def get_data():

    response = table.scan()
    items = response.get('Items', [])


    for item in items:
        item['temperature'] = float(item['temperature'])
        item['vibration'] = float(item['vibration'])
        item['power'] = float(item['power'])

    return jsonify(items)

@app.route('/insert_random_data', methods=['GET'])
def insert_random_data():

    machine_id = f"M{random.randint(1, 5)}"
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    temperature = round(random.uniform(70, 100), 2)
    vibration = round(random.uniform(0.01, 0.1), 4)
    power = round(random.uniform(200, 400), 2)


    is_critical = False
    if temperature > 90 or vibration > 0.05:
        is_critical = True


    item = {
        'machine_id': machine_id,
        'timestamp': timestamp,
        'temperature': Decimal(str(temperature)),
        'vibration': Decimal(str(vibration)),
        'power': Decimal(str(power)),
        'is_critical': is_critical
    }


    table.put_item(Item=item)


    return jsonify({'status': 'success', 'message': 'Random data inserted successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)
