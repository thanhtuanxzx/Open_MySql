# 🎯 Hướng dẫn lần đầu sử dụng Open MySQL

Chào mừng bạn đến với **Open MySQL**! Hướng dẫn này sẽ giúp bạn bắt đầu trong vài phút.

> **⚠️ LƯU Ý PHÁP LÝ:** Dự án này là mã nguồn mở, miễn phí, dùng cho mục đích giáo dục và cá nhân. Phần mềm này bao gồm các thành phần của bên thứ ba (MySQL Server, phpMyAdmin, PHP) với giấy phép riêng. Xem [LICENSE](LICENSE) để biết thêm chi tiết.

---

## 📦 Bước 1: Chuẩn bị

### Nếu bạn chạy từ .exe (Khuyến nghị):

✅ **KHÔNG CẦN** cài đặt gì cả! Chỉ cần:

1. **Tải xuống** thư mục `final` (từ release hoặc sau khi chạy `package_final.bat`)
2. **Giải nén** vào bất kỳ thư mục nào trên máy tính
3. **Double-click** `MySQL_Manager.exe` → Xong!

> **Lưu ý:** Lần đầu chạy, Windows có thể hiển thị cảnh báo Windows Defender. Đây là false positive. Bạn có thể thêm file vào danh sách ngoại lệ hoặc tạm thời tắt Windows Defender để chạy.

---

## 🚀 Bước 2: Lần đầu mở app

Khi mở app lần đầu, bạn sẽ thấy giao diện như sau:

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

**⚠️ BẮT BUỘC:** Bạn phải chạy setup lần đầu để ứng dụng hoạt động đúng.

### Cách 1: Dùng nút Setup (Khuyến nghị)

1. Click nút **"⚙️ Thiết lập ban đầu"** ở góc phải trên cùng
2. Ứng dụng sẽ tự động thực hiện:
   - ✅ Tạo file `my.ini` cho MySQL Server
   - ✅ Tạo file `config.inc.php` cho phpMyAdmin
   - ✅ Cấu hình ports mặc định (MySQL: 3306, HTTP: 8080)
   - ✅ Tạo thư mục `data` cho database (nếu chưa có)
   - ✅ Khởi tạo MySQL data directory (nếu lần đầu)

### Cách 2: Dùng tab Thiết lập

1. Click tab **"Thiết lập"** ở phía trên
2. Click nút **"Bắt đầu thiết lập"**
3. Chờ thông báo **"✅ Thiết lập thành công!"**

**📌 LƯU Ý:** Chỉ cần setup **1 LẦN DUY NHẤT**. Lần sau mở app sẽ tự động load cấu hình đã lưu.

**❌ Nếu setup thất bại:**
- Kiểm tra quyền ghi vào thư mục hiện tại
- Đảm bảo không có process MySQL nào đang chạy
- Xem log trong tab **"Log & Trạng thái"** để biết lỗi cụ thể

---

## 🎮 Bước 4: Sử dụng

### Khởi động phpMyAdmin (Cách dễ nhất và khuyến nghị):

1. Click nút **"🟢 Khởi động phpMyAdmin"** ở tab **"Chức năng chính"**
2. Ứng dụng sẽ tự động:
   - ✅ Khởi động MySQL Server
   - ✅ Khởi động PHP Web Server
   - ✅ Tự động mở trình duyệt: `http://localhost:8080`

3. **Đăng nhập phpMyAdmin:**
   ```
   Username: root
   Password: (để trống - không nhập gì)
   ```

4. **✅ Hoàn thành!** Bạn đã có thể quản lý database qua phpMyAdmin.

**💡 Tips:**
- phpMyAdmin cho phép bạn tạo, xóa, quản lý database và bảng
- Có thể import/export database từ giao diện web
- Hỗ trợ SQL editor để chạy truy vấn trực tiếp

### Chỉ khởi động MySQL Server:

1. Click nút **"🔵 Khởi động MySQL Server"**
2. MySQL Server sẽ chạy, nhưng **KHÔNG** mở phpMyAdmin
3. **Khi nào dùng:**
   - Kết nối MySQL từ ứng dụng khác (MySQL Workbench, DBeaver, HeidiSQL, v.v.)
   - Kết nối từ command line: `mysql -u root -p`
   - Kết nối từ ứng dụng Python/Node.js/Java, v.v.

**📌 Thông tin kết nối:**
- Host: `localhost` hoặc `127.0.0.1`
- Port: `3306` (mặc định)
- Username: `root`
- Password: `(để trống)`

### Dừng tất cả services:

1. Click nút **"🔴 Dừng tất cả"**
2. Tất cả services (MySQL, PHP Web Server) sẽ được dừng an toàn
3. **⚠️ LƯU Ý:** Luôn dừng services trước khi đóng ứng dụng

---

## 📊 Theo dõi trạng thái

### Tab "Trạng thái":

Hiển thị trạng thái real-time của các services:

- **MySQL Server**: 
  - 🟢 **Đang chạy** - Port 3306 đang active
  - ⚪ **Không chạy** - Service chưa được khởi động

- **PHP Web Server**: 
  - 🟢 **Đang chạy** - Port 8080 đang active
  - ⚪ **Không chạy** - Service chưa được khởi động

- **PHP Portable**: 
  - ✅ **Đã cài** - Thư mục PHP tồn tại
  - ❌ **Chưa có** - Cần chọn thư mục PHP

**🔧 Chức năng:**
- Click **"Khởi động"** để start từng service riêng lẻ
- Click **"Dừng"** để stop từng service riêng lẻ
- Click **"Làm mới"** để cập nhật trạng thái

### Tab "Log & Trạng thái":

- Xem logs chi tiết của tất cả operations
- Log panel có scroll tự động
- Click **"Làm mới trạng thái"** để cập nhật thông tin
- Dùng để debug khi gặp vấn đề

---

## 🔧 Các tính năng khác

### 1. Đổi Theme (Sáng/Tối):

- Click nút **🌓** ở góc phải trên cùng
- Theme sẽ chuyển đổi giữa:
  - **Sáng (Flatly)**: Giao diện sáng, dễ nhìn ban ngày
  - **Tối (Darkly)**: Giao diện tối, bảo vệ mắt, tốt khi làm việc lâu

**💡 Tip:** Theme được lưu tự động, lần sau mở app sẽ giữ theme đã chọn.

### 2. Cấu hình Ports:

Nếu port mặc định bị conflict, bạn có thể đổi:

1. Vào tab **"Thiết lập"**
2. Tìm phần **"Cấu hình Ports"**
3. Đổi **MySQL Port** (mặc định: 3306)
4. Đổi **HTTP Port** (mặc định: 8080)
5. Click **"Lưu cấu hình"**
6. **Restart** các services để áp dụng thay đổi

**⚠️ LƯU Ý:** 
- MySQL Port thường là 3306
- HTTP Port có thể đổi thành 8081, 8082, 9000, v.v. nếu 8080 bị dùng
- Sau khi đổi port, URL phpMyAdmin sẽ là: `http://localhost:<port_mới>`

### 3. Sửa lỗi đăng nhập phpMyAdmin:

Nếu không đăng nhập được phpMyAdmin:

1. Vào tab **"Thiết lập"**
2. Click nút **"🔧 Sửa lỗi đăng nhập"**
3. Ứng dụng sẽ tự động:
   - Reset password cho user `root`
   - Sửa file `config.inc.php` của phpMyAdmin
   - Tạo lại MySQL user nếu cần
   - Kiểm tra và fix các vấn đề phổ biến

**📌 Sau khi sửa:**
- Thử đăng nhập lại với: `root` / `(để trống)`
- Nếu vẫn lỗi, xem log trong tab **"Log & Trạng thái"**

### 4. Chọn thư mục PHP:

Nếu ứng dụng không tìm thấy PHP:

1. Vào tab **"Trạng thái"**
2. Tìm card **"PHP 8.2.x (Portable)"**
3. Click **"Chọn thư mục PHP..."**
4. Chọn thư mục chứa file `php.exe`
5. Click **"OK"**

**💡 Tip:** Thư mục PHP thường là `php` trong cùng thư mục với `MySQL_Manager.exe`.

### 5. Chọn thư mục Data:

Thư mục `data` chứa tất cả database files. Bạn có thể đổi nơi lưu:

1. Vào tab **"Thiết lập"**
2. Tìm phần **"Thư mục Data"**
3. Click **"Chọn thư mục Data..."**
4. Chọn thư mục mới
5. Click **"Lưu"**

**⚠️ CẢNH BÁO:** 
- Đổi thư mục data sẽ làm mất tất cả database cũ
- Chỉ đổi khi thực sự cần thiết
- Sao lưu thư mục `data` trước khi đổi

---

## ❗ Lưu ý quan trọng

### ✅ NÊN LÀM:

- ✅ **Setup lần đầu** trước khi sử dụng
- ✅ **Xem logs** nếu gặp lỗi hoặc vấn đề
- ✅ **Đổi ports** nếu bị conflict với ứng dụng khác
- ✅ **Đóng app đúng cách**: Dùng nút **"🔴 Dừng tất cả"** trước khi đóng
- ✅ **Sao lưu** thư mục `data` định kỳ nếu có dữ liệu quan trọng
- ✅ **Đọc README.md** để hiểu rõ hơn về dự án

### ❌ KHÔNG NÊN:

- ❌ **Không đóng app** khi services đang chạy (dùng "Dừng tất cả" trước)
- ❌ **Không xóa** thư mục `config` (sẽ mất tất cả cấu hình)
- ❌ **Không xóa** thư mục `data` (trừ khi muốn reset toàn bộ database)
- ❌ **Không chỉnh sửa** file `my.ini` hoặc `config.inc.php` thủ công (trừ khi biết rõ)
- ❌ **Không sử dụng** cho mục đích thương mại mà không có giấy phép phù hợp

---

## 🐛 Khắc phục sự cố

### 1. "Port đã được sử dụng" (Port already in use)

**Nguyên nhân:** Port 3306 (MySQL) hoặc 8080 (HTTP) đang được sử dụng bởi ứng dụng khác.

**Giải pháp:**
- Vào tab **"Thiết lập"** → Đổi **MySQL Port** hoặc **HTTP Port**
- Hoặc tắt ứng dụng đang dùng port đó:
  - MySQL: Kiểm tra MySQL service trong Windows Services
  - HTTP: Kiểm tra Apache, IIS, hoặc ứng dụng web khác đang chạy

### 2. "Không tìm thấy MySQL Server"

**Nguyên nhân:** Thư mục `MySQL Server 9.5` không nằm đúng vị trí.

**Giải pháp:**
- Đảm bảo thư mục `MySQL Server 9.5` nằm **cùng cấp** với `MySQL_Manager.exe`
- Cấu trúc đúng:
  ```
  Open_MySql/
  ├── MySQL_Manager.exe
  ├── MySQL Server 9.5/    ← Phải có
  ├── php/
  └── ...
  ```

### 3. "Lỗi đăng nhập phpMyAdmin"

**Nguyên nhân:** Cấu hình phpMyAdmin hoặc MySQL user bị lỗi.

**Giải pháp:**
1. Vào tab **"Thiết lập"** → Click **"🔧 Sửa lỗi đăng nhập"**
2. Thử đăng nhập lại:
   - Username: `root`
   - Password: `(để trống)`
3. Nếu vẫn lỗi, kiểm tra log trong tab **"Log & Trạng thái"**

### 4. "MySQL không start được"

**Nguyên nhân:** Nhiều khả năng (port conflict, lỗi config, permission, v.v.)

**Giải pháp:**
1. **Kiểm tra port:** Xem có ứng dụng nào dùng port 3306 không
2. **Kiểm tra quyền:** Đảm bảo có quyền ghi vào thư mục `data`
3. **Reset data:** Xóa thư mục `data` và chạy setup lại (⚠️ sẽ mất tất cả database)
4. **Xem log:** Tab **"Log & Trạng thái"** sẽ hiển thị lỗi cụ thể
5. **Kiểm tra file my.ini:** Đảm bảo file `MySQL Server 9.5/my.ini` tồn tại và đúng cấu hình

### 5. "Windows Defender cảnh báo"

**Nguyên nhân:** Windows Defender có thể nhận diện nhầm file .exe là virus (false positive).

**Giải pháp:**
- **Cách 1:** Thêm `MySQL_Manager.exe` vào danh sách ngoại lệ của Windows Defender
- **Cách 2:** Tạm thời tắt Windows Defender khi chạy lần đầu
- **Giải thích:** Đây là file Python được compile thành .exe, hoàn toàn an toàn

### 6. "PHP Web Server không start"

**Nguyên nhân:** Không tìm thấy PHP hoặc port HTTP bị conflict.

**Giải pháp:**
1. Kiểm tra thư mục `php` có tồn tại và chứa `php.exe`
2. Tab **"Trạng thái"** → Click **"Chọn thư mục PHP..."** nếu cần
3. Đổi HTTP Port nếu port 8080 bị dùng

### 7. "Browser không tự động mở"

**Nguyên nhân:** Hệ thống hoặc trình duyệt không hỗ trợ auto-open.

**Giải pháp:**
- Mở trình duyệt thủ công và truy cập: `http://localhost:8080`
- Đảm bảo PHP Web Server đã start (kiểm tra trong tab **"Trạng thái"**)

---

## 📚 Tài liệu tham khảo

- **README.md**: Tài liệu chính của dự án
- **LICENSE**: Thông tin về giấy phép và bản quyền
- **MySQL Documentation**: https://dev.mysql.com/doc/
- **phpMyAdmin Documentation**: https://docs.phpmyadmin.net/
- **PHP Documentation**: https://www.php.net/docs.php

---

## ⚖️ Thông tin pháp lý

**Open MySQL Manager** là phần mềm mã nguồn mở, miễn phí, dùng cho mục đích giáo dục và cá nhân.

### Giấy phép:

- **Open MySQL Manager**: MIT License (xem [LICENSE](LICENSE))
- **MySQL Server**: GNU General Public License version 2 (GPLv2)
- **phpMyAdmin**: GNU General Public License version 2 (GPLv2)
- **PHP**: PHP License version 3.01

### Sử dụng:

- ✅ **Được phép:** Dùng cho mục đích giáo dục, học tập, phát triển cá nhân
- ⚠️ **Cần lưu ý:** Sử dụng thương mại có thể yêu cầu giấy phép riêng từ Oracle (MySQL), phpMyAdmin team, và PHP Group

### Liên hệ:

Nếu có câu hỏi về giấy phép hoặc bản quyền:
- **Open MySQL Manager**: tuanzingm@gmail.com
- **MySQL Licensing**: https://www.mysql.com/about/legal/licensing/
- **phpMyAdmin**: https://www.phpmyadmin.net/team/

---

## 🎉 Hoàn thành!

Bây giờ bạn đã sẵn sàng sử dụng Open MySQL!

### Tips hữu ích:

- Tab **"Chức năng chính"** là nơi bạn sẽ dùng nhiều nhất
- Theme tối (dark mode) tốt cho mắt khi làm việc lâu
- Log panel giúp debug khi có vấn đề
- Sao lưu thư mục `data` định kỳ nếu có dữ liệu quan trọng

### Cần giúp đỡ?

1. Xem [README.md](README.md) để biết thêm thông tin
2. Kiểm tra phần [Khắc phục sự cố](#-khắc-phục-sự-cố) ở trên
3. Tạo [Issue trên GitHub](https://github.com/thanhtuanxzx/open-mysql/issues)
4. Email: tuanzingm@gmail.com

---

**Made with ❤️ by [thanhtuanxzx](https://github.com/thanhtuanxzx)**

*Phiên bản 2.0 | MIT License | Open Source - Non-commercial use*
