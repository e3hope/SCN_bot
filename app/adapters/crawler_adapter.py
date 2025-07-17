import httpx
from bs4 import BeautifulSoup

class CrawlerAdapter:
    @staticmethod
    
    def crawl(url: str, keyword: str = None) -> list:
        response = httpx.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.find_all('table', class_=['bd_lst', 'bd_tb_lst', 'bd_tb'])
        results = []
        for table in tables:
            tds = table.find_all('td', class_='title hotdeal_var8')
            for td in tds:
                a_tag = td.find('a')
                if a_tag and a_tag.has_attr('href'):
                    title = a_tag.get_text(strip=True)
                    href = a_tag['href']
                    # 절대경로/상대경로 모두 처리
                    if href.startswith('/'):
                        link = f"https://www.fmkorea.com{href}"
                    else:
                        link = href
                    if keyword is None or keyword in title:
                        results.append({'title': title, 'link': link})
        return results

if __name__ == "__main__":
    url = "https://www.fmkorea.com/football_news"  # 테스트할 URL
    result = CrawlerAdapter.crawl(url)
    print(result)

