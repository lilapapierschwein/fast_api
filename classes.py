from datetime import datetime as dt

class Article:
    """Klasse, die Inhalt und Metadaten (`pub_date`, `pub_time`, `title`, `subtitle`, `body`, `author`, `url`) eines gecrawlten Artikels beinhaltet"""
    
    def __init__(self, pub_date, pub_time, title=str, subtitle=str, body=str, author=str, url=str, article_tags=list):
        self.title = title
        self.subtitle = subtitle
        self.pub_date = pub_date
        self.pub_time = pub_time
        self.body = body
        self.author = author
        self.url = url
        self.article_tags = article_tags
        
    def pub_date_and_time(self):
        """Formatiert Datum und Uhrzeit und gibt die als einen String im Format `Datum | Uhrzeit` zurück"""
        
        return f'{self.pub_date} | {self.pub_time}'

    def make_pub_timestamp(self):
        return dt(year=int(self.pub_date[6:]),month=int(self.pub_date[3:5]),day=int(self.pub_date[:2]),hour=int(self.pub_time[:2]),minute=int(self.pub_time[3:5]))
    
    
    def body_as_one(self):
        """Fügt alle Teile `body` (Textabschnitte & Teilüberschriften) des Artikelinhalts zusammen und gibt sie als einen String zurück."""
        
        one_body = ''
        
        for _ in self.body:
            one_body += f'{_}\n\n'
                    
        return one_body.strip()
    
    
    def tags_as_string(self):
        return " , ".join(self.article_tags)
    
    
    def to_dict(self):
        articleDict = {
            'title': self.title,
            'subtitle': self.subtitle,
            'pub_date': self.pub_date,
            'pub_time': self.pub_time,
            'body': self.body_as_one(),
            'author': self.author,
            'url': self.url,
            'tags': self.article_tags
        }
        return articleDict