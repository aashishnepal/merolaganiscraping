from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium. webdriver.common.keys import Keys
from selenium.webdriver. support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException        
from selenium.common.exceptions import TimeoutException,ElementNotVisibleException,ElementNotSelectableException
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

def fluent_wait(xpathid):
    try:
        element = WebDriverWait(driver, 20, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
            EC.presence_of_element_located((By.XPATH, xpathid)))
    except TimeoutException:
        print("Element not found")
    return element

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
 driver.find_element('id', 'ctl00_ContentPlaceHolder1_CompanyDetail1_lnkFloorsheetTab').click()
 driver.implicitly_wait(10)

 pagination="ctl00_ContentPlaceHolder1_CompanyDetail1_PagerControlFloorsheet1_litRecords"
 
 element = wait.until(EC.presence_of_element_located ((By.ID, pagination)))
#  element = wait.until(EC.text_to_be_present_in_element (((By.ID, pagination),"Total pages: ")))
 total_pages=10
# Check if the element has text
#  print(element)
 if element.text :
   soup = BeautifulSoup(element.get_attribute("outerHTML"), 'html.parser')
   total_pages_text = soup.find('span', {'id': pagination}).text
   total_pages = total_pages_text.split('[Total pages: ')[1].split(']')[0]

#  else:
#   total_pages=1
 
#  print('*-*-*-* pages')
#  print(f'Total pages: {total_pages}')

 data_extract_save(total_pages)


# Extracting data from web
def data_extract_save(pages):
   path_table='//*[@id="ctl00_ContentPlaceHolder1_CompanyDetail1_divDataFloorsheet"]/div[2]/table/tbody'
   next_button='//*[@id="ctl00_ContentPlaceHolder1_CompanyDetail1_divDataFloorsheet"]/div[1]/div[2]/a[6]'
   loading_element='//*[@id="processing"]'
   tbody =wait.until(lambda x: x.find_element(By.XPATH,path_table))
   data = []           
   

# Pagination data extraction
   for page in range(pages):
    driver.implicitly_wait(20)  
    tbody= fluent_wait(path_table)

    rows = tbody.find_elements(By.XPATH,'//tr')
    for row in rows:
      # row_data=row.text.split()
      data.append(row.text)
    wait.until(EC.presence_of_element_located((By.XPATH, next_button))).click()
    wait.until(EC.invisibility_of_element((By.XPATH, loading_element)))
 
  #  data_index= int(data.index("#"))
 
#   Save to CSV
   skip_count = 36
   selected_data = data[skip_count : skip_count + 100]
   chunk_size = 100
   all_selected_data = []
   while skip_count < len(data):
       selected_data = data[skip_count : skip_count + chunk_size]
       all_selected_data.extend(selected_data)
       skip_count += chunk_size + 36
  #  titles=data[35].split()   
   with open("hdlscrapdata.csv", "w", newline="") as csvfile:
    csvfile.writelines(data[35]) 
    csvfile.write('\n')
    for i in range(len(all_selected_data)):
      csvfile.writelines (all_selected_data[i])
      csvfile.write('\n')






if __name__ == "__main__":
   search('hdl')
   driver.quit()