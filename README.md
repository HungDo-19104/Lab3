# Travel Chatbot vs Travel Agent Demo

Project này là web app FastAPI dùng để demo sự khác biệt giữa:

- Travel Chatbot
- Travel ReAct Agent

## Chạy project

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

Mở trình duyệt tại [http://localhost:8000](http://localhost:8000).

## Form input

Người dùng nhập:

- `destination`
- `date`
- `preference`
- `days`
- `budget`
- `travel_style`

Sau đó bấm:

`Compare Chatbot vs Agent`

## Kết quả hiển thị trên localhost

Trang web sẽ hiện:

1. **Comparison Table**
2. **Chatbot Output**
3. **Agent Output**
4. **Agent ReAct Trace**

## Chatbot vs Agent

### Chatbot

- Không gọi tool
- Trả lời trực tiếp từ prompt
- Không có trace Thought / Action / Observation

### Agent

Agent bắt buộc gọi đúng 4 tool:

1. `get_weather()`
2. `recommend_activities()`
3. `estimate_trip_cost()`
4. `check_budget()`

## API

### `POST /compare`

Đây là endpoint chính cho demo.

Request body:

```json
{
  "destination": "Đà Lạt",
  "date": "2026-06-15",
  "preference": "thiên nhiên",
  "days": 4,
  "budget": 2000000,
  "travel_style": "budget"
}
```

Response body:

```json
{
  "chatbot": {
    "final_answer": "...",
    "uses_tools": false,
    "method": "Direct LLM response"
  },
  "agent": {
    "trace": [
      {
        "thought": "...",
        "action": "get_weather",
        "observation": {}
      }
    ],
    "final_answer": "...",
    "uses_tools": true,
    "total_cost": 0,
    "within_budget": true
  },
  "comparison": [
    {
      "criteria": "Có dùng tool không",
      "chatbot": "Không",
      "agent": "Có"
    }
  ]
}
```

### `POST /plan`

Endpoint phụ, vẫn giữ để lấy riêng output của Agent.

## Demo case gợi ý

```json
{
  "destination": "Đà Lạt",
  "date": "2026-06-15",
  "preference": "thiên nhiên",
  "days": 4,
  "budget": 2000000,
  "travel_style": "budget"
}
```

Kỳ vọng:

- Chatbot trả lời chung chung hơn
- Agent có weather, activities, cost breakdown, budget check và ReAct trace

## Final check

1. Chạy `python main.py`
2. Mở `http://localhost:8000`
3. Submit form
4. Xem bảng so sánh Chatbot vs Agent
5. Xem Agent ReAct Trace hiển thị đủ 4 bước
