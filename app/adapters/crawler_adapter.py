import httpx
from bs4 import BeautifulSoup

class CrawlerAdapter:
    @staticmethod
    def crawl(url: str) -> dict:
        response = httpx.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else ''
        content = soup.get_text()
        return {
            'url': url,
            'title': title,
            'content': content
        }
