import requests
from classes import Article
import urllib.parse

from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('API_TOKEN')
API_KEY_NAME = os.getenv('API_TOKEN_NAME')

# apiPath = 'http://127.0.0.1:8000/get_article' #(local testing)
apiPath = 'https://lps.uber.space/get_article'

targetUrl = 'https://www.lvz.de/wissen/nabu-stunde-der-gartenvoegel-am-wochenende-wo-und-bis-wann-voegel-gemeldet-werden-koennen-GEX7QOVMURIWRHF6N5BPGDLLZY.html'
targetUrlEncoded = urllib.parse.quote(targetUrl, safe="")

reqPath = apiPath+'?'+API_KEY_NAME+'='+API_KEY+'&url='+targetUrlEncoded

resp = requests.get(reqPath)
respJson = resp.json()

if resp.ok == False:
    print(f"""Fehler!
          
Statuscode: {resp.status_code} [{resp.reason}] - {respJson['detail']}
          """)
    if resp.status_code == 403:
        print("Überprüfe den API Key!")
elif resp.status_code == 200:   
    art = Article(respJson['date'],respJson['time'],respJson['title'].strip(),respJson['subtitle'].strip(),respJson['content'],respJson['author'],respJson['url'],respJson['tags'])

    print(f"""{art.title}
{art.subtitle}

{art.author}
{art.pub_date_and_time()}

{art.body}

[{art.url}]""")
else:
    print(f"""Request beendet!

Response:          
Statuscode: {resp.status_code} [{resp.reason}] - {respJson['detail']}
          """)