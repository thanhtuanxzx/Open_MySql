<?php
/**
 * Router script for PHP Built-in Server
 * Routes /myadmin to phpMyAdmin directory
 */
$uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if ($uri === false) {
    $uri = '/';
}

if (strpos($uri, '/myadmin') !== 0) {
    return false;
}

if (preg_match('#^/myadmin(.*)$#', $uri, $matches)) {
    $path = $matches[1];
    if (empty($path)) {
        header('Location: /myadmin/');
        exit;
    }
    $path = ltrim($path, '/');
    if (empty($path)) {
        $path = 'index.php';
    }
    
    $phpMyAdminPath = __DIR__ . '/phpMyAdmin-5.2.3-all-languages/' . $path;
    
    if (file_exists($phpMyAdminPath) && is_file($phpMyAdminPath)) {
        if (preg_match('/\.php$/', $phpMyAdminPath)) {
            chdir(dirname($phpMyAdminPath));
            $_SERVER['SCRIPT_NAME'] = '/myadmin/' . $path;
            $_SERVER['PHP_SELF'] = '/myadmin/' . $path;
            require $phpMyAdminPath;
            exit;
        } else {
            $ext = strtolower(pathinfo($phpMyAdminPath, PATHINFO_EXTENSION));
            $mimeTypes = [
                'css' => 'text/css',
                'js' => 'application/javascript',
                'png' => 'image/png',
                'jpg' => 'image/jpeg',
                'jpeg' => 'image/jpeg',
                'gif' => 'image/gif',
                'svg' => 'image/svg+xml',
                'ico' => 'image/x-icon',
                'woff' => 'font/woff',
                'woff2' => 'font/woff2',
                'ttf' => 'font/ttf',
                'eot' => 'application/vnd.ms-fontobject',
                'json' => 'application/json',
                'xml' => 'application/xml',
                'txt' => 'text/plain',
                'html' => 'text/html',
                'htm' => 'text/html',
            ];
            $mimeType = $mimeTypes[$ext] ?? 'application/octet-stream';
            
            $lastModified = filemtime($phpMyAdminPath);
            $etag = md5_file($phpMyAdminPath);
            
            header('Content-Type: ' . $mimeType);
            header('Content-Length: ' . filesize($phpMyAdminPath));
            header('Cache-Control: public, max-age=3600');
            header('Last-Modified: ' . gmdate('D, d M Y H:i:s', $lastModified) . ' GMT');
            header('ETag: "' . $etag . '"');
            
            if (isset($_SERVER['HTTP_IF_MODIFIED_SINCE']) || isset($_SERVER['HTTP_IF_NONE_MATCH'])) {
                if (isset($_SERVER['HTTP_IF_NONE_MATCH']) && $_SERVER['HTTP_IF_NONE_MATCH'] === '"' . $etag . '"') {
                    http_response_code(304);
                    exit;
                }
            }
            
            readfile($phpMyAdminPath);
            exit;
        }
    } else {
        if (is_dir($phpMyAdminPath)) {
            $indexPath = $phpMyAdminPath . '/index.php';
            if (file_exists($indexPath)) {
                chdir($phpMyAdminPath);
                $_SERVER['SCRIPT_NAME'] = '/myadmin/' . rtrim($path, '/') . '/index.php';
                $_SERVER['PHP_SELF'] = '/myadmin/' . rtrim($path, '/') . '/index.php';
                require $indexPath;
                exit;
            }
        }
        http_response_code(404);
        echo "404 - File not found: /myadmin" . $path;
        exit;
    }
}
return false;
