import os
import shutil
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE1 = os.path.join(ROOT, 'project', 'site-1')
SITE2 = os.path.join(ROOT, 'project', 'site-2')

print(f"ROOT: {ROOT}")

# 1. Copy jquery-2.2.4.min.js
jq_source = os.path.join(ROOT, 'project', 'site-test', 'assets', '_mirror', 'code.jquery.com', 'jquery-2.2.4.min.js')
if not os.path.exists(jq_source):
    # Try finding it in site-1 or site-2 mirror
    jq_source = os.path.join(SITE1, 'assets', '_mirror', 'code.jquery.com', 'jquery-2.2.4.min.js')
if not os.path.exists(jq_source):
    jq_source = os.path.join(SITE2, 'assets', '_mirror', 'code.jquery.com', 'jquery-2.2.4.min.js')

if os.path.exists(jq_source):
    shutil.copyfile(jq_source, os.path.join(SITE1, 'assets', 'jquery-2.2.4.min.js'))
    shutil.copyfile(jq_source, os.path.join(SITE2, 'assets', 'jquery-2.2.4.min.js'))
    print("Copied jquery-2.2.4.min.js to site-1 and site-2 assets")

# 2. Setup site-1
# Ensure 00.jpg exists
kristall1 = os.path.join(SITE1, 'assets', 'kristall.jpg')
if os.path.exists(kristall1):
    shutil.copyfile(kristall1, os.path.join(SITE1, 'assets', '00.jpg'))
    print("Created 00.jpg in site-1/assets from kristall.jpg")

# Copy real style.css to root of site-1 as well
real_style1 = os.path.join(SITE1, 'assets', 'style.css')
if os.path.exists(real_style1):
    shutil.copyfile(real_style1, os.path.join(SITE1, 'style.css'))
    print("Updated site-1/style.css with real stylesheet")

# 3. Setup site-2 assets
# Copy all mirrored assets from dexxpress.uz/Snake.1.1-4/assets to site-2/assets
mirror_s2_dir = os.path.join(SITE2, 'assets', '_mirror', 'dexxpress.uz', 'Snake.1.1-4', 'assets')
if os.path.exists(mirror_s2_dir):
    for f in os.listdir(mirror_s2_dir):
        src_path = os.path.join(mirror_s2_dir, f)
        dst_path = os.path.join(SITE2, 'assets', f)
        if os.path.isfile(src_path):
            shutil.copyfile(src_path, dst_path)
    print("Copied all mirrored assets to site-2/assets")

# Remove placeholder SVGs in site-2/assets
for f in os.listdir(os.path.join(SITE2, 'assets')):
    if f.endswith('.svg') and not f.startswith('cpa_'):
        fpath = os.path.join(SITE2, 'assets', f)
        if os.path.getsize(fpath) < 500: # placeholder svg
            os.remove(fpath)
print("Cleaned placeholder SVGs in site-2/assets")

# Copy fonts and roboto.css from site-1 to site-2
fonts_s1 = os.path.join(SITE1, 'assets', 'fonts')
fonts_s2 = os.path.join(SITE2, 'assets', 'fonts')
if os.path.exists(fonts_s1):
    if os.path.exists(fonts_s2):
        shutil.rmtree(fonts_s2)
    shutil.copytree(fonts_s1, fonts_s2)
    print("Copied fonts directory to site-2/assets/fonts")

roboto_s1 = os.path.join(SITE1, 'assets', 'roboto.css')
roboto_s2 = os.path.join(SITE2, 'assets', 'roboto.css')
if os.path.exists(roboto_s1):
    shutil.copyfile(roboto_s1, roboto_s2)
    print("Copied roboto.css to site-2/assets")

kristall2 = os.path.join(SITE2, 'assets', 'kristall.jpg')
if os.path.exists(kristall2):
    shutil.copyfile(kristall2, os.path.join(SITE2, 'assets', '00.jpg'))
    print("Created 00.jpg in site-2/assets from kristall.jpg")

real_style2 = os.path.join(SITE2, 'assets', 'style.css')
if os.path.exists(real_style2):
    shutil.copyfile(real_style2, os.path.join(SITE2, 'style.css'))
    print("Updated site-2/style.css with real stylesheet")

# 4. Helper function to sanitize HTML
def sanitize_html(html_str):
    # Remove base tag
    html = re.sub(r'<base\b[^>]*>', '', html_str, flags=re.I)
    
    # Fix double quote typo on sandiq.webp
    html = html.replace('src="./assets/sandiq.webp""', 'src="./assets/sandiq.webp"')
    
    # Ensure clean stylesheet links (synchronous loading so styles render immediately)
    html = html.replace("onload=\"this.rel='stylesheet'\"", "")
    html = html.replace("onload=\"this.rel=&#39;stylesheet&#39;\"", "")
    html = html.replace('as="style"', "")
    
    # Point jQuery fallback to local jquery-2.2.4.min.js
    html = html.replace('https://code.jquery.com/jquery-2.2.4.min.js', './assets/jquery-2.2.4.min.js')
    
    # Remove/skip fcm_pre.js import
    html = re.sub(r"const\s*\{\s*setup\s*\}\s*=\s*await\s*import\(['\"]/fcm_pre\.js[^'\"]*['\"]\);", "// fcm_pre skipped", html)
    
    # Fix base64 thumbnail in order__img to kristall.jpg
    html = re.sub(r'<img\s+class="order__img"[^>]*src="data:image/[^"]+"', '<img class="order__img" loading="lazy" alt="Маҳсулот сурати" src="./assets/kristall.jpg"', html)

    return html

# 5. Process site-1/index.html
with open(os.path.join(ROOT, 'downloaded_target_index.html'), encoding='utf-8') as f:
    html1 = f.read()

clean_html1 = sanitize_html(html1)
with open(os.path.join(SITE1, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(clean_html1)
print(f"Written {len(clean_html1)} bytes to site-1/index.html")

# 6. Process site-2/index.html
with open(os.path.join(ROOT, 'downloaded_target_snake1.html'), encoding='utf-8') as f:
    html2 = f.read()

clean_html2 = sanitize_html(html2)
with open(os.path.join(SITE2, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(clean_html2)
print(f"Written {len(clean_html2)} bytes to site-2/index.html")

