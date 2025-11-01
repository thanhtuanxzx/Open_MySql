<?php
declare(strict_types=1);

// Blowfish secret for cookie authentication
$cfg['blowfish_secret'] = 'phpMyAdmin2024SecretKey12345678';

// Server configuration
$i = 0;
$i++;
$cfg['Servers'][$i]['auth_type'] = 'cookie';
$cfg['Servers'][$i]['host'] = 'localhost';
$cfg['Servers'][$i]['port'] = '3306';
$cfg['Servers'][$i]['compress'] = false;
$cfg['Servers'][$i]['AllowNoPassword'] = true;

// Directories for saving/loading files
$cfg['UploadDir'] = '';
$cfg['SaveDir'] = '';

// Default language
$cfg['DefaultLang'] = 'vi';

// Increase timeout for large imports
$cfg['ExecTimeLimit'] = 600;
