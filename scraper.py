from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os.path
import pickle
import time
import csv


driver = webdriver.Chrome()
driver.maximize_window()
def get_all_mobile_url(driver):
    mobile_url = "https://www.digikala.com/search/category-mobile-phone/"
    all_mobiles_urls = []
    # last page: 173
    number_of_loaded_product = 0
    even_odd = 0
    driver.get(mobile_url)
    page_number = ""
    while (True):
        try:
            element = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[3]/div[3]/div[1]/div/section[1]/div[2]/div[2]/div[2]/span[5]/span")
            page_number = element.text
            break
        except:
            if even_odd % 2 == 0:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
            else:
                driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(1)
            even_odd += 1

    for page in range(1, int(page_number)+1):

        page_url = mobile_url + "?page=" + str(page)
        driver.get(page_url)
        time.sleep(5)
        try:
            element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.border-b:nth-child(5)")))
        except:
            print ("page excepted: " , str(page_url))
            continue
        mobiles = driver.find_elements(By.XPATH, '//a[contains(@href, "/product/dkp")]') #for finding all the mobile elements 
        for mobile in mobiles:
            all_mobiles_urls.append(mobile.get_attribute("href"))
    with open('all_mobiles_urls.pkl', 'wb') as f:
        pickle.dump(all_mobiles_urls, f)
if not os.path.isfile('all_mobiles_urls.pkl'):
    get_all_mobile_url(driver)

with open('all_mobiles_urls.pkl', 'rb') as f:
        all_mobiles_urls = pickle.load(f)
print (all_mobiles_urls[251])
if not os.path.isfile('all_mobiles_properties.pkl'):

    all_mobiles_urls = []
    with open('all_mobiles_urls.pkl', 'rb') as f:
        all_mobiles_urls = pickle.load(f)
    # print(all_mobiles_urls)

    
    mobiles_dict_list = []
    counter = 1
    for mobile_url in all_mobiles_urls[:400]:
        print (counter)
        counter += 1
        try:
            driver.get(mobile_url)
            time.sleep(2)
            driver.execute_script("document.querySelector(\"#specification > span\").click();")

            all_properties_div = driver.find_element(By.XPATH, "//*[@id=\"specification\"]/div[2]")
            properties = all_properties_div.find_elements(By.XPATH, "//div[@class='w-full d-flex last PdpSpecification_PdpSpecification__valuesBox__smZXG']")
            mobile_property_dict = {}
            for mobile_property in properties:
                property_ps = mobile_property.find_elements(By.TAG_NAME, "p")
                property_name , property_value = property_ps[0].text, property_ps[1].text
                mobile_property_dict[property_name] = property_value
            mobile_property_dict["price"] = driver.find_element(By.XPATH, "//*[@id=\"__next\"]/div[1]/div[3]/div[3]/div[2]/div[2]/div[2]/div[2]/div[3]/div[1]/div[8]/div/div[2]/div[1]/div/div[1]/span").text
            mobiles_dict_list.append(mobile_property_dict)
        except:
            continue


    with open('all_mobiles_properties.pkl', 'wb') as f:
            pickle.dump(mobiles_dict_list, f)


mobiles_dict_list = []
with open('all_mobiles_properties.pkl', 'rb') as f:
        mobiles_dict_list = pickle.load(f)



property_header_csv = []
for mobile_dict in mobiles_dict_list:
    for dict_key in mobile_dict.keys():
        if dict_key not in property_header_csv:
            property_header_csv.append(dict_key)

mobiles_row = []
for mobile_dict in mobiles_dict_list:
    mobile_row = []
    for dict_key in property_header_csv:
        if dict_key in mobile_dict:
            mobile_row.append(mobile_dict[dict_key])
        else:
            mobile_row.append("")
    mobiles_row.append(mobile_row)
# delete the extra charachter
for i in range(len(property_header_csv)):
    if "\u200c" in property_header_csv[i]:
        property_header_csv[i] = property_header_csv[i].replace("\u200c", " ")
print (property_header_csv)
with open('data.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(property_header_csv)
    for mobile_row in mobiles_row:
        writer.writerow(mobile_row)

driver.close()
