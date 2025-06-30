from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import re
import time

def parse_car_data(url: str) -> dict:
    try:
        print("[parser] Запуск selenium-парсера:", url)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)
        time.sleep(5)

        title = driver.title or ""
        print("[parser] title:", title)

        # Поиск цены
        try:
            price_element = driver.find_element(By.CSS_SELECTOR, '[itemprop="price"]')
            price_str = price_element.get_attribute("content")
        except Exception as e:
            print("[parser] price error:", e)
            price_str = None

        try:
            price = int(float(price_str.replace(" ", "").replace("\u202f", ""))) if price_str else 0
        except:
            price = 0

        brand = title.split()[0] if title else "Unknown"
        model = title.split()[1] if len(title.split()) > 1 else "Unknown"
        year_match = re.search(r"\b(19|20)\d{2}\b", title)
        year = int(year_match.group(0)) if year_match else 2020

        driver.quit()

        result = {
            "brand": brand,
            "model": model,
            "year": year,
            "price": price
        }

        print("[parser] result:", result)
        return result

    except Exception as e:
        print(f"[Selenium parser error]: {e}")
        return None
