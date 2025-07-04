import json

# Load filtered data from first file (after keyword matching)
with open('filtered.json', 'r', encoding='utf-8') as f:
    filtered_data = json.load(f)

# Load LinkedIn data
with open('linkedin_results.json', 'r', encoding='utf-8') as f:
    linkedin_data = json.load(f)

# Extract all titles from filtered data
filtered_titles = set(item['title'].strip().lower() for item in filtered_data)

# Match and extract relevant LinkedIn info
matched_items = []
for item in linkedin_data:
    title = item.get('title', '').strip().lower()
    if title in filtered_titles:
        matched_items.append({
            'founder': item.get('founder', ''),
            'title': item.get('title', ''),
            'linkedin_profiles': item.get('linkedin_profiles', [])
        })

# Save the matched LinkedIn data
with open('matched_linkedin.json', 'w', encoding='utf-8') as f:
    json.dump(matched_items, f, indent=2, ensure_ascii=False)

print(f"Saved {len(matched_items)} matched LinkedIn items to 'matched_linkedin.json'")
