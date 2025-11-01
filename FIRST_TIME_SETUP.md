# 🎯 Hướng dẫn lần đầu sử dụng Open MySQL

Chào mừng bạn đến với **Open MySQL**! Hướng dẫn này sẽ giúp bạn bắt đầu trong vài phút.

---

## 📦 Bước 1: Chuẩn bị

### Nếu bạn chạy từ .exe (Khuyến nghị):
✅ **KHÔNG CẦN** cài đặt gì cả! Chỉ cần:
1. Download thư mục `final` (từ release hoặc sau khi chạy `package_final.bat`)
2. Giải nén vào bất kỳ đâu
3. Double-click `MySQL_Manager.exe` → Xong!

### Nếu bạn chạy từ source code:
```bash
# 1. Cài dependencies
pip install -r requirements.txt

# 2. Chạy app
python app.py
```

---

## 🚀 Bước 2: Lần đầu mở app

Khi mở app lần đầu, bạn sẽ thấy:

```
┌─────────────────────────────────────────┐
│  Open MySQL                    🌓  ⚙️   │
├─────────────────────────────────────────┤
│ [Tab: Chức năng chính]                  │
│                                         │
│  [🟢 Khởi động phpMyAdmin]              │
│  [🔵 Khởi động MySQL Server]            │
│  [🔴 Dừng tất cả]                       │
│                                         │
│  ┌─ Log Panel ───────────────┐         │
│  │ [Logs sẽ hiển thị ở đây]  │         │
│  └───────────────────────────┘         │
└─────────────────────────────────────────┘
```

---

## ⚙️ Bước 3: Thiết lập ban đầu (QUAN TRỌNG!)

### Cách 1: Dùng nút Setup
1. Click nút **"⚙️ Thiết lập ban đầu"** ở góc phải trên
2. App sẽ tự động:
   - ✅ Tạo file `my.ini` cho MySQL
   - ✅ Tạo file `config.inc.php` cho phpMyAdmin
   - ✅ Cấu hình ports (MySQL: 3306, HTTP: 8080)
   - ✅ Tạo thư mục `data` cho database

### Cách 2: Dùng tab Thiết lập
1. Click tab **"Thiết lập"** ở trên
2. Click nút **"Bắt đầu thiết lập"**
3. Chờ thông báo "Thiết lập thành công!"

**⚠️ LƯU Ý:** Chỉ cần setup **1 LẦN DUY NHẤT**. Lần sau mở app sẽ tự động load config.

---

## 🎮 Bước 4: Sử dụng

### Khởi động phpMyAdmin (Cách dễ nhất):

1. Click nút **"🟢 Khởi động phpMyAdmin"** ở tab **"Chức năng chính"**
2. App sẽ:
   - ✅ Start MySQL Server
   - ✅ Start PHP Web Server
   - ✅ Tự động mở browser: `http://localhost:8080`

3. Đăng nhập phpMyAdmin:
   ```
   Username: root
   Password: (để trống)
   ```

4. **Xong!** Bạn đã có thể quản lý database qua phpMyAdmin.

### Chỉ khởi động MySQL:

1. Click nút **"🔵 Khởi động MySQL Server"**
2. MySQL sẽ chạy, nhưng **KHÔNG** mở phpMyAdmin
3. Dùng khi bạn muốn kết nối MySQL từ app khác (như Workbench, DBeaver)

### Dừng tất cả:

1. Click nút **"🔴 Dừng tất cả"**
2. Tất cả services sẽ được stop

---

## 📊 Theo dõi trạng thái

### Tab "Trạng thái":
- **MySQL Server**: 🟢 Đang chạy / ⚪ Không chạy
- **PHP Web Server**: 🟢 Đang chạy / ⚪ Không chạy  
- **PHP Portable**: ✅ Đã cài / ❌ Chưa có

### Tab "Log & Trạng thái":
- Xem logs chi tiết
- Click **"Làm mới trạng thái"** để cập nhật

---

## 🔧 Các tính năng khác

### 1. Đổi Theme (Sáng/Tối):
- Click nút **🌓** ở góc phải trên
- Theme sẽ chuyển giữa sáng (flatly) ↔ tối (darkly)

### 2. Đổi Ports:
1. Tab **"Thiết lập"**
2. Đổi **MySQL Port** (mặc định: 3306)
3. Đổi **HTTP Port** (mặc định: 8080)
4. Lưu và restart services

### 3. Sửa lỗi đăng nhập:
- Tab **"Thiết lập"** → Click **"Sửa lỗi đăng nhập"**
- App sẽ tự động fix các vấn đề phổ biến:
  - Reset password root
  - Fix config.inc.php
  - Tạo lại user MySQL

### 4. Chọn thư mục PHP:
- Tab **"Trạng thái"** → Card **"PHP 8.2.x (Portable)"**
- Click **"Chọn thư mục PHP..."**
- Chọn thư mục chứa `php.exe`

---

## ❗ Lưu ý quan trọng

### ✅ DO (Nên làm):
- ✅ Setup lần đầu trước khi dùng
- ✅ Xem logs nếu có lỗi
- ✅ Đổi ports nếu bị conflict
- ✅ Đóng app bằng nút X, không force quit

### ❌ DON'T (Không nên):
- ❌ Không đóng app khi services đang chạy (dùng "Dừng tất cả" trước)
- ❌ Không xóa thư mục `config` (sẽ mất cấu hình)
- ❌ Không xóa thư mục `data` (trừ khi muốn reset database)

---

## 🐛 Gặp vấn đề?

### "Port đã được sử dụng"
→ Vào **"Thiết lập"** → Đổi port

### "Không tìm thấy MySQL Server"
→ Đảm bảo thư mục `MySQL Server 9.5` nằm cùng cấp với `.exe`

### "Lỗi đăng nhập phpMyAdmin"
→ **"Thiết lập"** → **"Sửa lỗi đăng nhập"**

### MySQL không start
→ Xem log trong tab **"Log & Trạng thái"** để biết lỗi cụ thể

---

## 🎉 Hoàn thành!

Bây giờ bạn đã sẵn sàng sử dụng Open MySQL!

**Tips:**
- Tab **"Chức năng chính"** là nơi bạn sẽ dùng nhiều nhất
- Theme tối tốt cho mắt khi làm việc lâu
- Log panel giúp debug khi có vấn đề

**Need help?** → Xem [README.md](README.md) hoặc tạo [Issue](https://github.com/thanhtuanxzx/open-mysql/issues)

---

**Made with ❤️ by [thanhtuanxzx](https://github.com/thanhtuanxzx)**

