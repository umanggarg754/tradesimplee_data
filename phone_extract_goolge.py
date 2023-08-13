
from selenium.webdriver.common.keys import Keys
import time,os,sys
import pandas as pd
import numpy as np
import logging,re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from driver import get_driver
import urllib.parse
import concurrent.futures



def get_page_phone(name):
    try:
        name = name 
        safe_string = urllib.parse.quote_plus(name)
        driver = get_driver()
        print(safe_string)
        url = f'https://www.google.co.in/search?q={safe_string}+india+phone+number'
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
    try:
        data = pd.read_excel(file)
    except Exception as e:
        data = pd.read_csv(file)
    else:
        print("WRong file foramt")

    # ans = []
    # for i , row in data.iterrows():
    #     name = row["name"]
    #     print(name)
    #     result = get_page_phone(name)
    #     ans.append(result)
    #     #     break



    def get_phone_number(name):
        # Replace this with your actual get_page_phone function
        result = get_page_phone(name)
        return result

    # Assuming you have the "data" DataFrame with the "name" column

    ans = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit tasks to the executor for each row
        futures = [executor.submit(get_phone_number, row["name"]) for _, row in data.iterrows()]

        # Retrieve results as they become available
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            ans.append(result)

    
    data['phone'] = ans

    try:
        data.to_excel(file,index=False)
    except Exception as e:
        data.to_csv(file,index=False)
    else:
        print("Error")
    

    
