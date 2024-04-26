import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

# 初始化webdriver

'''
cpuurl = "https://zj.zol.com.cn/proFilter/sub28_m_gnoPrice__k_1_1_1.html?&time=28"
主板url = "https://zj.zol.com.cn/proFilter/sub5_m_gnoPrice__k_1_1_1.html?&time=5"
内存url = "https://zj.zol.com.cn/proFilter/sub3_m_gnoPrice__k_1_1_1.html?&time=3"
硬盘url = "https://zj.zol.com.cn/proFilter/sub2_m_gnoPrice__k_1_1_1.html?&time=2"
固态硬盘url = “https://zj.zol.com.cn/proFilter/sub626_m_gnoPrice__k_1_1_1.html?&time=626”
显卡url = "https://zj.zol.com.cn/proFilter/sub6_m_gnoPrice__k_1_1_1.html?&time=6"
显示器url = "https://zj.zol.com.cn/proFilter/sub84_m_gnoPrice__k_1_1_1.html?&time=84"
机箱url = "https://zj.zol.com.cn/proFilter/sub10_m_gnoPrice__k_1_1_1.html?&time=10"
电源url = "https://zj.zol.com.cn/proFilter/sub35_m_gnoPrice__k_1_1_1.html?&time=35"
'''

urls = ["https://zj.zol.com.cn/proFilter/sub28_m_gnoPrice__k_1_1_1.html?&time=28", "https://zj.zol.com.cn/proFilter/sub5_m_gnoPrice__k_1_1_1.html?&time=5", "https://zj.zol.com.cn/proFilter/sub3_m_gnoPrice__k_1_1_1.html?&time=3",
"https://zj.zol.com.cn/proFilter/sub2_m_gnoPrice__k_1_1_1.html?&time=2", "https://zj.zol.com.cn/proFilter/sub626_m_gnoPrice__k_1_1_1.html?&time=626", "https://zj.zol.com.cn/proFilter/sub6_m_gnoPrice__k_1_1_1.html?&time=6", 
"https://zj.zol.com.cn/proFilter/sub84_m_gnoPrice__k_1_1_1.html?&time=84", "https://zj.zol.com.cn/proFilter/sub10_m_gnoPrice__k_1_1_1.html?&time=10", "https://zj.zol.com.cn/proFilter/sub35_m_gnoPrice__k_1_1_1.html?&time=35"]

for url_index in range(3, 5):
    all_products = []

# 打开网页
    driver = webdriver.Chrome()
    driver.get(urls[url_index])

    def scrape_products():
        products = []

        product_elements = driver.find_elements(By.CSS_SELECTOR, ".pitem.clearfix")

        for product_element in product_elements:
            name = product_element.find_element(By.CSS_SELECTOR, ".pro-intro h3 a").text
            price = product_element.find_element(By.CSS_SELECTOR, ".price-box .price").text
            price = price[1:]


            try:
                jdprice = product_element.find_element(By.CSS_SELECTOR, ".jd.shop-click").text
                jdprice = jdprice[4:]
                # print(jdprice)
            except:
                jdprice = '暂无京东价格'

            parameters_elements = product_element.find_elements(By.CSS_SELECTOR, ".paramet span")
            parameters = {}

            for element in parameters_elements:
                element_text = element.text
                cleaned_text = re.sub(r'更多参数>>\s+\d+人点评\s+\d+篇评测', '', element_text)
                cleaned_text = cleaned_text.strip().split('\n')
                for i in cleaned_text:
                    if i == "":
                        continue
                    try:
                        key, value = i.split('：')
                        if value.endswith('/'):
                            value = value[:-1]
                        parameters[key] = value
                    except ValueError:
                        continue

            product = {
                "name": name,
                "price": price,
                "jdprice": jdprice,
                "parameters": parameters
            }

            products.append(product)
        
        return products

    # 获取当前页码（假设初始为第一页）
    current_page = 1

    while True:
        flag = 0
        print(f"正在处理第{current_page}页...")
        
        # 执行数据爬取
        current_products = scrape_products()
        all_products.extend(current_products)

        # 点击下一页
        try:
            page_source_before_click = driver.page_source  # 点击前的页面源代码

            page_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "page-box"))
            )
            next_button = page_box.find_element(By.CLASS_NAME, "next")
            
            next_button.click()
            
            # 等待页面加载完成
            WebDriverWait(driver, 10).until(
                lambda driver: driver.page_source != page_source_before_click  # 等待页面源代码更新
            )
            
            # 更新当前页码
            current_page += 1
            
        except Exception as e:
            driver.quit()
            break

    # 关闭浏览器
    driver.quit()

    if url_index == 0:
        with open('cpu.json', 'a', encoding='utf-8') as f:
            json_str = json.dumps(all_products, ensure_ascii=False, indent=4)
            f.write(json_str)
    if url_index == 1:
        with open('motherboard.json', 'a', encoding='utf-8') as f:
            json_str = json.dumps(all_products, ensure_ascii=False, indent=4)
            f.write(json_str)

    if url_index == 2:
        with open('memory.json', 'a', encoding='utf-8') as f:
            json_str = json.dumps(all_products, ensure_ascii=False, indent=4)
            f.write(json_str)
    
    if url_index == 3:
        with open('harddisk.json', 'a', encoding='utf-8') as f:
            json_str = json.dumps(all_products, ensure_ascii=False, indent=4)
            f.write(json_str)
    
    if url_index == 4:
        with open('ssd.json', 'a', encoding='utf-8') as f:
            json_str = json.dumps(all_products, ensure_ascii=False, indent=4)
            f.write(json_str)
    
    if url_index == 5:
        with open('graphicscard.json', 'a', encoding='utf-8') as f:
            json_str = json.dumps(all_products, ensure_ascii=False, indent=4)
            f.write(json_str)
    
    if url_index == 6:
        with open('monitor.json', 'a', encoding='utf-8') as f:
            json_str = json.dumps(all_products, ensure_ascii=False, indent=4)
            f.write(json_str)
    
    if url_index == 7:
        with open('chassis.json', 'a', encoding='utf-8') as f:
            json_str = json.dumps(all_products, ensure_ascii=False, indent=4)
            f.write(json_str)
    
    if url_index == 8:
        with open('power.json', 'a', encoding='utf-8') as f:
            json_str = json.dumps(all_products, ensure_ascii=False, indent=4)
            f.write(json_str)
