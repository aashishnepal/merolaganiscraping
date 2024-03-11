from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium. webdriver.common.keys import Keys
from selenium.webdriver. support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
import chromedriver_autoinstaller


 
chromedriver_autoinstaller.install() 
                                   

options = webdriver.ChromeOptions()

options.add_argument('--headless')
options.add_argument('--enable-javascript')  
options.add_argument('blink-settings=imagesEnabled=false')     
options.add_argument('--no-sandbox')               
options.add_argument('--disable-gpu')              
options.add_argument('--hide-scrollbars')          
options.add_argument("--headless")  

url='https://merolagani.com/'
driver = webdriver.Chrome(options=options)
driver.get(url)

wait=WebDriverWait(driver,20)

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
   next_button='//*[@id="ctl00_ContentPlaceHolder1_CompanyDetail1_divDataFloorsheet"]/div[1]/div[2]/a[6]'
   tbody =wait.until(lambda x: x.find_element(By.XPATH,path_table))
   data = []
   

# Pagination data extraction
   for page in range(5):
    driver.implicitly_wait(20)
   #  tbody= WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, path_table)))
    rows = tbody.find_elements(By.XPATH,'//tr')
    for row in rows:
       data.append(row.text)
   #  wait.until(EC.presence_of_element_located((By.XPATH, next_button))).click()
 
   data_index= int(data.index("# Date Transact. No. Buyer Seller Qty. Rate Amount"))
 
#   Save to CSV
   skip_count = 36
   selected_data = data[skip_count : skip_count + 100]
   chunk_size = 100
   all_selected_data = []
   while skip_count < len(data):
       selected_data = data[skip_count : skip_count + chunk_size]
       all_selected_data.extend(selected_data)
       skip_count += chunk_size + 36
   
   with open("hdlscrapdata.csv", "w", newline="") as csvfile:
    csvfile.write(data[data_index]+'\n') 
    for i in range(len(all_selected_data)):
      csvfile.write(all_selected_data[i]+'\n')      





if __name__ == "__main__":
   search('hdl')
   driver.quit()

 



