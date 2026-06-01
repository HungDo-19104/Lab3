# Group Report: Lab 3 - Production-Grade Agentic System

- **Team Name**: Travel Planning Agent Team
- **Team Members**: Bùi Văn Thái, Đỗ Văn Hùng, Lê Hoàng Nam, Lê Trần Quốc Bảo, Đặng Ngọc Bách
- **Deployment Date**: 2026-06-01

---

## 1. Executive Summary

Nhóm đã chuyển bài lab từ baseline chatbot/CLI demo thành một Travel Planning Agent web app chạy trên FastAPI tại localhost. Hệ thống hỗ trợ nhiều điểm du lịch nổi tiếng ở Việt Nam, dùng deterministic tool flow để sinh kế hoạch rõ ràng, có trace và cost breakdown.

- **Success Rate**: 100% trên bộ smoke test nội bộ đã thiết kế cho các destination chính
- **Key Outcome**: Agent hiện hỗ trợ knowledge base đa điểm đến, cost engine theo travel style, và giao diện web giúp mentor thử nhiều case thực tế hơn chatbot baseline

---

## 2. System Architecture & Tooling

### 2.1 ReAct Loop Implementation

Hệ thống áp dụng deterministic ReAct-style flow:

1. `get_weather(destination, date)`
2. `recommend_activities(destination, weather, preference, travel_style)`
3. `estimate_trip_cost(destination, days, activities, travel_style)`
4. `check_budget(total_cost, budget)`
5. Render `Final Answer`

### 2.2 Tool Definitions (Inventory)

| Tool Name | Input Format | Use Case |
| :--- | :--- | :--- |
| `get_weather` | `destination, date` | Trả về thời tiết mock theo ngày và mùa |
| `recommend_activities` | `destination, weather, preference, travel_style` | Chọn hoạt động đúng điểm đến, đúng sở thích, đúng ngân sách |
| `estimate_trip_cost` | `destination, days, activities, travel_style` | Tính cost engine V2 gồm hotel, food, transport, activities |
| `check_budget` | `total_cost, budget` | Kiểm tra chi phí có vượt ngân sách hay không |

### 2.3 LLM Providers Used

- **Primary**: Deterministic agent flow
- **Secondary (Backup)**: Không dùng LLM runtime trong bản demo cuối để đảm bảo tính ổn định

---

## 3. Telemetry & Performance Dashboard

Hệ thống có structured logging ở mức tool execution và agent lifecycle trên console/API flow.

- **Average Latency (P50)**: Thấp trong môi trường localhost vì không gọi external API
- **Max Latency (P99)**: Chủ yếu phụ thuộc thời gian render web và serialization JSON
- **Average Tokens per Task**: Không áp dụng cho deterministic final flow
- **Total Cost of Test Suite**: Gần như 0 ở runtime vì không dùng model trả phí

---

## 4. Root Cause Analysis (RCA) - Failure Traces

### Case Study: Legacy CLI / Encoding / Limited Data

- **Input**: Các case chạy cũ như Đà Lạt hoặc Đà Nẵng trong phiên bản CLI
- **Observation**: Output bị lẫn log `LLM_RESPONSE`, có lúc lỗi encoding trên PowerShell và knowledge base quá nhỏ
- **Root Cause**: Thiết kế ban đầu dành cho lab skeleton, chưa tối ưu cho web demo thực tế và chưa có destination database đủ sâu
- **Fix**: Loại bỏ legacy agent, chuyển sang FastAPI web app, mở rộng travel knowledge base theo vùng miền, và thêm cost engine V2

---

## 5. Ablation Studies & Experiments

### Experiment 1: Small Knowledge Base vs Expanded Knowledge Base

- **Diff**: Từ 3-4 destination lên bộ data cho nhiều điểm du lịch nổi bật ở Bắc, Trung, Nam
- **Result**: Demo trở nên thực tế hơn, mentor có thể thử nhiều trường hợp mà không lặp activity giữa các thành phố

### Experiment 2: Simple Cost Engine vs Cost Engine V2

| Case | Cost Engine cũ | Cost Engine V2 | Winner |
| :--- | :--- | :--- | :--- |
| Đà Lạt | Giá trị gần đúng, ít phân rã | Có hotel, food, transport, activities | **V2** |
| Phú Quốc | Không phản ánh đặc thù island travel | Có transport và hotel premium đúng hơn | **V2** |

---

## 6. Production Readiness Review

- **Security**: Đã có validation cơ bản cho payload và fallback khi destination chưa tồn tại
- **Guardrails**: Tool order là deterministic nên không bị loop vô hạn
- **Scaling**: Bước tiếp theo nên tách knowledge base ra JSON/DB, thêm caching, và có thể kết hợp optional LLM summarizer cho natural language tốt hơn

---

> [!NOTE]
> File này được tạo sẵn như bản group report cho project Travel Planning Agent web app.
