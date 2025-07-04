import json
import time
import signal
import multiprocessing
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options

INPUT_FILE = "leads.json"
OUTPUT_FILE = "linkedin_output.json"
PROCESSES = 4

# Graceful shutdown flag
shutdown = multiprocessing.Event()

def get_stealth_driver():
    options = uc.ChromeOptions()
    options.headless = False
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = uc.Chrome(options=options)
    return driver

def extract_linkedin_profiles(entry):
    founder = entry.get("founder_name", "")
    if not founder:
        return []

    query = f"{founder} site:linkedin.com"
    driver = get_stealth_driver()

    try:
        driver.get("https://www.google.com")
        time.sleep(1)
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.submit()
        time.sleep(2)

        results = driver.find_elements(By.CSS_SELECTOR, "div.g")
        links = []
        for result in results:
            link_element = result.find_element(By.TAG_NAME, "a")
            href = link_element.get_attribute("href")
            if "linkedin.com/in/" in href:
                links.append(href)
        return links
    except Exception as e:
        print(f"Error extracting {founder}: {e}")
        return []
    finally:
        driver.quit()

def process_chunk(chunk, output_queue):
    for entry in chunk:
        if shutdown.is_set():
            break

        founder = entry.get("founder_name", "")
        links = extract_linkedin_profiles(entry)
        output_queue.put({
            "title": entry.get("title", ""),
            "founder": founder,
            "linkedin_profiles": links
        })
        print(f"✅ [{entry.get('title')}] -> {len(links)} LinkedIn profiles.")

def save_results(queue, existing):
    results = existing
    while not queue.empty():
        results.append(queue.get())
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

def load_existing_output():
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def signal_handler(sig, frame):
    print("\n🛑 Ctrl+C detected. Saving progress...")
    shutdown.set()

signal.signal(signal.SIGINT, signal_handler)

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        entries = json.load(f)

    processed = load_existing_output()
    processed_names = {e["founder"] for e in processed if "founder" in e}
    unprocessed = [e for e in entries if e.get("founder_name") not in processed_names]

    if not unprocessed:
        print("✅ All entries already processed.")
        return

    print(f"🔄 Starting multiprocessing with {PROCESSES} workers...")
    chunks = [unprocessed[i::PROCESSES] for i in range(PROCESSES)]
    output_queue = multiprocessing.Manager().Queue()

    processes = [
        multiprocessing.Process(target=process_chunk, args=(chunk, output_queue))
        for chunk in chunks
    ]

    for p in processes:
        p.start()

    try:
        while any(p.is_alive() for p in processes):
            time.sleep(1)
    except KeyboardInterrupt:
        shutdown.set()
        for p in processes:
            p.terminate()

    for p in processes:
        p.join()

    save_results(output_queue, processed)
    print("💾 Results saved.")

if __name__ == "__main__":
    main()
