import requests
from bs4 import BeautifulSoup
import time

def crawl():
    base_url = "https://quotes.toscrape.com"
    current_page = "/"
    pages_content = {}

    while current_page:
        print(f"Crawling: {base_url}{current_page}")
        try:
            # 增加 timeout 防止程序死锁，设置 headers 模拟浏览器访问
            response = requests.get(
                base_url + current_page, 
                timeout=10, 
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            # 如果返回 4xx 或 5xx 状态码，直接抛出异常进入 except
            response.raise_for_status() 
            
        except requests.exceptions.RequestException as e:
            print(f"Network error occurred: {e}")
            # 如果某一页爬取失败，跳出循环保护已抓取的数据
            break
            
        soup = BeautifulSoup(response.text, 'html.parser')
        pages_content[current_page] = soup.get_text()
        
        next_tag = soup.select_one('li.next a')
        current_page = next_tag['href'] if next_tag else None
        
        if current_page:
            # 严格遵守 6 秒礼貌窗口 [cite: 17, 144]
            time.sleep(6) 
            
    return pages_content