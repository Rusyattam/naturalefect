"""
1. site-1: заполнить assets/ из shared/ + исправить пути ../shared/ -> ./assets/
2. site-2: уже готов (self-contained), просто проверим
3. Удалить shared/ (больше не нужна)
"""
import os, re, shutil, urllib.request

PROJECT = r'c:\Users\Windows 11\Desktop\test\project_1to1_checked\project'
SITE1   = os.path.join(PROJECT, 'site-1')
SITE2   = os.path.join(PROJECT, 'site-2')
SHARED  = os.path.join(PROJECT, 'shared', 'assets')

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read()

# ─────────────────────────────────────────────
# 1. Скачать свежий HTML для site-1
# ─────────────────────────────────────────────
print("=== Step 1: Download fresh site-1 HTML ===")
SITE1_URL = 'https://dexxpress.uz/Snake.3-4/'  # тот же оригинал — исправим ниже
# Но site-1 — это другой URL. Читаем downloaded_target_index.html
SRC_HTML = r'c:\Users\Windows 11\Desktop\test\project_1to1_checked\downloaded_target_index.html'
if os.path.exists(SRC_HTML):
    with open(SRC_HTML, encoding='utf-8', errors='replace') as f:
        html1 = f.read()
    print(f"  Loaded from downloaded_target_index.html: {len(html1)} bytes")
else:
    # Читаем текущий index.html
    with open(os.path.join(SITE1, 'index.html'), encoding='utf-8', errors='replace') as f:
        html1 = f.read()
    print(f"  Loaded current index.html: {len(html1)} bytes")

# ─────────────────────────────────────────────
# 2. Применить правки к site-1 HTML
# ─────────────────────────────────────────────
print("\n=== Step 2: Patch site-1 HTML ===")

html = html1

# Убираем base tag абсолютный
html = re.sub(r'<base\s+href=["\'][^.][^"\']*["\']>', '', html, flags=re.I)

# Убираем fcm_pre.js
html = re.sub(r"const\s*\{\s*setup\s*\}\s*=\s*await\s*import\(['\"][^'\"]*fcm_pre[^'\"]*['\"]\);", "// fcm_pre skipped", html)
html = html.replace("const { setup } = await import('/fcm_pre.js?v=2901_1');", "// fcm_pre skipped")

# Убираем onload трюки
html = html.replace("onload=\"this.rel='stylesheet'\"", "")
html = html.replace("onload=\"this.rel=&#39;stylesheet&#39;\"", "")
html = html.replace('as="style"', "")

# jQuery → локальный
html = html.replace('https://code.jquery.com/jquery-2.2.4.min.js', './assets/jquery-2.2.4.min.js')

# Исправляем base64 изображения
html = re.sub(
    r'<img\s+class="order__img"[^>]*src="data:image/[^"]+"',
    '<img class="order__img" loading="lazy" alt="Маҳсулот сурати" src="./assets/kristall.jpg"',
    html
)

# Исправляем двойные кавычки
html = html.replace('src="./assets/sandiq.webp""', 'src="./assets/sandiq.webp"')

# ГЛАВНОЕ: заменяем ../shared/assets/ → ./assets/
html = html.replace('../shared/assets/', './assets/')
html = html.replace('../shared/', './assets/')

# Проверяем
remaining = html.count('../shared/')
print(f"  ../shared/ refs remaining: {remaining}")
print(f"  HTML size: {len(html)} bytes")

with open(os.path.join(SITE1, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(html)
print("  Saved site-1/index.html")

# ─────────────────────────────────────────────
# 3. Заполнить site-1/assets/ из shared/
# ─────────────────────────────────────────────
print("\n=== Step 3: Populate site-1/assets/ from shared/ ===")
assets1 = os.path.join(SITE1, 'assets')
os.makedirs(assets1, exist_ok=True)

# Копируем все из shared/assets/
for fname in os.listdir(SHARED):
    src = os.path.join(SHARED, fname)
    dst = os.path.join(assets1, fname)
    if os.path.isfile(src) and not os.path.exists(dst):
        shutil.copy2(src, dst)
        print(f"  Copied: {fname}")
    elif os.path.isfile(src) and os.path.exists(dst):
        print(f"  Exists: {fname}")

# Копируем fonts/
fonts_src = os.path.join(SHARED, 'fonts')
fonts_dst = os.path.join(assets1, 'fonts')
if os.path.exists(fonts_src) and not os.path.exists(fonts_dst):
    shutil.copytree(fonts_src, fonts_dst)
    print("  Copied: fonts/")

# ─────────────────────────────────────────────
# 4. Удалить shared/ (больше не нужна)
# ─────────────────────────────────────────────
print("\n=== Step 4: Remove shared/ folder ===")
shared_root = os.path.join(PROJECT, 'shared')
if os.path.exists(shared_root):
    shutil.rmtree(shared_root)
    print("  Deleted shared/")

# ─────────────────────────────────────────────
# 5. Итог
# ─────────────────────────────────────────────
print("\n=== Summary ===")
for site in ['site-1', 'site-2', 'site-test']:
    path = os.path.join(PROJECT, site)
    if os.path.exists(path):
        count = sum(len(f) for _, _, f in os.walk(path))
        size  = sum(os.path.getsize(os.path.join(r, f)) for r, _, files in os.walk(path) for f in files)
        print(f"  {site}: {count} files, {round(size/1024, 1)} KB")

print("\nDone!")

