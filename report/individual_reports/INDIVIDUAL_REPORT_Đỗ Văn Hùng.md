# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- **Student Name**: Đỗ Văn Hùng
- **Student ID**: 2A202600759
- **Date**: 2026-06-01

---

## I. Technical Contribution (15 Points)

Đóng góp chính nằm ở phần Travel Knowledge Base và chuẩn hóa dữ liệu theo từng điểm đến cụ thể tại Việt Nam.

- **Modules Implemented**: `src/tools/travel_tools.py`
- **Code Highlights**: Mỗi destination có `nature`, `food`, `culture`, `indoor_rainy`, chi phí khách sạn theo style, phí di chuyển riêng và cost cho từng activity
- **Documentation**: Tool layer là nguồn dữ liệu lõi để agent suy luận có căn cứ thay vì dùng một danh sách hoạt động chung

---

## II. Debugging Case Study (10 Points)

- **Problem Description**: Bản đầu chỉ hỗ trợ vài thành phố, dữ liệu ít nên demo thiếu thực tế
- **Log Source**: Quan sát kết quả `/plan` với các case ngoài Đà Nẵng, Đà Lạt, Huế
- **Diagnosis**: Knowledge base nhỏ khiến recommendation lặp, thiếu diversity và khó test nhiều tình huống
- **Solution**: Mở rộng dữ liệu theo miền Bắc, Trung, Nam; đồng thời thêm fallback destination riêng để không dùng nhầm dữ liệu thành phố khác

---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

1. **Reasoning**: ReAct hiệu quả hơn khi mỗi bước dùng dữ liệu có cấu trúc tốt, nhất là destination-specific activities.
2. **Reliability**: Nếu dữ liệu tool không đủ chi tiết, agent dù có loop tốt vẫn dễ cho ra kế hoạch nghèo nàn.
3. **Observation**: Observation từ `recommend_activities()` quyết định trực tiếp chất lượng của phần cost estimation và final advice.

---

## IV. Future Improvements (5 Points)

- **Scalability**: Chuyển knowledge base sang JSON/YAML hoặc SQLite
- **Safety**: Thêm versioning cho dữ liệu travel để tránh sai lệch khi nhiều người cùng sửa
- **Performance**: Tạo index theo region/preference để truy vấn recommendation nhanh hơn

---

> [!NOTE]
> File này được tạo sẵn theo đúng định dạng báo cáo cá nhân cho project Travel Planning Agent web app.
