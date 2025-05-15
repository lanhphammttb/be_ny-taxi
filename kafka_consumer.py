import psycopg2
import json
import uuid
from kafka import KafkaConsumer

# Thiết lập kết nối đến PostgreSQL
conn = psycopg2.connect(
    dbname="ny_taxi", 
    user="postgres",
    password="Khongbiet098",
    host="localhost", 
    port="5432"
)
cursor = conn.cursor()

# Thiết lập Kafka consumer
consumer = KafkaConsumer(
    'ride_topic', 
    bootstrap_servers='192.168.168.249:9092', 
    group_id='ride-consumer-group', 
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Lắng nghe các message từ Kafka và lưu vào PostgreSQL
for message in consumer:
    ride_data = message.value
    print("Received ride data:", ride_data)  # In ra dữ liệu nhận được từ Kafka

    try:
        user_id = uuid.UUID(ride_data['user_id'])  # Chuyển user_id thành UUID
        ride_id = uuid.UUID(ride_data['ride_id'])  # Chuyển ride_id thành UUID
    except ValueError:
        print(f"Invalid UUID format for user_id or ride_id: {ride_data['user_id']} or {ride_data['ride_id']}")
        continue  # Bỏ qua message này nếu UUID không hợp lệ

    pickup = ride_data['pickup']
    dropoff = ride_data['dropoff']
    distance = ride_data['distance']
    total_price = ride_data['total_price']

    # In ra các giá trị để kiểm tra
    print(f"ride_id: {str(ride_id)}, user_id: {str(user_id)}")

    # Kiểm tra xem user_id đã tồn tại trong bảng users chưa
    cursor.execute("SELECT COUNT(*) FROM users WHERE user_id = %s", (str(user_id),))
    user_exists = cursor.fetchone()[0] > 0

    if not user_exists:
        print(f"User ID {user_id} không tồn tại trong bảng users. Không thể chèn dữ liệu vào bảng rides.")
        continue  # Bỏ qua nếu user_id không tồn tại
    else:
        # Chèn dữ liệu vào bảng rides nếu user_id hợp lệ
        cursor.execute("""
            INSERT INTO rides (ride_id, customer_id, pickup_location, dropoff_location, distance, total_price, ride_status)
            VALUES (%s, %s, %s, %s, %s, %s, 'pending')
        """, (str(ride_id), str(user_id), pickup, dropoff, distance, total_price))
        conn.commit()  # Lưu thay đổi vào cơ sở dữ liệu
        print(f"Ride {ride_id} đã được lưu vào cơ sở dữ liệu")

# Đóng kết nối sau khi hoàn tất
cursor.close()
conn.close()
