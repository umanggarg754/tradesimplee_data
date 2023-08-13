
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


if __name__=="__main__":

    results = []

    link = "https://www.indiantradeportal.in/searchMember.jsp?t=Like&p=ceramic+tiles&x=0&y=0"
    driver = get_driver()
    driver.get(link) # //*[@id="inner-content"]/div[1]/form/table/tbody/tr
    contacts = driver.find_elements(By.XPATH,'//*[@id="inner-content"]/div[1]/form/table/tbody/tr')
    for i,contact in enumerate(contacts):
        html_content = contact.get_attribute("innerHTML")
        pattern = r'<td[^>]*>(.*?)<\/td>'
        matches = re.findall(pattern, html_content)
        # print(matches)
        data = {}
        try:
            data['name'] = matches[0].strip()
            data['products'] = matches[1].strip()
            data['HSN'] = matches[2].strip()
        except Exception as e:
            print(e,html_content)
            continue
        results.append(data)

    df = pd.DataFrame(results)
    df.to_csv("ceramic_tiles.csv",index=False)