# Mangayomi Extension
# name: AsuraScans
# lang: en
# type: manga
# version: 1

import requests
    r.raise_for_status()
    return BeautifulSoup(r.text, 'html.parser')




def search(query, page=1):
    q = requests.utils.requote_uri(query)
    url = f"{BASE}/?s={q}&post_type=wp-manga&page={page}"
    soup = _get_soup(url)
    results = []
    for card in soup.select('.c-tabs-item__content'):
        a = card.select_one('h3 a')
        if not a:
            continue
        title = a.get_text(strip=True)
        link = a['href']
        thumb = card.select_one('img') and card.select_one('img').get('data-src') or None
        results.append({'id': link, 'title': title, 'url': link, 'thumbnail': thumb})
    return results




def get_popular(page=1):
    url = f"{BASE}/manga/?page={page}"
    soup = _get_soup(url)
    results = []
    for item in soup.select('.c-image-hover a'):
        link = item['href']
        title = item.get('title', '') or item.get_text(strip=True)
        thumb = item.select_one('img') and item.select_one('img').get('data-src') or None
        results.append({'id': link, 'title': title, 'url': link, 'thumbnail': thumb})
    return results




def get_manga_details(manga_url):
    soup = _get_soup(manga_url)
    title = soup.select_one('.post-title h1').get_text(strip=True) if soup.select_one('.post-title h1') else ''
    thumb = soup.select_one('.summary_image img') and soup.select_one('.summary_image img').get('data-src') or None
    info = {
        'title': title,
        'author': '',
        'artist': '',
        'description': '',
        'genres': [],
        'status': '',
        'thumbnail': thumb,
    }
    desc = soup.select_one('.summary__content')
    if desc:
        info['description'] = desc.get_text('\n', strip=True)
    for row in soup.select('.post-content_item'):
        heading = row.select_one('.summary-heading')
        if not heading:
            continue
        key = heading.get_text(strip=True).lower()
        val = row.select_one('.summary-content') and row.select_one('.summary-content').get_text(', ', strip=True) or ''
        if 'author' in key:
            info['author'] = val
        if 'artist' in key:
            info['artist'] = val
        if 'status' in key:
            info['status'] = val
        if 'genres' in key:
            info['genres'] = [g.strip() for g in val.split(',')]
    return info




def get_chapters(manga_url):
    soup = _get_soup(manga_url)
    chapters = []
    for a in soup.select('.wp-manga-chapter a'):
        name = a.get_text(strip=True)
        link = a['href']
        chapters.append({'id': link, 'name': name, 'url': link, 'date': ''})
    return chapters




def get_pages(chapter_url):
    soup = _get_soup(chapter_url)
    pages = []
    for img in soup.select('.reading-content img'):
        src = img.get('data-src') or img.get('src')
        if src:
            pages.append(src)
    return pages
