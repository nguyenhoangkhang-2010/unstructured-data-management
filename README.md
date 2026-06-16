# Hệ Thống Quản Lý Hồ Sơ Ứng Viên & Khai Phá Dữ Liệu

## 1. Yêu cầu & Cài đặt
Hệ thống yêu cầu **Python 3.12** và **MongoDB**.

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