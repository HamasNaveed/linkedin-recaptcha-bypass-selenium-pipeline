import json
import time
import random
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent

# === File Paths ===
INPUT_PATH = r"D:\University\Personals\Intership\Script\indiResults.json"
OUTPUT_PATH = r"D:\University\Personals\Intership\Script\linkedin_results.json"

# === Get Stealth Chrome Driver ===
def get_stealth_driver():
    ua = UserAgent()
    user_agent = ua.random
    print(f"🌀 Using User-Agent: {user_agent}")

    options = uc.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument(f'user-agent={user_agent}')
    return uc.Chrome(options=options)

# === Load Input JSON ===
try:
    with open(INPUT_PATH, "r", encoding="utf-8") as file:
        projects = json.load(file)
except json.JSONDecodeError as e:
    print(f"❌ Error reading JSON: {e}")
    exit()

# === Load Existing Output Data ===
if os.path.exists(OUTPUT_PATH):
    try:
        with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
            linkedin_data = json.load(f)
            print(f"📂 Loaded existing {len(linkedin_data)} entries from output file.")
    except:
        linkedin_data = []
else:
    linkedin_data = []

# === Track Already Processed Founders ===
already_done = set()
for entry in linkedin_data:
    already_done.add(entry.get("founder", "").strip())

# === Start Chrome Driver ===
driver = get_stealth_driver()

def handle_captcha_and_retry(query_url):
    global driver
    driver.get(query_url)
    time.sleep(5)
    page_source = driver.page_source.lower()
    if "unusual traffic" in page_source or "captcha" in page_source:
        print("🛑 CAPTCHA detected. Restarting browser...")
        driver.quit()
        driver = get_stealth_driver()
        driver.get(query_url)
        time.sleep(5)

try:
    for index, project in enumerate(projects):
        founder = project.get("founder_name", "").strip()
        title = project.get("title", "").strip()

        if not founder or founder in already_done:
            continue

        query = f'"{founder}" CEO OR Founder OR President linkedin'
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"

        print(f"\n🔍 [{index + 1}] Searching: {founder} ({title})")
        handle_captcha_and_retry(search_url)

        timeout = 30
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

        if len(linkedin_data) % 5 == 0:
            with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
                json.dump(linkedin_data, f, indent=4)
            print("💾 Partial results saved.")

        delay = random.uniform(4, 9)
        print(f"⏳ Sleeping for {delay:.2f} seconds...")
        time.sleep(delay)

except KeyboardInterrupt:
    print("\n🛑 Interrupted by user (Ctrl+C). Saving collected data...")

except Exception as e:
    print(f"\n❌ Unexpected error: {e}")

finally:
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(linkedin_data, f, indent=4)
    driver.quit()
    print(f"\n💾 Final results saved to: {OUTPUT_PATH}")
