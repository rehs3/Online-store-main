import urllib.request
import sys
import re

urls = [
    'http://127.0.0.1:8000/',
    'http://127.0.0.1:8000/product_detail/1',
    'http://127.0.0.1:8000/product_detail/2',
    'http://127.0.0.1:8000/cart/',
    'http://127.0.0.1:8000/orders/',
    'http://127.0.0.1:8000/account/login/',
]

patterns = {
    'cyrillic': re.compile(r'[\u0400-\u04FF]'),
    'english_words': re.compile(r'\b(Detail|Price|Cart|In stock|Out of stock|Login|Register)\b', re.I),
}

for url in urls:
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            html = r.read().decode('utf-8', errors='ignore')
            status = r.getcode()
    except Exception as e:
        print(f'{url} -> ERROR: {e}')
        continue

    findings = {}
    findings['cyrillic'] = bool(patterns['cyrillic'].search(html))
    findings['english_words'] = bool(patterns['english_words'].search(html))

    print(
        f'URL: {url}  STATUS: {status}  Cyrillic present: {findings["cyrillic"]}  English words present: {findings["english_words"]}')

    # show small excerpt where english words or cyrillic found
    if findings['cyrillic'] or findings['english_words']:
        excerpt = ''
        if findings['cyrillic']:
            m = patterns['cyrillic'].search(html)
            i = m.start()
            excerpt = html[max(0, i-60):i+60]
        else:
            m = patterns['english_words'].search(html)
            i = m.start()
            excerpt = html[max(0, i-60):i+60]
        excerpt = excerpt.replace('\n', ' ')
        print('  Excerpt:', excerpt)

print('Check completed')
