<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Open MySQL - Portable MySQL Manager</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 800px;
            width: 100%;
            padding: 60px 40px;
            text-align: center;
        }
        
        .logo {
            width: 120px;
            height: 120px;
            margin: 0 auto 30px;
            border-radius: 30px;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
            overflow: hidden;
            background: white;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 8px;
        }
        
        .logo img {
            width: 100%;
            height: 100%;
            object-fit: contain;
            object-position: center;
        }
        
        h1 {
            color: #333;
            font-size: 42px;
            margin-bottom: 10px;
            font-weight: 700;
        }
        
        .subtitle {
            color: #666;
            font-size: 18px;
            margin-bottom: 50px;
        }
        
        .actions {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        
        .action-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 30px;
            border-radius: 12px;
            text-decoration: none;
            font-size: 18px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        
        .action-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        }
        
        .action-btn.secondary {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            box-shadow: 0 4px 15px rgba(245, 87, 108, 0.3);
        }
        
        .action-btn.secondary:hover {
            box-shadow: 0 8px 25px rgba(245, 87, 108, 0.4);
        }
        
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 40px;
        }
        
        .info-card {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 12px;
            border: 2px solid #e9ecef;
        }
        
        .info-card h3 {
            color: #667eea;
            font-size: 20px;
            margin-bottom: 10px;
        }
        
        .info-card p {
            color: #666;
            font-size: 14px;
            line-height: 1.6;
        }
        
        .status-badge {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            margin-top: 8px;
        }
        
        .status-running {
            background: #d4edda;
            color: #155724;
        }
        
        .status-stopped {
            background: #f8d7da;
            color: #721c24;
        }
        
        .footer {
            margin-top: 50px;
            padding-top: 30px;
            border-top: 2px solid #e9ecef;
            color: #999;
            font-size: 14px;
        }
        
        .footer a {
            color: #667eea;
            text-decoration: none;
        }
        
        .footer a:hover {
            text-decoration: underline;
        }
        
        @media (max-width: 600px) {
            .container {
                padding: 40px 20px;
            }
            
            h1 {
                font-size: 32px;
            }
            
            .actions {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <img src="/logo.jpg" alt="Open MySQL Logo" onerror="this.style.display='none'; this.parentElement.innerHTML='OM'; this.parentElement.style.background='linear-gradient(135deg, #667eea 0%, #764ba2 100%)'; this.parentElement.style.color='white'; this.parentElement.style.fontSize='48px'; this.parentElement.style.fontWeight='bold';">
        </div>
        <h1>Open MySQL</h1>
        <p class="subtitle">Portable MySQL Manager by thanhtuanxzx</p>
        
        <div class="actions">
            <a href="/myadmin" class="action-btn">
                <span>🗄️</span>
                <span>Mở phpMyAdmin</span>
            </a>
            <a href="/htdocs/test.php" class="action-btn secondary">
                <span>🧪</span>
                <span>Test PHP (htdocs)</span>
            </a>
            <a href="https://github.com/thanhtuanxzx/Open_MySql" target="_blank" class="action-btn secondary">
                <span>⭐</span>
                <span>GitHub Repository</span>
            </a>
        </div>
        
        <div class="info-grid">
            <div class="info-card">
                <h3>MySQL Server</h3>
                <p>Port: 3306</p>
                <span class="status-badge status-running">Sẵn sàng</span>
            </div>
            
            <div class="info-card">
                <h3>PHP Web Server</h3>
                <p>Port: 8080</p>
                <span class="status-badge status-running">Đang chạy</span>
            </div>
            
            <div class="info-card">
                <h3>phpMyAdmin</h3>
                <p>Phiên bản 5.2.3</p>
                <span class="status-badge status-running">Hoạt động</span>
            </div>
        </div>
        
        <div class="footer">
            <p>Made with ❤️ by <a href="https://github.com/thanhtuanxzx/Open_MySql" target="_blank">thanhtuanxzx</a></p>
            <p style="margin-top: 10px;">© 2024 Open MySQL - All rights reserved</p>
        </div>
    </div>
</body>
</html>

