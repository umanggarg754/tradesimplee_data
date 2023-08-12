import selenium 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time,os,sys
import pandas as pd
import numpy as np
import logging,re
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import urllib.parse



def get_driver():

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-extensions")

    # PROXY = f"socks5://127.0.0.1:{TOR_PORT}"
    if os.getenv('USE_TOR')=='1':
        logging.info("using tor browser")
        webdriver.DesiredCapabilities.CHROME['proxy'] = {
            "httpProxy": PROXY,
            "ftpProxy": PROXY,
            "sslProxy": PROXY,
            "proxyType": "MANUAL",
        }
        webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True
        # options.add_argument("--proxy-server=)
        # chrome_options.add_argument('--proxy-server=%s' % PROXY)
    else:
        logging.info("skipping tor browser")
    options.add_argument('window-size=1920,1080')
    options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36')
    options.add_argument('accept=text/html,application/xhtml+xml,application/xml;q=0.9,'
                         'image/webp,image/apng,*/*;q=0.8')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    # driver = webdriver.Chrome( chrome_options=options)
    return driver



def get_page_phone(name):
    try:
        name = name 
        safe_string = urllib.parse.quote_plus(name)
        driver = get_driver()
        print(safe_string)
        url = f'https://www.google.co.in/search?q={safe_string}+karanataka+india+phone+number'
        print(url)
        driver.get(url)
        # time.sleep(2)
        # html_source = driver.page_source
        # print(html_source)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.kno-result.JEPF1b.kno-kp.g-blk')))
        element = driver.find_element(By.CSS_SELECTOR, 'div.kno-result.JEPF1b.kno-kp.g-blk') # class="osrp-blk"
        phone = element.text.split("\n")
        # phone =  re.search(r'Phone: (.*?)\n', element.text).group(1)
        print(phone)
        return phone[0]
    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':

    file = sys.argv[1]
    data = pd.read_excel(file)
    ans = []
    for i , row in data.iterrows():
        name = row["Name of the Company"]
        print(name)
        result = get_page_phone(name)
        ans.append(result)
        #     break
    
    data['phone'] = ans

    data.to_excel(file,index=False)
    

    
