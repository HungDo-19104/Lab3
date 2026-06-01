# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- **Student Name**: Đặng Ngọc Bách
- **Student ID**: 2A202600661
- **Date**: 2026-06-01

---

## I. Technical Contribution (15 Points)

Đóng góp chính là phần kiểm thử, hoàn thiện README và xác nhận web app chạy được trên localhost với nhiều case demo.

- **Modules Implemented**: `tests/test_travel_agent.py`, `README.md`
- **Code Highlights**: Test cho Hà Nội, Sapa, Đà Lạt, Đà Nẵng, Phú Quốc, Quảng Ninh (Hạ Long), và fallback destination
- **Documentation**: README mô tả rõ input, API, cách chạy `python main.py`, cùng cấu trúc cost engine và knowledge base

---

## II. Debugging Case Study (10 Points)

- **Problem Description**: Dữ liệu tiếng Việt và output terminal từng có lúc hiển thị lỗi encoding hoặc bị cắt dòng
- **Log Source**: Kiểm tra output server và response từ `POST /plan`
- **Diagnosis**: Sự khác biệt giữa console Windows và dữ liệu JSON dễ gây hiểu nhầm rằng API bị lỗi
- **Solution**: Dựa vào test và API verification để xác nhận dữ liệu đầy đủ, đồng thời ưu tiên kiểm tra trên browser localhost

---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

1. **Reasoning**: ReAct dễ benchmark hơn chatbot vì có thể assert từng bước.
2. **Reliability**: Chatbot có thể trôi chảy hơn về ngôn ngữ, nhưng agent đáng tin hơn khi cần tính chi phí và kiểm ngân sách.
3. **Observation**: Observation là nền tảng để viết test tự động và kiểm tra regression.

---

## IV. Future Improvements (5 Points)

- **Scalability**: Thêm snapshot test cho response JSON và UI
- **Safety**: Bổ sung validation kỹ hơn cho destination/date/travel_style
- **Performance**: Tạo smoke test tự động cho `GET /` và `POST /plan` sau mỗi thay đổi lớn

---

> [!NOTE]
> File này được tạo sẵn theo đúng định dạng báo cáo cá nhân cho project Travel Planning Agent web app.
