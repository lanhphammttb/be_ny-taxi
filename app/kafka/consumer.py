from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'ride_topic',
    bootstrap_servers='kafka:9092',
    group_id='ride-consumer-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    data = message.value
    print("Received from Kafka:", data)
