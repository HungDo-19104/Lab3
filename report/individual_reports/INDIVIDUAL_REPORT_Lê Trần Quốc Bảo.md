# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- **Student Name**: Lê Trần Quốc Bảo
- **Student ID**: [Fill Your ID Here]
- **Date**: 2026-06-01

---

## I. Technical Contribution (15 Points)

Đóng góp chính là hoàn thiện deterministic agent flow và đảm bảo thứ tự tool call luôn đúng trong web app.

- **Modules Implemented**: `src/agent/travel_agent.py`
- **Code Highlights**: Agent luôn chạy theo chuỗi `get_weather -> recommend_activities -> estimate_trip_cost -> check_budget`, lưu trace `thoughts/actions/observations`, và sinh `travel_advice`
- **Documentation**: Deterministic flow giúp demo ổn định, dễ kiểm thử, tránh tình trạng LLM loop sinh lỗi không lặp lại được

---

## II. Debugging Case Study (10 Points)

- **Problem Description**: Legacy flow cũ có thể gây nhầm với `LLM_RESPONSE` logs và output bị cắt ở CLI
- **Log Source**: So sánh legacy traces với deterministic web API traces
- **Diagnosis**: Khi không cần LLM thật, việc giữ loop cũ chỉ làm tăng nhiễu và khó review
- **Solution**: Dọn legacy agent, chỉ giữ deterministic flow trong `travel_agent.py`, đồng thời chuẩn hóa response JSON để frontend render đầy đủ

---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

1. **Reasoning**: ReAct flow tách bước rõ ràng nên mentor có thể kiểm tra tool order dễ hơn chatbot.
2. **Reliability**: Agent có thể trở nên cứng nếu heuristic recommendation chưa đủ thông minh cho preference phức tạp.
3. **Observation**: Mỗi observation đóng vai trò như một checkpoint, giúp hệ thống dễ debug và test hơn.

---

## IV. Future Improvements (5 Points)

- **Scalability**: Kết hợp deterministic planner với optional LLM summarizer
- **Safety**: Ghi audit trail riêng cho từng request ID
- **Performance**: Tối ưu serialization khi observation list lớn hơn

---

> [!NOTE]
> File này được tạo sẵn theo đúng định dạng báo cáo cá nhân cho project Travel Planning Agent web app.
