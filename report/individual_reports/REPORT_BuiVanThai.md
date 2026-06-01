# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- **Student Name**: Bùi Văn Thái
- **Student ID**: 2A202600674
- **Date**: 2026-06-01

---

## I. Technical Contribution (15 Points)

Đóng góp chính tập trung vào việc xây dựng bản web app FastAPI và chuẩn hóa luồng chạy `python main.py` để hệ thống không còn là CLI demo đơn thuần.

- **Modules Implemented**: `main.py`, `src/app.py`, `src/templates/index.html`, `src/static/styles.css`
- **Code Highlights**: Thiết lập `GET /` cho giao diện, `POST /plan` cho API planning, và cấu hình để server luôn chạy tại `http://localhost:8000`
- **Documentation**: Phần giao diện web đóng vai trò lớp tương tác người dùng, gửi dữ liệu vào deterministic ReAct flow và render lại Thought, Action, Observation, Final Answer

---

## II. Debugging Case Study (10 Points)

- **Problem Description**: Hệ thống ban đầu chỉ in CLI output và không phù hợp yêu cầu web demo
- **Log Source**: Theo dõi từ console run `python main.py` và các lần gọi thử `/plan`
- **Diagnosis**: Kiến trúc cũ thiên về demo script, thiếu lớp API và UI nên mentor khó thử nhiều case thực tế
- **Solution**: Chuyển project sang FastAPI, dùng form submit JSON vào `/plan`, và giữ `main.py` chỉ làm entry point khởi động server

---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

1. **Reasoning**: `Thought` giúp tách rõ từng bước xử lý, đặc biệt hữu ích khi planner phải xét thời tiết rồi mới đến hoạt động và chi phí.
2. **Reliability**: Agent có thể kém hơn chatbot nếu tool schema nghèo dữ liệu hoặc ranking activity chưa khớp nhu cầu người dùng.
3. **Observation**: Observation là đầu vào rất quan trọng để agent cập nhật bước tiếp theo, ví dụ sau khi có thời tiết mưa thì phải xoay sang indoor activities.

---

## IV. Future Improvements (5 Points)

- **Scalability**: Tách knowledge base ra file JSON hoặc database riêng để mở rộng destination dễ hơn
- **Safety**: Bổ sung validation và schema checking chặt hơn cho request payload
- **Performance**: Cache weather mock và destination profile để giảm xử lý lặp lại

---

> [!NOTE]
> File này được tạo sẵn theo đúng định dạng báo cáo cá nhân cho project Travel Planning Agent web app.
