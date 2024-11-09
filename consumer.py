import json
import pika
import os
from pymongo import MongoClient
from datetime import datetime

# Read environment variables
rabbitmq_host = os.environ.get('RABBITMQ_HOST', 'localhost')
rabbitmq_port = os.environ.get('RABBITMQ_PORT', 5672)
mongodb_host = os.environ.get('MONGODB_HOST', 'localhost')
mongodb_port = os.environ.get('MONGODB_PORT', 27017)

# MongoDB setup
client = MongoClient(mongodb_host, mongodb_port)
db = client.feedapp
polls_collection = db.polls

# RabbitMQ setup
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=rabbitmq_host,
    port=rabbitmq_port
))
channel = connection.channel()
channel.queue_declare(queue='poll_updates')

def callback(ch, method, properties, body):
    data = json.loads(body)
    data['last_updated'] = datetime.utcnow()
    polls_collection.update_one(
        {'poll_id': data['poll_id']},
        {'$set': data},
        upsert=True
    )
    print(f"Poll {data['poll_id']} updated in MongoDB.")

channel.basic_consume(queue='poll_updates', on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
