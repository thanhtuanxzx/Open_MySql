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

- ✅ Giao diện hiện đại xây dựng trên `ttkbootstrap`
- ✅ Theme sáng/tối linh hoạt (Light / Dark mode toggle)
- ✅ Quản lý đồng bộ: **MySQL Server 9.5**, **PHP Built-in Server**, **phpMyAdmin 5.2.3**
- ✅ Giám sát trạng thái thời gian thực (Status Cards: Running / Stopped)
- ✅ Bảng điều khiển Log đa luồng (Thread-safe Logger Panel)
- ✅ Tùy chỉnh cổng linh hoạt (MySQL default: 3306, HTTP default: 8080)
- ✅ Tự động khởi tạo và cấu hình `my.ini` và `config.inc.php`
- ✅ **100% Portable** - Chạy trực tiếp từ mã nguồn Python hoặc file `.exe`, không cần cài đặt vào hệ thống

---

## 📋 Yêu cầu hệ thống

- Hệ điều hành: Windows 10 / 11 (64-bit)
- Chạy trực tiếp từ `.exe`: **Không cần cài đặt gì thêm**
- Chạy từ mã nguồn: Python 3.8+ (khuyến nghị Python 3.10 - 3.13)

---

## 💻 Hướng dẫn chạy từ mã nguồn Python

Nếu bạn là lập trình viên muốn phát triển hoặc tùy biến giao diện:

1. **Clone repository:**
   ```bash
   git clone https://github.com/thanhtuanxzx/Open_MySql.git
   cd Open_MySql
   ```

2. **Cài đặt các thư viện cần thiết:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Khởi chạy ứng dụng:**
   ```bash
   python app.py
   ```
   *Hoặc click đúp trực tiếp vào file `run.bat`.*

4. **Đóng gói lại thành file `.exe`:**
   ```bash
   build_exe.bat
   ```

---

## 🎯 Hướng dẫn sử dụng Portable (.exe)

1. Tải bản release hoặc mở thư mục dự án `Open_MySql`.
2. Chạy trực tiếp file `MySQL_Manager.exe`.
3. **Lần đầu sử dụng**:
   - Nhấn nút **"⚙️ Thiết lập ban đầu"** (hoặc vào tab **"Thiết lập"** → **"Bắt đầu thiết lập"**).
   - Ứng dụng sẽ tự động khởi tạo:
     - Cấu hình MySQL (`MySQL Server 9.5/my.ini`)
     - Cấu hình phpMyAdmin (`config.inc.php`)
     - Cổng mạng và các đường dẫn tương ứng
4. **Khởi động dịch vụ:**
   - Nhấn **"Khởi động phpMyAdmin"**: Tự động bật MySQL + PHP Web Server và mở trình duyệt tại `http://localhost:8080`.
   - Đăng nhập mặc định:
     - **Tài khoản:** `root`
     - **Mật khẩu:** *(để trống)*
   - Khi hoàn thành công việc, nhấn **"Dừng tất cả"** để tắt an toàn mọi dịch vụ.

---

## 📖 Các tab trong ứng dụng

### 1. **Chức năng chính** (Tab mặc định)
- 🟢 **Khởi động phpMyAdmin** - Start MySQL + PHP + mở browser
- 🔵 **Khởi động MySQL Server** - Chỉ start MySQL
- 🔴 **Dừng tất cả** - Dừng tất cả dịch vụ đang chạy
- 📋 **Log panel** - Xem logs hoạt động thời gian thực

### 2. **Trạng thái**
- Thẻ giám sát trạng thái chi tiết của từng dịch vụ: MySQL Server, PHP Web Server
- Cho phép Bật / Tắt riêng lẻ từng thành phần

### 3. **Thiết lập**
- ⚙️ **Bắt đầu thiết lập** - Tự động thiết lập cấu hình ban đầu
- 🔐 **Sửa lỗi đăng nhập** - Khôi phục cấu hình xác thực phpMyAdmin
- 🔌 **Cấu hình ports**:
  - MySQL Port (mặc định: `3306`)
  - HTTP Port (mặc định: `8080`)
- 📁 **Chọn thư mục PHP** - Cho phép đổi bản phân phối PHP tùy ý

### 4. **Log & Trạng thái**
- Hiển thị đầy đủ lịch sử hoạt động hệ thống kèm chức năng cuộn
- Nút **"🔄 Làm mới trạng thái"** cập nhật tức thì trạng thái cổng

---

## 📁 Cấu trúc dự án

```text
Open_MySql/
├── app.py                      # Điểm vào chính của ứng dụng (GUI Tkinter)
├── services/                   # Quản lý dịch vụ & cấu hình ngầm
│   ├── __init__.py
│   ├── config_manager.py       # Quản lý đọc/ghi cấu hình JSON
│   └── service_controller.py   # Điều khiển tiến trình MySQL, PHP, check port
├── ui/                         # Các thành phần giao diện
│   ├── __init__.py
│   ├── app_bar.py              # Thanh tiêu đề, nút thu nhỏ / đóng
│   ├── components.py           # Thẻ trạng thái (StatusCard), nút bấm (ActionButton)
│   ├── logger_panel.py         # Khung hiển thị Log đa luồng
│   └── style_manager.py        # Quản lý theme Light / Dark
├── MySQL Server 9.5/           # Máy chủ MySQL Server Portable
├── php/                        # Môi trường chạy PHP Portable
├── phpMyAdmin-5.2.3-.../       # Giao diện web quản trị cơ sở dữ liệu
├── data/                       # Thư mục lưu trữ database của MySQL
├── requirements.txt            # Danh sách thư viện Python phụ thuộc
├── MySQL_Manager.exe           # Bản thực thi đóng gói sẵn
├── .gitignore                  # Cấu hình bỏ qua file runtime/cache cho Git
└── README.md                   # Tài liệu hướng dẫn này
```

---

## 🔧 Cấu hình: `config/config.json`

File cấu hình được sinh tự động khi chạy ứng dụng:

```json
{
  "mysql": {
    "port": 3306,
    "data_dir": "data",
    "basedir": "MySQL Server 9.5",
    "my_ini_path": "MySQL Server 9.5/my.ini"
  },
  "php": {
    "port": 8080,
    "php_dir": "php",
    "php_exe_path": "php/php.exe"
  },
  "phpmyadmin": {
    "dir": "phpMyAdmin-5.2.3-all-languages",
    "config_path": "phpMyAdmin-5.2.3-all-languages/config.inc.php"
  },
  "theme": "light",
  "last_php_path": ""
}
```

---

## ❓ Xử lý sự cố thường gặp (Troubleshooting)

### 1. "Port đã được sử dụng (Port already in use)"
- **Cách khắc phục:** Vào tab **"Thiết lập"** → Đổi port MySQL khác `3306` (ví dụ `3307`) hoặc HTTP khác `8080` (ví dụ `8088`).

### 2. "Lỗi đăng nhập phpMyAdmin"
- **Cách khắc phục:** Vào tab **"Thiết lập"** → Nhấn nút **"🔐 Sửa lỗi đăng nhập"** để tạo lại cấu hình cookie authentication.

### 3. "MySQL Server không khởi động được"
- **Cách khắc phục:**
  - Kiểm tra xem có instance `mysqld.exe` nào đang chạy ngầm bằng Task Manager.
  - Kiểm tra xem file log lỗi tại `data/mysql-error.log`.

---

## 🤝 Đóng góp

Mọi đóng góp nhằm cải thiện phần mềm đều được chào đón! 

1. Fork dự án
2. Tạo nhánh tính năng (`git checkout -b feature/AmazingFeature`)
3. Commit thay đổi (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push lên nhánh của bạn (`git push origin feature/AmazingFeature`)
5. Mở một Pull Request

---

## 📝 Bản quyền & Giấy phép

**Open MySQL Manager** được phân phối theo giấy phép **MIT License**.

- **MySQL Server 9.5 (Community Edition)**: Oracle Corporation (GPLv2)
- **phpMyAdmin 5.2.3**: phpMyAdmin devel team (GPLv2)
- **PHP**: The PHP Group (PHP License 3.01)

Xem chi tiết trong file [LICENSE](LICENSE).

---

## 👤 Tác giả

**thanhtuanxzx**
- GitHub: [@thanhtuanxzx](https://github.com/thanhtuanxzx)
- Email: tuanzingm@gmail.com
- Repository: [thanhtuanxzx/Open_MySql](https://github.com/thanhtuanxzx/Open_MySql)

⭐ **Nếu thấy dự án hữu ích, đừng quên tặng repo một Star trên GitHub nhé!**
