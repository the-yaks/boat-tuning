# Собирает portfolio.html из index.html: шапка, стили, скрипты и контакты общие
import re, html
s = open('index.html').read()
boats = re.findall(r'<article class="boat" data-photos="([^"]+)">.*?<h3>(.*?)</h3>\s*<p>(.*?)</p>', s, re.S)
# Лодки только для портфолио (на главной их нет)
import json, os
extra_path = os.path.join(os.path.dirname(__file__), 'portfolio_extra.json')
if os.path.exists(extra_path):
    for b in json.load(open(extra_path)):
        boats.append((','.join(b['photos']), b['title'], b['desc']))

head_end = s.index('<main>')
head = s[:head_end]
head = head.replace('<title>Tuning Boat Service Surgut — тюнинг лодок и катеров в Сургуте</title>',
                    '<title>Портфолио — Tuning Boat Service Surgut</title>')
head = head.replace('<a href="#works">Работы</a>', '<a href="index.html#works">Работы</a>')
head = head.replace('<a href="#workshop">Мастерская</a>', '<a href="index.html#workshop">Мастерская</a>')
head = head.replace('<a href="#services">Услуги</a>', '<a href="index.html#services">Услуги</a>')
head = head.replace('<a href="portfolio.html">Портфолио</a>', '<a href="portfolio.html" class="is-active" aria-current="page">Портфолио</a>')
head = head.replace('<link rel="canonical" href="https://boat-service-surgut.ru/">', '<link rel="canonical" href="https://boat-service-surgut.ru/portfolio.html">')
head = head.replace('<meta property="og:url" content="https://boat-service-surgut.ru/">', '<meta property="og:url" content="https://boat-service-surgut.ru/portfolio.html">')
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Портфолио Tuning Boat Service Surgut: фото лодок и катеров после установки эхолотов, электромоторов, проводки и другого оборудования в Сургуте.">', head, count=1)
head = re.sub(r'  <script type="application/ld\+json">.*?</script>\n', '', head, count=1, flags=re.S)
head = head.replace('<a href="#top" class="logo"', '<a href="index.html" class="logo"')

nav = ''.join('        <a href="#boat-%d">%s</a>\n' % (i + 1, h3) for i, (_, h3, _) in enumerate(boats))
secs = ''
for i, (photos, h3, p) in enumerate(boats):
    lst = photos.split(',')
    alt = html.unescape(h3).replace('\xa0', ' ')
    def thumb(f): return re.sub(r'\.(jpg|mp4)$', '-thumb.jpg', f)
    btns = ''
    for j, f in enumerate(lst):
        if f.endswith('.mp4'):
            btns += '          <button type="button" data-index="%d" aria-label="Смотреть видео"><img src="%s" alt="%s, видео" loading="lazy" width="640" height="360"><i class="play" aria-hidden="true"></i></button>\n' % (j, thumb(f), alt)
        else:
            btns += '          <button type="button" data-index="%d" aria-label="Открыть фото %d"><img src="%s" alt="%s, фото %d" loading="lazy" width="640" height="480"></button>\n' % (j, j + 1, thumb(f), alt, j + 1)
    nvid = sum(f.endswith('.mp4') for f in lst)
    count = '%d&nbsp;фото' % (len(lst) - nvid) + (' · %d&nbsp;видео' % nvid if nvid else '')
    secs += '''      <section class="pf-boat" id="boat-%d" data-photos="%s">
        <span class="pf-boat__count">%s</span>
        <h2>%s</h2>
        <p>%s</p>
        <div class="pf-grid">
%s        </div>
      </section>
''' % (i + 1, photos, count, h3, p, btns)

contacts = s[s.index('  <!-- CONTACTS -->'):s.index('</main>')]
main = '''<main>
  <section class="pf-hero">
    <div class="container">
      <p class="eyebrow">Портфолио</p>
      <h1 class="section__title">Наши работы</h1>
      <p>%d&nbsp;лодок и&nbsp;катеров. Нажмите на&nbsp;фото, чтобы открыть его на&nbsp;весь экран</p>
      <nav class="pf-nav" aria-label="Лодки">
%s      </nav>
    </div>
  </section>

  <div class="pf-list">
    <div class="container">
%s    </div>
  </div>

%s</main>''' % (len(boats), nav, secs, contacts)

tail = s[s.index('</main>') + len('</main>'):]
open('portfolio.html', 'w').write(head + main + tail)
print('boats', len(boats))
