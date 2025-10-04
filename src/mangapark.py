# Mangayomi Extension
# name: AsuraScans
# lang: en
# type: manga
# version: 1

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


BASE = 'https://v2.mangapark.net'
headers = {'User-Agent': 'Mangayomi-Converter/1.0'}




def _get_soup(url):
r = requests.get(url, headers=headers, timeout=15)
r.raise_for_status()
return BeautifulSoup(r.text, 'html.parser')




def search(query, page=1):
q = requests.utils.requote_uri(query)
url = f"{BASE}/search?word={q}&page={page}"
soup = _get_soup(url)
results = []
for it in soup.select('.item'): # adjusted for MangaPark v2 layout
a = it.select_one('a.cover')
if not a:
continue
link = urljoin(BASE, a['href'])
title = it.select_one('.title').get_text(strip=True) if it.select_one('.title') else a.get('title', '')
thumb = it.select_one('img').get('src') if it.select_one('img') else None
results.append({'id': link, 'title': title, 'url': link, 'thumbnail': thumb})
return results




def get_popular(page=1):
url = f"{BASE}/browse?sort=rating&page={page}"
soup = _get_soup(url)
results = []
for it in soup.select('.item'):
a = it.select_one('a.cover')
if not a:
continue
link = urljoin(BASE, a['href'])
title = it.select_one('.title').get_text(strip=True) if it.select_one('.title') else a.get('title', '')
thumb = it.select_one('img').get('src') if it.select_one('img') else None
results.append({'id': link, 'title': title, 'url': link, 'thumbnail': thumb})
return results




def get_manga_details(manga_url):
soup = _get_soup(manga_url)
title = soup.select_one('h3.manga-name').get_text(strip=True) if soup.select_one('h3.manga-name') else ''
thumb = soup.select_one('.cover img').get('src') if soup.select_one('.cover img') else None
info = {
'title': title,
'author': '',
'artist': '',
'description': '',
'genres': [],
'status': '',
'thumbnail': thumb,
}
desc = soup.select_one('.summary')
if desc:
info['description'] = desc.get_text('\n', strip=True)
info['genres'] = [g.get_text(strip=True) for g in soup.select('.genres a')]
return info




def get_chapters(manga_url):
soup = _get_soup(manga_url)
chapters = []
for a in soup.select('ul.chapter-list a'):
name = a.get_text(strip=True)
link = urljoin(BASE, a['href'])
chapters.append({'id': link, 'name': name, 'url': link, 'date': ''})
return chapters




def get_pages(chapter_url):
soup = _get_soup(chapter_url)
pages = []
for img in soup.select('.img-container img'):
src = img.get('data-src') or img.get('src')
if src:
pages.append(src)
return pages
