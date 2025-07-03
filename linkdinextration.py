import json
import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

# === File Paths ===
INPUT_PATH = r"D:\University\Personals\Intership\Script\indiResults.json"
OUTPUT_PATH = r"D:\University\Personals\Intership\Script\linkedin_results.json"

# === Get Stealth Chrome Driver ===
def get_stealth_driver():
    options = uc.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')
    return uc.Chrome(options=options)

# === Load Input JSON ===
try:
    with open(INPUT_PATH, "r", encoding="utf-8") as file:
        projects = json.load(file)
except json.JSONDecodeError as e:
    print(f"❌ Error reading JSON: {e}")
    exit()

# === Start Chrome & Setup Storage ===
driver = get_stealth_driver()
linkedin_data = []

try:
    for index, project in enumerate(projects):
        founder = project.get("founder_name", "").strip()
        title = project.get("title", "").strip()

        if not founder:
            print(f"⚠️ Skipping entry {index + 1} due to missing founder name.")
            continue

        # ✅ Build Search Query
        query = f'"{founder}" CEO OR Founder OR President linkedin'
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"

        print(f"\n🔍 [{index + 1}] Searching: {founder} ({title})")
        driver.get(search_url)
        print("🕵️ If CAPTCHA appears, solve it manually...")

        # Wait for results or timeout
        timeout = 60
        start_time = time.time()
        while True:
            try:
                results = driver.find_elements(By.CSS_SELECTOR, 'div.yuRUbf a')
                if results:
                    break
            except:
                pass
            if time.time() - start_time > timeout:
                print("⏱️ Timeout waiting for search results.")
                results = []
                break
            time.sleep(2)

        # ✅ Collect LinkedIn Links
        linkedin_links = []
        for result in results:
            link = result.get_attribute("href")
            if "linkedin.com/in/" in link and link not in linkedin_links:
                linkedin_links.append(link)
            if len(linkedin_links) >= 5:
                break

        linkedin_data.append({
            "founder": founder,
            "title": title,
            "linkedin_profiles": linkedin_links
        })

        print(f"✅ Found {len(linkedin_links)} LinkedIn profiles.")
        time.sleep(random.uniform(4, 7))

except KeyboardInterrupt:
    print("\n🛑 Interrupted by user (Ctrl+C). Saving collected data...")

except Exception as e:
    print(f"\n❌ Unexpected error: {e}")

finally:
    # ✅ Save collected results no matter what
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(linkedin_data, f, indent=4)
    driver.quit()
    print(f"\n💾 Results saved to: {OUTPUT_PATH}")
