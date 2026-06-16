# Hệ Thống Quản Lý Hồ Sơ Ứng Viên & Khai Phá Dữ Liệu

Đây là hệ thống quản lý tuyển dụng thông minh được xây dựng bằng **Flask (Python)** và **MongoDB**. Dự án tích hợp các công nghệ trích xuất thông tin tự động, phân tích mạng xã hội, và các thuật toán khai phá dữ liệu để phân cụm ứng viên cũng như gợi ý việc làm.

## Tính Năng Chính

- **Quản lý Hồ sơ Ứng viên (CRUD):** Thêm, sửa, xóa, và xem chi tiết hồ sơ ứng viên (hỗ trợ upload CV PDF, hình ảnh, video, audio).
- **Auto-fill CV (PyPDF2):** Tự động đọc và trích xuất Email, Số điện thoại và mô tả từ file CV PDF ngay trên giao diện upload.
- **Social Analysis (GitHub API):** Tự động lấy thông tin cá nhân và trích xuất kỹ năng (ngôn ngữ lập trình) dựa vào link GitHub của ứng viên.
- **Hệ thống Gợi ý (Job Recommendation):** Đánh giá mức độ phù hợp giữa Ứng viên và Tin tuyển dụng thông qua việc kết hợp dữ liệu đa phương thức (Multi-modal fusion: kỹ năng, mô tả, OCR Text, Transcript).
- **Khai phá Dữ liệu (K-Means Clustering):** Tiền xử lý văn bản tiếng Việt/Anh (Underthesea, regex), trích xuất đặc trưng văn bản và sử dụng thuật toán K-Means để phân cụm ứng viên thành 5 nhóm vai trò (Roles) tự động.
- **Báo cáo & Trực quan hóa:** Xuất kết quả phân tích ra file `.csv`, báo cáo `.txt` và xuất biểu đồ phân bố phân cụm `.png`.
- **Mock Data Generator:** Hỗ trợ tạo tự động lượng lớn dữ liệu (300 ứng viên, 30 tin tuyển dụng, và 1000 đơn ứng tuyển) bằng thư viện `Faker`.

## 🛠 Yêu Cầu Hệ Thống
- **Python:** 3.12 trở lên.
- **Cơ sở dữ liệu:** MongoDB Community Server (hoạt động mặc định ở `mongodb://localhost:27017/`).

## Hướng Dẫn Cài Đặt

**1. Cài đặt các thư viện cần thiết**
```bash
pip install -r requirements.txt
```

## 2. Hướng dẫn cài đặt MongoDB
1. Tải MongoDB Community Server.
2. Cài đặt và khởi chạy MongoDB service (mặc định tại `mongodb://localhost:27017/`).
3. Khuyến nghị cài thêm MongoDB Compass để quản lý CSDL trực quan.

## 3. Khởi tạo dữ liệu mẫu
Để tạo tự động 300 ứng viên, 30 tin tuyển dụng và 1000 đơn ứng tuyển:
```bash
python data/generate_mock_data.py
```

## 4. Chạy ứng dụng Flask
Tại thư mục gốc `data-mining-project`, chạy lệnh:
```bash
python run.py
```
Truy cập `http://localhost:5000` để sử dụng hệ thống.

## 5. Luồng Data Mining (K-Means)
MongoDB -> Lấy CV -> Tiền xử lý văn bản -> TF-IDF -> K-Means (5 roles) -> Đánh giá & Trực quan hóa.