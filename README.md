# Travel Planning Agent Web App

Project này là một web app FastAPI cho Travel Planning Agent chạy trên localhost.

## Cách chạy

```bash
pip install -r requirements.txt
python main.py
```

Sau khi chạy:

```text
Server started successfully
Running at:
http://localhost:8000
```

## Input hỗ trợ

- `destination`
- `date`
- `preference`
- `days`
- `budget`
- `travel_style`: `budget`, `standard`, `premium`

## Agent flow

Agent luôn gọi đúng 4 tools theo thứ tự:

1. `get_weather(destination, date)`
2. `recommend_activities(destination, weather, preference, travel_style)`
3. `estimate_trip_cost(destination, days, activities, travel_style)`
4. `check_budget(total_cost, budget)`

## Travel Knowledge Base

Knowledge base hiện có các điểm đến:

### Miền Bắc

- Hà Nội
- Sapa
- Hà Giang
- Ninh Bình
- Quảng Ninh (Hạ Long)
- Mộc Châu

### Miền Trung

- Huế
- Đà Nẵng
- Hội An
- Quy Nhơn
- Nha Trang
- Phú Yên

### Miền Nam

- TP Hồ Chí Minh
- Vũng Tàu
- Phú Quốc
- Cần Thơ
- Đà Lạt

Mỗi destination có đủ:

- `nature`
- `food`
- `culture`
- `indoor_rainy`

Nếu destination chưa tồn tại, hệ thống dùng fallback riêng và không lấy dữ liệu từ thành phố khác.

## Cost Engine V2

Tổng chi phí được tính theo:

```text
total_cost = hotel_cost + food_cost + transport_cost + activity_cost
```

### Hotel cost

Theo destination và `travel_style`.

### Food cost

- `budget`: `150000/ngày`
- `standard`: `300000/ngày`
- `premium`: `700000/ngày`

### Transport cost

Theo từng destination trong knowledge base.

### Activity cost

Mỗi activity có `cost` riêng ngay trong database.

## API

### `GET /`

Trang giao diện web.

### `POST /plan`

Request body:

```json
{
  "destination": "Phú Quốc",
  "date": "2026-08-20",
  "preference": "biển và ăn uống",
  "days": 4,
  "budget": 12000000,
  "travel_style": "standard"
}
```

Response body:

```json
{
  "thoughts": ["..."],
  "actions": ["..."],
  "observations": [{}, [], {}, {}],
  "final_answer": "...",
  "total_cost": 0,
  "within_budget": true,
  "cost_breakdown": {
    "hotel": 0,
    "food": 0,
    "transport": 0,
    "activities": 0
  },
  "travel_advice": "..."
}
```

## Test coverage

Đã có test cho:

- Hà Nội
- Sapa
- Đà Lạt
- Đà Nẵng
- Phú Quốc
- Quảng Ninh (Hạ Long)

Ngoài ra còn có test fallback destination riêng.
