📘 README.md
🔍 Project: LinkedIn Profile Scraper + Keyword Filter
This project is a two-part automation pipeline using Python and Selenium:

Keyword Filter — filters projects based on relevance using keyword matching.

LinkedIn Scraper — performs Google searches to extract potential LinkedIn profiles of founders, bypassing reCAPTCHA using stealth techniques.

📁 Folder Structure
graphql
Copy
Edit
.
├── linkedin_scraper.py          # Main LinkedIn scraping script (uses undetected Chrome)
├── keyword_filter.py            # Keyword-based project filtering script
├── keywords.py                  # Contains the list of matching keywords
├── indiResults.json             # Raw input JSON with project data
├── filtered.json                # Output: filtered projects based on keywords
├── linkedin_results.json        # Output: scraped LinkedIn profiles
🛠️ Requirements
Install the required packages:

bash
Copy
Edit
pip install selenium undetected-chromedriver fake-useragent
🔑 Files Explained
1. keyword_filter.py
Purpose: Filters project entries (indiResults.json) that match any keyword or phrase in keywords.py.

Matches both full phrases and individual words.

Outputs filtered results to filtered.json.

Example keywords.py:
python
Copy
Edit
KEYWORDS = [
    "AI", "Artificial Intelligence", "machine learning", 
    "early-stage startup", "MVP", "B2B SaaS"
]
2. linkedin_scraper.py
Purpose: Automates Google searches to find LinkedIn profiles of startup founders.

Key Features:

Uses undetected-chromedriver to bypass Google CAPTCHA.

Randomizes user-agent using fake_useragent.

Saves output to linkedin_results.json.

Resumes from where it left off if interrupted.

Saves data every 5 records to prevent loss.

🧪 How to Run
Step 1: Filter Relevant Projects
bash
Copy
Edit
python keyword_filter.py
This will:

Read indiResults.json

Match based on keywords.py

Write matching entries to filtered.json

Step 2: Scrape LinkedIn Profiles
bash
Copy
Edit
python linkedin_scraper.py
This will:

Read from filtered.json or indiResults.json

For each founder, search Google for LinkedIn profiles

Store results in linkedin_results.json

🧠 How It Works
Keyword Filter Logic
Scans description and paragraphs fields.

If any keywords or keyword words are present, includes the item.

Scraper Logic
Constructs a Google search query like:
"John Doe" CEO OR Founder OR President linkedin

Parses top 5 result links containing "linkedin.com/in/"

Automatically skips already-processed entries.

🛡️ Anti-Bot Handling
undetected-chromedriver mimics real user behavior

Randomized user-agent strings

Automatically restarts Chrome if CAPTCHA detected

📝 Output Format
linkedin_results.json:
json
Copy
Edit
[
  {
    "founder": "John Doe",
    "title": "Awesome AI App",
    "linkedin_profiles": [
      "https://www.linkedin.com/in/john-doe-ai",
      "https://www.linkedin.com/in/john-doe-xyz"
    ]
  }
]
🚧 Notes
Make sure you have Google Chrome installed.

This script uses public Google Search and may hit rate limits if run too fast or too often.

You may want to proxy or rotate IPs for large-scale scraping.
