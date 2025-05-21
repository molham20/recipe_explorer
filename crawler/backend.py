from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import time

def scrape_recipe(url):
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get(url)
        time.sleep(5)  # انتظار إضافي لتحميل الصفحة

        # استخدام BeautifulSoup لتحليل المحتوى
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # استخراج البيانات بطريقة أكثر مرونة
        recipe = {
            'title': soup.find('h1').get_text(strip=True) if soup.find('h1') else 'No Title Found',
            'ingredients': [li.get_text(strip=True) for li in soup.select('.ingredients-section li')],
            'instructions': [step.get_text(strip=True) for step in soup.select('.instructions-section li')],
            'prep_time': soup.select_one('.prep-time').get_text(strip=True) if soup.select_one('.prep-time') else 'N/A',
            'cook_time': soup.select_one('.cook-time').get_text(strip=True) if soup.select_one('.cook-time') else 'N/A',
            'url': url
        }
        
        return recipe
        
    except Exception as e:
        print(f"Error scraping recipe: {str(e)}")
        return None
    finally:
        driver.quit()