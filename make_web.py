# 從 app 的 index.html 產生網頁版（docs/ 資料夾，給 GitHub Pages 用）
# 用法：python3 make_web.py
# 每次改完 app/src/main/assets/index.html 後執行一次，再一起上傳。
from pathlib import Path
from PIL import Image, ImageDraw
import json, hashlib

ROOT = Path(__file__).parent
SRC = ROOT / 'app/src/main/assets/index.html'
OUT = ROOT / 'docs'
OUT.mkdir(exist_ok=True)
html = SRC.read_text(encoding='utf-8')
ver = hashlib.sha1(html.encode()).hexdigest()[:10]

HEAD = '''<link rel="manifest" href="manifest.webmanifest">
<meta name="theme-color" content="#0a0a0a">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="健身紀錄">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="icon" href="icon-192.png">
<style>
  #a2hs{position:fixed;left:12px;right:12px;bottom:calc(88px + env(safe-area-inset-bottom));z-index:70;background:#202020;border:1px solid rgba(255,255,255,.08);
    border-radius:22px;padding:14px 44px 14px 16px;color:#fff;font-size:13.5px;line-height:1.6;box-shadow:0 18px 40px rgba(0,0,0,.6)}
  #a2hs b{color:#c6f432}
  #a2hs button{position:absolute;right:10px;top:10px;width:28px;height:28px;border-radius:50%;border:1px solid rgba(255,255,255,.2);background:transparent;color:#fff;cursor:pointer}
</style>
'''
TAIL = '''<script>
(() => {
  // 離線也能打開：註冊 service worker
  if ('serviceWorker' in navigator) navigator.serviceWorker.register('sw.js').catch(() => {});
  // iPhone 用 Safari 開、還沒加到主畫面時，提示加到主畫面（資料才會一直保留）
  const ios = /iphone|ipad|ipod/i.test(navigator.userAgent), standalone = navigator.standalone || matchMedia('(display-mode: standalone)').matches;
  let seen = false; try { seen = localStorage.getItem('a2hs-dismissed') === '1'; } catch (e) {}
  if (ios && !standalone && !seen) {
    const d = document.createElement('div'); d.id = 'a2hs';
    d.innerHTML = '請點 Safari 下方的 <b>分享</b> 按鈕，選 <b>加入主畫面</b>，之後從桌面圖示打開。<br>直接在 Safari 裡使用，太久沒打開時資料可能會被清除。<button aria-label="關閉">✕</button>';
    d.querySelector('button').onclick = () => { d.remove(); try { localStorage.setItem('a2hs-dismissed', '1'); } catch (e) {} };
    document.body.appendChild(d);
  }
})();
</script>
'''
html = html.replace('<title>健身紀錄</title>\n', '<title>健身紀錄</title>\n' + HEAD, 1)
html = html.replace('</body>', TAIL + '</body>', 1)
(OUT / 'index.html').write_text(html, encoding='utf-8')

# 圖示：沿用 app 的啞鈴圖示，加黑底
fg = Image.open(ROOT / 'app/src/main/res/mipmap-xxxhdpi/ic_launcher_foreground.png').convert('RGBA')
for size in (180, 192, 512):
    im = Image.new('RGBA', fg.size, (0, 0, 0, 255)); im.alpha_composite(fg)
    im.resize((size, size), Image.LANCZOS).convert('RGB').save(OUT / f'icon-{size}.png')

(OUT / 'manifest.webmanifest').write_text(json.dumps({
    'name': '健身紀錄', 'short_name': '健身紀錄', 'lang': 'zh-Hant',
    'start_url': './', 'scope': './', 'display': 'standalone',
    'background_color': '#0a0a0a', 'theme_color': '#0a0a0a',
    'icons': [
        {'src': 'icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
        {'src': 'icon-512.png', 'sizes': '512x512', 'type': 'image/png'},
        {'src': 'icon-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'},
    ]}, ensure_ascii=False, indent=2), encoding='utf-8')

# 先抓網路上的新版，沒網路時用快取（所以更新會自動生效，也能離線開）
(OUT / 'sw.js').write_text(f'''const CACHE = 'gymlog-{ver}';
const FILES = ['./', 'index.html', 'manifest.webmanifest', 'icon-180.png', 'icon-192.png', 'icon-512.png'];
self.addEventListener('install', e => {{ e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES))); self.skipWaiting(); }});
self.addEventListener('activate', e => {{ e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))); self.clients.claim(); }});
self.addEventListener('fetch', e => {{
  if (e.request.method !== 'GET') return;
  e.respondWith(fetch(e.request).then(r => {{ const c = r.clone(); caches.open(CACHE).then(x => x.put(e.request, c)); return r; }})
    .catch(() => caches.match(e.request, {{ ignoreSearch: true }}).then(r => r || caches.match('index.html'))));
}});
''', encoding='utf-8')
(OUT / '.nojekyll').write_text('')
print('docs/ 產生完成，版本', ver)
