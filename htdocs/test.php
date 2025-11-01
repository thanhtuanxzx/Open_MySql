<?php
/**
 * Test PHP file for htdocs directory
 */
?>
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PHP Test - Open MySQL</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            margin: 0;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 800px;
            width: 100%;
            padding: 40px;
        }
        h1 {
            color: #667eea;
            margin-bottom: 30px;
        }
        .info-box {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 15px;
        }
        .info-box strong {
            color: #667eea;
        }
        .success {
            color: #198754;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>✅ PHP Test Page - htdocs</h1>
        
        <div class="info-box">
            <strong>PHP Version:</strong> <?php echo phpversion(); ?>
        </div>
        
        <div class="info-box">
            <strong>Server Software:</strong> <?php echo $_SERVER['SERVER_SOFTWARE'] ?? 'PHP Built-in Server'; ?>
        </div>
        
        <div class="info-box">
            <strong>Document Root:</strong> <?php echo $_SERVER['DOCUMENT_ROOT'] ?? __DIR__; ?>
        </div>
        
        <div class="info-box">
            <strong>Script Name:</strong> <?php echo $_SERVER['SCRIPT_NAME']; ?>
        </div>
        
        <div class="info-box">
            <strong>Request URI:</strong> <?php echo $_SERVER['REQUEST_URI']; ?>
        </div>
        
        <div class="info-box">
            <strong>Current Time:</strong> <?php echo date('Y-m-d H:i:s'); ?>
        </div>
        
        <div class="info-box">
            <strong>Loaded Extensions:</strong><br>
            <?php
            $extensions = get_loaded_extensions();
            echo implode(', ', array_slice($extensions, 0, 10)) . '... (Total: ' . count($extensions) . ')';
            ?>
        </div>
        
        <div class="info-box">
            <strong>MySQL Extension:</strong> 
            <?php 
            if (extension_loaded('mysqli')) {
                echo '<span class="success">✓ mysqli loaded</span>';
            } else {
                echo '<span style="color: red;">✗ mysqli not loaded</span>';
            }
            ?>
        </div>
        
        <div class="info-box">
            <strong>Test MySQL Connection:</strong><br>
            <?php
            if (extension_loaded('mysqli')) {
                $mysqli = @new mysqli('localhost', 'root', '', '', 3306);
                if ($mysqli->connect_error) {
                    echo '<span style="color: orange;">⚠ ' . $mysqli->connect_error . '</span>';
                } else {
                    echo '<span class="success">✓ MySQL connection successful!</span>';
                    $mysqli->close();
                }
            } else {
                echo '<span style="color: red;">✗ mysqli extension not available</span>';
            }
            ?>
        </div>
        
        <div style="margin-top: 30px; text-align: center;">
            <a href="/" style="color: #667eea; text-decoration: none; font-weight: bold;">← Back to Homepage</a>
        </div>
    </div>
</body>
</html>

