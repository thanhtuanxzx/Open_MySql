# Open MySQL

Portable MySQL Server Manager với giao diện hiện đại, dễ sử dụng.

**Made by [thanhtuanxzx](https://github.com/thanhtuanxzx)**

![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)
![Open Source](https://img.shields.io/badge/open--source-yes-green)
![Non Commercial](https://img.shields.io/badge/non--commercial-yes-orange)

> **⚠️ Lưu ý pháp lý:** Dự án này là mã nguồn mở, miễn phí, dùng cho mục đích giáo dục và cá nhân. Bao gồm MySQL Server (GPLv2 - Oracle), phpMyAdmin (GPLv2), và PHP (PHP License). Xem [LICENSE](LICENSE) để biết thêm chi tiết.

---

## 🚀 Tính năng

- ✅ Giao diện hiện đại với ttkbootstrap
- ✅ Theme sáng/tối (toggle ở góc phải)
- ✅ Quản lý MySQL Server, PHP Web Server, phpMyAdmin
- ✅ Status cards real-time
- ✅ Log panel với scroll
- ✅ Cấu hình ports linh hoạt
- ✅ **100% Portable** - Copy và chạy, không cần cài đặt
- ✅ **Mã nguồn mở** - MIT License, miễn phí cho mục đích giáo dục

---

## 📋 Yêu cầu

### Để chạy trực tiếp từ source code:
- Python 3.8 trở lên
- `ttkbootstrap` (tự động cài qua `requirements.txt`)

### Để chạy từ .exe (khuyến nghị):
- Windows 10/11
- **KHÔNG CẦN** cài Python hay bất kỳ thứ gì khác!

---

## 🎯 Hướng dẫn cho người dùng lần đầu

### Cách 1: Chạy từ .exe (Dễ nhất) ⭐

1. **Tải và giải nén** thư mục `final` (từ release hoặc `package_final.bat`)

2. **Mở thư mục `final`**, bạn sẽ thấy:
   ```
   final/
   ├── MySQL_Manager.exe      ← Chạy file này!
   ├── MySQL Server 9.5/       ← MySQL Server
   ├── phpMyAdmin-5.2.3-all-languages/  ← phpMyAdmin
   ├── php/                     ← PHP Portable
   ├── data/                    ← Database (tự tạo)
   └── config/                  ← Configuration
   ```

3. **Double-click** `MySQL_Manager.exe`

4. **Tab "Chức năng chính"** sẽ mở sẵn, bạn sẽ thấy:
   - Nút **"Khởi động phpMyAdmin"** → Click để start MySQL + PHP + mở browser
   - Nút **"Khởi động MySQL Server"** → Chỉ start MySQL
   - Nút **"Dừng tất cả"** → Stop tất cả services

5. **Lần đầu sử dụng**:
   - Click nút **"⚙️ Thiết lập ban đầu"** ở góc phải trên
   - Hoặc vào tab **"Thiết lập"** → Click **"Bắt đầu thiết lập"**
   - App sẽ tự động cấu hình:
     - Tạo `my.ini` cho MySQL
     - Tạo `config.inc.php` cho phpMyAdmin
     - Thiết lập ports và paths

6. **Sau khi setup xong**:
   - Click **"Khởi động phpMyAdmin"**
   - Browser tự động mở: `http://localhost:8080`
   - Đăng nhập:
     - **Username:** `root`
     - **Password:** *(để trống)*

### Cách 2: Chạy từ source code

1. **Clone hoặc download** dự án:
   ```bash
   git clone https://github.com/thanhtuanxzx/open-mysql.git
   cd open-mysql
   ```

2. **Cài đặt dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Chạy ứng dụng**:
   ```bash
   python app.py
   ```

4. **Setup lần đầu** (giống Cách 1, bước 5)

---

## 📖 Các tab trong ứng dụng

### 1. **Chức năng chính** (Tab mặc định)
- 🟢 **Khởi động phpMyAdmin** - Start MySQL + PHP + mở browser
- 🔵 **Khởi động MySQL Server** - Chỉ start MySQL
- 🔴 **Dừng tất cả** - Stop tất cả services
- 📋 **Log panel** - Xem logs real-time

### 2. **Trạng thái**
- Status cards cho MySQL Server, PHP Web Server, PHP Portable
- Xem trạng thái real-time: **Đang chạy** / **Không chạy**
- Start/Stop từng service riêng lẻ

### 3. **Thiết lập**
- ⚙️ **Bắt đầu thiết lập** - Auto-config (dùng lần đầu)
- 🔧 **Sửa lỗi đăng nhập** - Fix login issues
- 🔌 **Cấu hình ports**:
  - MySQL Port (mặc định: 3306)
  - HTTP Port (mặc định: 8080)
- 📁 **Thư mục data** - Chọn nơi lưu database

### 4. **Log & Trạng thái**
- Log chi tiết với scroll
- Nút **"Làm mới trạng thái"** để cập nhật

---

## 🔧 Cấu hình

### File cấu hình: `config/config.json`

```json
{
  "theme": "light",
  "mysql": {
    "port": 3306,
    "data_dir": "data"
  },
  "php": {
    "http_port": 8080,
    "path": "php"
  },
  "phpmyadmin": {
    "path": "phpMyAdmin-5.2.3-all-languages"
  }
}
```

### Thay đổi theme:
- Click nút **🌓** ở góc phải trên để toggle sáng/tối

---

## 🛠️ Build từ source code

### Build .exe:

```bash
build_exe.bat
```

File `.exe` sẽ được tạo tại: `dist\MySQL_Manager.exe`

### Tạo thư mục final portable:

```bash
package_final.bat
```

Thư mục `final\` sẽ chứa:
- `MySQL_Manager.exe`
- MySQL Server 9.5
- phpMyAdmin
- PHP Portable
- Config files

**Copy thư mục `final\` sang máy khác là chạy được ngay!**

---

## ❓ Troubleshooting

### 1. "Port đã được sử dụng"
- **Giải pháp:** Vào tab **"Thiết lập"** → Đổi port MySQL (3306) hoặc HTTP (8080)

### 2. "Không tìm thấy MySQL Server"
- **Giải pháp:** Đảm bảo thư mục `MySQL Server 9.5` nằm cùng cấp với `MySQL_Manager.exe`

### 3. "Lỗi đăng nhập phpMyAdmin"
- **Giải pháp:** Tab **"Thiết lập"** → Click **"Sửa lỗi đăng nhập"**

### 4. "Windows Defender cảnh báo"
- **Giải pháp:** Đây là false positive. Thêm vào exception hoặc tắt Defender tạm thời.

### 5. MySQL không start được
- **Giải pháp:** 
  - Kiểm tra port 3306 có đang được dùng không
  - Xóa thư mục `data` và chạy setup lại
  - Xem log trong tab **"Log & Trạng thái"**

---

## 📁 Cấu trúc dự án

```
open-mysql/
├── app.py                      # Main application
├── services/                   # Service management
│   ├── service_controller.py  # MySQL/PHP controllers
│   └── config_manager.py      # Config management
├── ui/                         # UI components
│   ├── app_bar.py             # Top bar
│   ├── components.py          # Reusable widgets
│   ├── logger_panel.py        # Log display
│   └── style_manager.py       # Theme/styles
├── config/                     # Configuration files
│   ├── default.json           # Default config
│   └── config.json            # User config
├── build_exe.bat              # Build script
├── package_final.bat          # Package script
├── requirements.txt            # Python dependencies
└── README.md                  # This file
```

---

## 🎨 Screenshots

### Light Theme
- Giao diện sáng, dễ nhìn
- Status cards với màu sắc rõ ràng

### Dark Theme
- Giao diện tối, bảo vệ mắt
- Toggle bằng nút 🌓

---

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! 

1. Fork dự án
2. Tạo branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

**Open MySQL Manager** được phân phối dưới giấy phép MIT License.

**⚠️ LƯU Ý QUAN TRỌNG VỀ BẢN QUYỀN:**

Dự án này bao gồm các phần mềm của bên thứ ba với giấy phép riêng:

- **MySQL Server 9.5 (Community Edition)**: 
  - Copyright (c) 1997-2025, Oracle and/or its affiliates
  - Giấy phép: GNU General Public License version 2 (GPLv2)
  - Nguồn: https://www.mysql.com/downloads/

- **phpMyAdmin 5.2.3**: 
  - Copyright (c) The phpMyAdmin devel team
  - Giấy phép: GNU General Public License version 2 (GPLv2)
  - Nguồn: https://www.phpmyadmin.net/

- **PHP (Portable Edition)**: 
  - Copyright (c) The PHP Group
  - Giấy phép: PHP License version 3.01
  - Nguồn: https://www.php.net/

### Sử dụng và Phân phối:

✅ **Được phép:**
- Sử dụng cho mục đích giáo dục, học tập, phát triển cá nhân
- Phân phối mã nguồn của Open MySQL Manager (MIT License)
- Sử dụng mã nguồn mở, không thương mại

⚠️ **Cần lưu ý:**
- Sử dụng thương mại có thể yêu cầu giấy phép riêng từ Oracle Corporation (cho MySQL)
- Khi phân phối lại, phải tuân thủ GPLv2 cho MySQL và phpMyAdmin
- Phải bao gồm tất cả các file giấy phép gốc

📄 **Xem file [LICENSE](LICENSE) để biết thông tin chi tiết về giấy phép và các disclaimer pháp lý.**

---

**Tuyên bố miễn trừ trách nhiệm:**

Dự án này là phần mềm mã nguồn mở, được cung cấp "như là" (as is), không có bảo hành. Tác giả không chịu trách nhiệm về bất kỳ thiệt hại nào phát sinh từ việc sử dụng phần mềm này. Người dùng tự chịu trách nhiệm tuân thủ tất cả các giấy phép và quy định pháp lý liên quan đến các phần mềm của bên thứ ba được bao gồm trong phân phối này.

---

## 👤 Author

**thanhtuanxzx**

- GitHub: [@thanhtuanxzx](https://github.com/thanhtuanxzx)
- Email: tuanzingm@gmail.com

---

## ⭐ Star History

Nếu dự án này hữu ích, hãy cho một ⭐ trên GitHub!

---

## 📞 Support

Nếu gặp vấn đề:
1. Xem phần [Troubleshooting](#-troubleshooting)
2. Tạo [Issue](https://github.com/thanhtuanxzx/open-mysql/issues)
3. Email: tuanzingm@gmail.com

---

**Made with ❤️ by thanhtuanxzx**

