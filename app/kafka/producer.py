from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda m: json.dumps(m).encode('utf-8')
)

def send_to_kafka(topic: str, data: dict):
    producer.send(topic, value=data)
    producer.flush()
