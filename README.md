# 🧠 MLN Chatbot — Chatbot Hỗ Trợ Học Triết Học Mác - Lênin  

## 🌐 Link Public App
🔗 **[Truy cập Chatbot trên Streamlit](https://mlnchatbot.streamlit.app/)**  
⚙️ **[Xem mã nguồn trên GitHub](https://github.com/biaunu/MLNChatbot)**  

---

## 📘 Giới thiệu

**MLN Chatbot** là chatbot học tập được phát triển nhằm hỗ trợ sinh viên môn **Triết học Mác - Lênin**.  
Chatbot cho phép người dùng **chọn các mục theo từng chương** (như trong giáo trình gốc) để hệ thống **chỉ trả lời dựa trên nội dung OCR từ giáo trình gốc**, đảm bảo **độ chính xác cao** và **hạn chế việc suy luận lan man** từ Internet.

Ứng dụng được xây dựng bằng **Streamlit** và sử dụng **DeepSeek API** làm nền tảng AI.  

---

## 🧩 Tính năng chính

- ✅ Chọn mục (I, II, III, ...) trong từng **chương của giáo trình Triết học Mác - Lênin**.  
- ✅ Chatbot chỉ trả lời **theo nội dung đúng trang giáo trình OCR** tương ứng với mục đã chọn.  
- ✅ Giao diện thân thiện, dễ dùng trên web (Streamlit).  
- ✅ Giúp sinh viên ôn tập, tra cứu khái niệm, lý luận, ví dụ một cách chính xác và nhanh chóng.

---

## ⚠️ Lưu ý khi sử dụng

1. 🔹 **Không nên chọn nhiều mục thuộc các chương khác nhau cùng lúc.**  
   → Mỗi lần chỉ nên chọn **tất cả các mục trong 1 chương** để chatbot hoạt động hiệu quả.  

2. 🔹 **Không nên chọn quá nhiều mục một lúc** (vì giáo trình gần 500 trang, input quá dài).  

3. 🔹 **Khi chatbot đang trả lời**, không nên:
   - Thay đổi lựa chọn mục.
   - Nhập và gửi thêm câu hỏi khác.  
   → Việc này có thể khiến chatbot **tự ngắt trả lời trước đó** (do chưa có chức năng khóa phiên trả lời).  

4. 🔹 Nếu link Streamlit bị lỗi hoặc app không chạy được, có thể do:
   - Streamlit tự tắt ứng dụng sau một thời gian không hoạt động.  
   - API Key của DeepSeek **hết quota hoặc hết hạn**.  

---

## 🛠️ Hướng dẫn chạy trên máy cá nhân

Nếu link public không hoạt động, bạn có thể **chạy chatbot trên máy của mình** theo hướng dẫn sau:

### 1️⃣ Clone project
```bash
git clone https://github.com/biaunu/MLNChatbot.git
cd MLNChatbot
```

### 2️⃣ Cài đặt thư viện cần thiết
```bash
pip install -r requirements.txt
```

### 3️⃣ Đăng ký và lấy API key của DeepSeek
- Truy cập [https://platform.deepseek.com/](https://platform.deepseek.com/)  
- Tạo tài khoản, sau đó vào phần **API Keys** để tạo key mới.  
- Sao chép key và lưu lại.

### 4️⃣ Tạo file `.env`
Trong thư mục gốc của project, tạo file `.env`:
```
DEEPSEEK_API_KEY=your_api_key_here
```

### 5️⃣ Chạy ứng dụng
```bash
streamlit run app.py
```

Sau đó mở trình duyệt tại địa chỉ:  
👉 **http://localhost:8501**

---

## 📂 Cấu trúc thư mục (gợi ý sắp xếp GitHub)

```
MLNChatbot/
│
├── app.py                        # Mã nguồn chính của ứng dụng Streamlit
├── requirements.txt              # Danh sách thư viện cần cài
├── data/
│   ├── ocr_pages/                # Các file văn bản OCR theo từng trang giáo trình
│   └── metadata.json             # Thông tin chương - mục - trang
│
├── documents/
│   ├── MLN_Textbook.pdf          # Giáo trình bản đẹp (PDF)
│   └── MLNChatbot_Proposal.pdf   # Slide proposal nhóm 9
│
├── .env.example                  # Nơi để API Key
└── README.md                     # Tài liệu mô tả dự án
```

---

## 👥 Thông tin nhóm

***Trường Đại học FPT - Phân hiệu tại TP.HCM***
- **Môn:** Triết học Mác-Lênin (MLN111)
- **Nhóm:** 09  
- **Lớp:** Half1_SE1714_MLN111  
- **Học kỳ:** Fall 2025  

---

## 💬 Liên hệ

Vui lòng liên hệ qua phần *Issues* trên GitHub repo
