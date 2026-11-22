# Собирает portfolio.html из index.html: шапка, стили, скрипты и контакты общие
import re, html
s = open('index.html').read()
boats = re.findall(r'<article class="boat" data-photos="([^"]+)">.*?<h3>(.*?)</h3>\s*<p>(.*?)</p>', s, re.S)

head_end = s.index('<main>')
head = s[:head_end]
head = head.replace('<title>Tuning Boat Service Surgut — тюнинг лодок и катеров в Сургуте</title>',
                    '<title>Портфолио — Tuning Boat Service Surgut</title>')
head = head.replace('<a href="#works">Работы</a>', '<a href="index.html#works">Работы</a>')
head = head.replace('<a href="portfolio.html">Портфолио</a>', '<a href="portfolio.html" class="is-active" aria-current="page">Портфолио</a>')
head = head.replace('<a href="#top" class="logo"', '<a href="index.html" class="logo"')

nav = ''.join('        <a href="#boat-%d">%s</a>\n' % (i + 1, h3) for i, (_, h3, _) in enumerate(boats))
secs = ''
for i, (photos, h3, p) in enumerate(boats):
    lst = photos.split(',')
    alt = html.unescape(h3).replace('\xa0', ' ')
    btns = ''.join('          <button type="button" data-index="%d" aria-label="Открыть фото %d"><img src="%s" alt="%s, фото %d" loading="lazy" width="640" height="480"></button>\n'
                   % (j, j + 1, f.replace('.jpg', '-thumb.jpg'), alt, j + 1) for j, f in enumerate(lst))
    secs += '''      <section class="pf-boat" id="boat-%d" data-photos="%s">
        <span class="pf-boat__count">%d&nbsp;фото</span>
        <h2>%s</h2>
        <p>%s</p>
        <div class="pf-grid">
%s        </div>
      </section>
''' % (i + 1, photos, len(lst), h3, p, btns)

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
