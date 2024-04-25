import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 初始化webdriver
driver = webdriver.Chrome()

url = "https://zj.zol.com.cn/proFilter/sub28_m_gnoPrice__k_1_1_1.html?&time=28"

# 打开网页
driver.get(url)

def scrape_products():
    products = []

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
                try:
                    key, value = i.split('：')
                    parameters[key] = value
                except ValueError:
                    continue

        product = {
            "name": name,
            "price": price,
            "parameters": parameters
        }

        products.append(product)
    
    return products

# 获取当前页码（假设初始为第一页）
current_page = 1

while True:
    print(f"正在处理第{current_page}页...")
    
    # 执行数据爬取
    current_products = scrape_products()
    for product in current_products:
        print(product)
    
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
        print(f"翻页失败: {e}")
        break

# 关闭浏览器
driver.quit()
