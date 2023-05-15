import json
import requests
from bs4 import BeautifulSoup
import re
from classes import Article


def get_article(target_url=str):
    """
    Crawlt den übergebenen String (Webseite), extrahiert die gewünschten Daten & Metadaten (Datum, Uhrzeit, Titel, Untertitel, Inhalt, Autor:in(nen), URL) des Artikels und gibt sie als `Article`-Objekt zurück
    
    Args:
        target_url (str): Webadresse des zu verarbeitenden Artikels
        
    Returns: Objekt der Klasse `Article`(`date`, `time`, `title`, `subtitle`, `body`, `author`, `url`)
    """
    
    raw = requests.get(target_url)
    raw_soup = BeautifulSoup(raw.content, "html.parser")
    
    og_url = str(raw_soup.find('meta',attrs={'property': 'og:url'})).split('"')[1]

    r = requests.get(og_url)
    soup = BeautifulSoup(r.content, "html.parser")

    try:
        author = str(soup.find('meta',attrs={'name': 'author'})).split('"')[1]
    except:
        author = 'N/A (Agenturmeldung)'
        
        
    title = str(soup.find('meta',attrs={'property': 'og:title'})).split('"')[1]
    title = re.sub(r'&amp;', '&', title)
    
    try:
        subtitle = str(soup.find('meta',attrs={'property': 'og:description'})).split('"')[1]
        subtitle = re.sub(r'&amp;', '&', subtitle)
    except:
        subtitle = 'NONE'

    article_tags = []
    script = soup.find_all('script',type='application/javascript')[3].text.strip()
    script_split_tags = script.split(f',"breadcrumbs":[')[1]
    script_split_tags_dict = script_split_tags.split(f'],"canonicalUrl":"')[0]
    cat_data = json.loads(script_split_tags_dict)
    cat_data_canon = cat_data['href'].split('/')
    
    for i in range(1,len(cat_data_canon)):
        article_tags.append(cat_data_canon[i].lower())
        
    article_tags.append(cat_data['title'].lower())    
    article_tags = [*set(article_tags)]
                
    script_split = script.split(f',"elements":')
       
    script_body = script_split[1].split('],"headline":')[0] + ']'
                 
    data = json.loads(script_body)

    body = []
    
    for _ in data:
        if _['type'] == 'text' or _['type'] == 'header':
            if('Laden Sie sich jetzt hier kostenfrei unsere neue LVZ-App herunter' in _['text'] or 'Lesen Sie auch' in _['text'] or 'LVZ+ gratis' in _['text'] or 'Für iOS' in _['text'] or 'Für Android' in _['text']):
                pass
            elif '<a href=' in _['text'] or '<strong>' in _['text'] or '&nbsp;' in _['text'] or '<b>' in _['text'] or '</b>' in _['text'] or '<br/>' in _['text'] or '<em>' in _['text'] or '<b style=' in _['text'] or '&amp;' in _['text'] or '<i>' in _['text'] or '</i>' in _['text']:
                text = re.sub(r'(<a href="\S+)">', '', _['text'])
                text = re.sub(r'<a href="\S+"', '', text)
                text = re.sub(r'target="_blank">', '', text)
                text = re.sub(r'target="_self">', '', text)
                text = re.sub(r'</a>$', '', text)
                text = re.sub(r'</a>', ' ', text)
                text = re.sub(r'<strong>', '', text)
                text = re.sub(r'</strong>$\S', ' ', text)
                text = re.sub(r'</strong>', '', text)
                text = re.sub(r'&nbsp;\d\d', '', text)
                text = re.sub(r'&nbsp;', '', text)
                text = re.sub(r'^(<b style="[\s\S]+)">', '', text)
                text = re.sub(r'(<b style="[\s\S]+)">', ' ', text)
                text = re.sub(r'^<b>', '', text)
                text = re.sub(r'<b>', ' ', text)
                text = re.sub(r'</b>$\S', ' ', text)
                text = re.sub(r'<b>', '', text)
                text = re.sub(r'</b>', '', text)
                text = re.sub(r'<br/>', '', text)
                text = re.sub(r'<em>', '', text)
                text = re.sub(r'</i>$', '', text)
                text = re.sub(r'<i>', '', text)
                text = re.sub(r'&amp;', '&', text)
                text = re.sub(r'„', '"', text)
                text = re.sub(r'“', '"', text)
                text = re.sub(r'\s{2,10}', ' ', text) #entferne alle evtl. entstandenen mehrfache Leerzeichen!
                body.append(text)
            else:
                body.append(_['text'])
        
    script_meta = script_split[0].split(';Fusion.globalContent=')[1] + '}'
        
    meta_data = json.loads(script_meta)   
    raw_date = meta_data['displayDate']

    article_date = f'{raw_date[8:10]}.{raw_date[5:7]}.{raw_date[0:4]}'
    article_time = f'{raw_date[11:16]} Uhr'
    
    return Article(article_date, article_time, title, subtitle, body, author, og_url, article_tags)