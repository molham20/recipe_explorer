from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import json
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def scrape_recipes():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    service = Service(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service, options=options)
    
    try:
        driver.get("https://www.tasteofhome.com/recipes/")
        time.sleep(5)  # انتظار تحميل الصفحة

        # استخراج محسن للوصفات
        recipes = []
        articles = driver.find_elements(By.CSS_SELECTOR, "article.card") or \
                  driver.find_elements(By.CSS_SELECTOR, "div.article-card")
        
        for article in articles[:5]:  # أول 5 وصفات فقط
            try:
                title = article.find_element(By.CSS_SELECTOR, "h2").text
                link = article.find_element(By.TAG_NAME, "a").get_attribute("href")
                recipes.append({"title": title, "url": link})
            except Exception as e:
                print(f"خطأ في استخراج وصفة: {e}")
                continue

        if recipes:
            with open("recipe_data.json", "w", encoding="utf-8") as f:
                json.dump(recipes, f, indent=4, ensure_ascii=False)
            print(f"✅ تم استخراج {len(recipes)} وصفات بنجاح!")
            return recipes
        else:
            print("⚠️ لم يتم العثور على وصفات. جرب selectors أخرى.")
            return []

    except Exception as e:
        print(f"❌ خطأ رئيسي: {e}")
        return []
    finally:
        driver.quit()

if __name__ == "__main__":
    data = scrape_recipes()
    if data:
        print("الوصفات المستخرجة:")
        for recipe in data:
            print(f"- {recipe['title']}")