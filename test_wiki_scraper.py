import requests
from bs4 import BeautifulSoup
import re

def test_month_page_scrape(day, month):
    safe_month = month.replace(' ', '_')
    url = f"https://en.wikipedia.org/wiki/{safe_month}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    print(f"Testing URL: {url} searching for Day {day}")
    
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code == 200:
            print("Status: 200 OK")
            soup = BeautifulSoup(resp.content, 'html.parser')
            
            day_patterns = [
                f"{day} {month}", 
                f"{day}th {month}",
                f"{day}st {month}",
                f"{day}nd {month}",
                f"{day}rd {month}",
                f"{day} "
            ]
            print(f"Patterns: {day_patterns}")

            content_div = soup.find('div', {'id': 'mw-content-text'})
            found_count = 0
            if content_div:
                for li in content_div.find_all('li'):
                    text = li.get_text(strip=True)
                    if any(text.lower().startswith(p.lower()) for p in day_patterns) or text.startswith(f"{day} –") or text.startswith(f"{day} -"):
                         if len(text) > 10 and len(text) < 300:
                            clean_text = re.sub(r'\[\d+\]', '', text)
                            print(f"MATCH: {clean_text}")
                            found_count += 1
            
            if found_count == 0:
                print("No matches found.")
        else:
            print(f"Failed status: {resp.status_code}")
    except Exception as e:
        print(f"Error: {e}")

print("--- Testing 15 Rajab Fallback ---")
test_month_page_scrape(15, "Rajab")

print("\n--- Testing 1 Muharram Fallback ---")
test_month_page_scrape(1, "Muharram")
