from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re

driver = webdriver.Chrome()

url = "https://zj.zol.com.cn/proFilter/sub28_m_gnoPrice__k_1_1_1.html?&time=28"
# url = "https://detail.zol.com.cn/cpu/"

driver.get(url)



page_source = driver.page_source

with open('cpu.txt', 'w', encoding='utf-8') as f:
    f.write(page_source)


products = []

# Extracting information for each product
product_elements = driver.find_elements(By.CSS_SELECTOR, ".pitem.clearfix")

for product_element in product_elements:
    name = product_element.find_element(By.CSS_SELECTOR, ".pro-intro h3 a").text
    price = product_element.find_element(By.CSS_SELECTOR, ".price-box .price").text
    
    parameters_elements = product_element.find_elements(By.CSS_SELECTOR, ".paramet span")
    parameters = {}
    
    for element in parameters_elements:
        element_text = element.text
        cleaned_text = re.sub(r'更多参数>>\s+\d+人点评\s+\d+篇评测', '', element_text)
        cleaned_text = cleaned_text.strip().split('\n')
        for i in cleaned_text:
            if i == "":
                continue
            key, value = i.split('：')
            print(key, value)
            parameters[key] = value

    product = {
        "name": name,
        "price": price,
        "parameters": parameters
    }
    
    products.append(product)

# Print the extracted information
for idx, product in enumerate(products, start=1):
    print(f"Product {idx}:")
    print("Name:", product["name"])
    print("Price:", product["price"])
    print("Parameters:", product["parameters"])
    print("-" * 50)

driver.quit()