from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium. webdriver.common.keys import Keys
from selenium.webdriver. support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
import chromedriver_autoinstaller

import time
import csv

chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--enable-javascript') # 启用 JavaScript
options.add_argument('blink-settings=imagesEnabled=false')      # 不加载图片，提升运行速度
options.add_argument('--no-sandbox')                # 解决DevToolsActivePort文件不存在的报错
options.add_argument('--disable-gpu')               # 谷歌文档提到需要加上这个属性来规避bug
options.add_argument('--hide-scrollbars')           # 隐藏滚动条，应对一些特殊页面
options.add_argument("--headless") #无界面

url='https://merolagani.com/'
driver = webdriver.Chrome(options=options)
driver.get(url)

wait=WebDriverWait(driver,10)

# Searching required Script
def search(ticker):
    driver.implicitly_wait(5)

    search_box = driver.find_element('id', 'ctl00_AutoSuggest1_txtAutoSuggest')
    search_box.send_keys(ticker)
 
    search_box.send_keys(Keys.ENTER)
    floor_sheet()

# Locating FloorSheet Menu 
def floor_sheet():  
 driver.implicitly_wait(5)
 floor_data = driver.find_element('id', 'ctl00_ContentPlaceHolder1_CompanyDetail1_lnkFloorsheetTab').click()

 pagination="ctl00_ContentPlaceHolder1_CompanyDetail1_PagerControlFloorsheet1_litRecords"
 
 element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, pagination)))
 total_pages=1
# Check if the element has text
 if element.text:
   soup = BeautifulSoup(element.get_attribute("outerHTML"), 'html.parser')
   total_pages_text = soup.find('span', {'id': pagination}).text
   total_pages = total_pages_text.split('[Total pages: ')[1].split(']')[0]

 else:
  total_pages=1
 
 print('*-*-*-* pages')
 print(f'Total pages: {total_pages}')

 data_extract_save(5)


# Extracting data from web
def data_extract_save(pages):
   path_table='//*[@id="ctl00_ContentPlaceHolder1_CompanyDetail1_divDataFloorsheet"]/div[2]/table/tbody'
   tbody =wait.until(lambda x: x.find_element(By.XPATH,path_table))
   data = []
   

# Pagination data extraction
   for page in range(5):
    # driver.implicitly_wait(10)

    # tbody= WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.XPATH, path_table)))
    rows = tbody.find_elements(By.XPATH,'//tr')
    for row in rows:
       data.append(row.text)
  #  wait.until(EC.presence_of_element_located((By.XPATH, '//a[contains(@onclick, "changePageIndex") and contains(@title, "Next Page")]'))).click()
 
   data_index= int(data.index("# Date Transact. No. Buyer Seller Qty. Rate Amount"))
 
# Save to CSV
  #  selected_data=process_data(data)
   start_index=data_index
   skip_interval=data_index+1
   selected_data=[]   
   data_to_store = 100
   for i in range(len(data)):
    # Skip indices before the 35th index
    if i < start_index:
        continue

    # Store data after the 35th index
    selected_data.append(data[i])

    # If 100 data points are stored, skip the next 35 indices
    if len(selected_data) == data_to_store:
        start_index = i + skip_interval


   with open("output.csv", "w", newline="") as csvfile:
    csvfile.write(data[data_index]+'\n') 
    for i in range(len(selected_data)):
      csvfile.write(selected_data[i]+'\n')      


# def process_data(data_list):
#     skip_interval = 35
#     batch_size = 100

#     # Iterate through the data list
#     for i in range(skip_interval, len(data_list), batch_size + skip_interval):
#         # Extract the batch of 100 elements after skipping 35 indices
#         batch_data = data_list[i:i + batch_size]
#         return batch_data
#         # Process or store the batch_data as needed
#         print(f"Processing data from index {i + 1} to {i + batch_size}:", batch_data)

 


if __name__ == "__main__":
   search('hdl')
   driver.quit()

 



#loop for pages
#extract data 
#next page
#extract data
#reach last page
#save data to csv
#
#
#