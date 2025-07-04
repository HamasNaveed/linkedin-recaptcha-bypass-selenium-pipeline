import json
from keywords import KEYWORDS

# Normalize keyword sets
full_keywords = set([kw.lower() for kw in KEYWORDS])
keyword_words = set()
for keyword in KEYWORDS:
    keyword_words.update(keyword.lower().split())

def get_matched_keywords(text):
    matched = set()
    text_lower = text.lower()

    # Match full phrases
    for keyword in full_keywords:
        if keyword in text_lower:
            matched.add(keyword)

    # Match individual words (optional: comment out if you only want exact phrases)
    for word in text_lower.split():
        if word in keyword_words:
            matched.add(word)

    return matched

# Load data
with open('indiResults.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Filter entries
filtered = []
for item in data:
    description = item.get('description', '')
    paragraphs = item.get('allParagraphs', [])
    all_texts = [description] + paragraphs

    matched_keywords = set()
    for text in all_texts:
        matched_keywords.update(get_matched_keywords(text))

    if matched_keywords:
        item['matched_keywords'] = list(matched_keywords)
        filtered.append(item)

# Save filtered results
with open('filtered.json', 'w', encoding='utf-8') as f:
    json.dump(filtered, f, indent=2, ensure_ascii=False)

print(f"Filtered {len(filtered)} matching items saved to 'filtered.json'")
