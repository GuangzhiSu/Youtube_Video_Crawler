from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os

# 设置 ChromeDriver 路径
driver_path = os.path.expanduser('/home/gs285/chrome-testing/chromedriver-linux64/chromedriver')

# 配置无头模式
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.binary_location = os.path.expanduser('/home/gs285/chrome-testing/chrome-linux64/chrome')  # 确保使用正确的 Chrome 可执行文件路径

# 初始化 WebDriver
driver = webdriver.Chrome(executable_path=driver_path, options=options)

# 禁用 webdriver 属性
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': '''
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
    '''
})

# 打开 YouTube
driver.get("https://www.youtube.com")
print("Opened YouTube")

# 加载登录 Cookies
with open('/home/gs285/Youtube_video_Scrape/cookies.json', 'r') as cookies_file:
    cookies = json.load(cookies_file)
    for cookie in cookies:
        # 修正 sameSite 属性
        if "sameSite" in cookie and cookie["sameSite"] not in ["Strict", "Lax", "None"]:
            cookie["sameSite"] = "None"
        # 修正 domain 属性
        if "domain" in cookie:
            cookie["domain"] = ".youtube.com"
        driver.add_cookie(cookie)
        print(f"Added cookie: {cookie}")

# 刷新页面以应用 Cookies
driver.refresh()
print("Refreshed page")

# 设置短暂延迟以确保所有会话设置和 Cookies 已完全应用
time.sleep(10)

# 截取截图以确认页面加载状态
screenshot_path = os.path.expanduser('/home/gs285/screenshot_after_refresh.png')
driver.save_screenshot(screenshot_path)
print(f"Saved screenshot after refresh: {screenshot_path}")

# 确认已登录
wait = WebDriverWait(driver, 60)
try:
    account_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@aria-label, 'Account') or contains(@aria-label, '账户')]")))
    print("Logged in successfully")
except Exception as e:
    print(f"Login failed: {e}")
    screenshot_path = os.path.expanduser('~/screenshot_login_failed.png')
    driver.save_screenshot(screenshot_path)
    print(f"Saved screenshot on login fail: {screenshot_path}")
    driver.quit()
    exit()

# 设置短暂延迟以确保所有会话设置和 Cookies 已完全应用
time.sleep(5)

# 搜索关键词
search_query = "robotic surgery bleeding"
search_box = wait.until(EC.presence_of_element_located((By.NAME, "search_query")))
search_box.send_keys(search_query)
search_box.send_keys(Keys.RETURN)

# 等待搜索结果加载
time.sleep(3)

# 初始化视频列表
videos = []
scroll_pause_time = 2  # 设置页面滚动的暂停时间
last_height = driver.execute_script("return document.documentElement.scrollHeight")

while True:
    # 获取第一页的视频信息
    video_elements = driver.find_elements(By.CSS_SELECTOR, "a#video-title")
    for video in video_elements:
        title = video.get_attribute("title")
        url = video.get_attribute("href")
        if url and {"title": title, "url": url} not in videos:
            videos.append({"title": title, "url": url})

    # 滚动页面到最底部
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    
    # 等待页面加载
    time.sleep(scroll_pause_time)
    
    # 计算新的页面高度并比较
    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# 将视频信息保存到文件
with open('videos2.json', 'w') as videos_file:
    json.dump(videos, videos_file)
print(f"Saved videos to videos.json")

# 关闭浏览器
driver.quit()
print("Closed browser")