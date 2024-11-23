# <여론M>에서 2022년 대선 여론조사 결과 HTML을 Selenium을 이용해 가져오는 코드입니다.
# 페이지가 동적으로 구성되었으므로, Selenium을 이용해 렌더링된 HTML을 그대로 다운 받았습니다. 

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

url = "https://poll-mbc.co.kr/bk/2022_president.html"
file_name = "2022_president.html"

headers = {'accept': '*/*',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53',
           'Accept-Language': 'en-US,en;q=0.9,it;q=0.8,es;q=0.7',
           'referer': 'https://www.google.com/'}
chrome_options = Options()

def main():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    print("the setting is done!")
    
    driver.get(url)
    html_text = driver.page_source
    with open(file_name, 'w', encoding="utf-8") as f:
        f.write(html_text)

    driver.close()

if __name__ == '__main__':
    main()
