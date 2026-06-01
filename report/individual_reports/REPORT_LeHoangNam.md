# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- **Student Name**: Lê Hoàng Nam
- **Student ID**: 2A202600965
- **Date**: 2026-06-01

---

## I. Technical Contribution (15 Points)

Đóng góp chính là nâng cấp Cost Engine V2 và luồng tính toán theo `travel_style`.

- **Modules Implemented**: `src/tools/travel_tools.py`, `src/agent/travel_agent.py`
- **Code Highlights**: Công thức mới `hotel + food + transport + activities`, hotel cost theo destination, food cost theo style, transport theo destination, activity cost theo dữ liệu thật
- **Documentation**: Agent gọi `estimate_trip_cost()` sau khi đã có activity list, vì chi phí activity phụ thuộc trực tiếp vào recommendation step

---

## II. Debugging Case Study (10 Points)

- **Problem Description**: Phiên bản cũ tính chi phí quá đơn giản nên không phản ánh tốt khác biệt giữa Phú Quốc, Hà Giang, Đà Lạt
- **Log Source**: So sánh output `total_cost` giữa các case API `/plan`
- **Diagnosis**: Hệ thống cũ chỉ dùng vài biến cost chung, không có profile budget/standard/premium
- **Solution**: Thiết kế cost engine theo profile người dùng và dữ liệu từng destination, sau đó expose `cost_breakdown` cho UI/API

---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

1. **Reasoning**: Bước estimate cost giúp agent tránh trả lời cảm tính về ngân sách.
2. **Reliability**: Nếu cost engine không minh bạch, final answer rất dễ nghe hợp lý nhưng sai thực tế.
3. **Observation**: Breakdown chi tiết từ tool cost giúp agent tạo travel advice rõ ràng hơn nhiều so với chatbot.

---

## IV. Future Improvements (5 Points)

- **Scalability**: Thêm seasonal pricing theo cao điểm/thấp điểm
- **Safety**: Áp dụng guardrail để không cho style không hợp lệ đi sâu vào pipeline
- **Performance**: Precompute average cost bundles cho các route phổ biến

---

> [!NOTE]
> File này được tạo sẵn theo đúng định dạng báo cáo cá nhân cho project Travel Planning Agent web app.
