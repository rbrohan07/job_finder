from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url="https://remoteok.com"


WebDriverWait(driver, 3).until(
    EC.presence_of_element_located((By.TAG_NAME, "script"))
)
driver.get(url)



html = driver.page_source
with open("REMOTE.html", "w", encoding="utf-8") as f:
    f.write(html)
# soup = BeautifulSoup(response.text, "lxml")
print(html)