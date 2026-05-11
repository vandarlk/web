import requests
from bs4 import BeautifulSoup
import time

def crawl():
    base_url = "https://quotes.toscrape.com"
    current_page = "/"
    pages_content = {}

    while current_page:
        print(f"Crawling: {base_url}{current_page}")
        response = requests.get(base_url + current_page)
        
        if response.status_code != 200:
            break
            
        soup = BeautifulSoup(response.text, 'html.parser')
        # 提取当前页的所有文字并去重
        pages_content[current_page] = soup.get_text()
        
        # 寻找下一页
        next_tag = soup.select_one('li.next a')
        current_page = next_tag['href'] if next_tag else None
        
        if current_page:
            time.sleep(6) # 必须遵守 6 秒礼貌窗口 [cite: 17]
            
    return pages_content
