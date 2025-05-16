from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from kafka import KafkaProducer
import json
import uuid
from app.api import users

# Thiết lập Kafka producer
producer = KafkaProducer(
    bootstrap_servers='192.168.168.249:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Mã hóa dữ liệu thành JSON
)

app = FastAPI(title='Ride Ordering Service')

# Mô hình dữ liệu của chuyến đi
class Ride(BaseModel):
    user_id: str  # Thay đổi từ int thành str nếu bạn muốn nhận user_id dưới dạng chuỗi
    pickup: str
    dropoff: str
    distance: float
    price_per_km: float

@app.post('/rides/', summary='Submit a ride request')
def submit_ride(ride: Ride):
    # Chuyển dữ liệu đầu vào thành dictionary
    data = ride.dict()
    data['ride_id'] = str(uuid.uuid4())  # Tạo UUID cho ride_id
    data['total_price'] = data['distance'] * data['price_per_km']  # Tính giá trị tổng tiền

    # Gửi dữ liệu vào Kafka
    producer.send('ride_topic', value=data)

    # Đảm bảo gửi thành công và trả về kết quả
    producer.flush()

    return {'ride_id': data['ride_id'], 'status': 'submitted'}


app.include_router(users.router, prefix="/users", tags=["users"])