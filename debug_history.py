from datetime import datetime
import requests
from bs4 import BeautifulSoup
from hijri_converter import Gregorian

def check_history():
    print("Checking history for 16 Rajab...")
    h_month_name = "Rajab"
    h_day = 16
    
    # 1. Check existing Wikipedia scraper logic
    try:
        safe_month = h_month_name.replace(' ', '_')
        wiki_url = f"https://en.wikipedia.org/wiki/{safe_month}"
        print(f"Fetching {wiki_url}")
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(wiki_url, headers=headers, timeout=5)
        
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            
            day_patterns = [
                f"{h_day} {h_month_name}", 
                f"{h_day}th {h_month_name}",
                f"{h_day}st {h_month_name}",
                f"{h_day}nd {h_month_name}",
                f"{h_day}rd {h_month_name}",
                f"{h_day} "
            ]
            print(f"Looking for patterns: {day_patterns}")
            
            found = False
            content_div = soup.find('div', {'id': 'mw-content-text'})
            if content_div:
                for li in content_div.find_all('li'):
                    text = li.get_text(strip=True)
                    if any(text.lower().startswith(p.lower()) for p in day_patterns) or text.startswith(f"{h_day} –") or text.startswith(f"{h_day} -"):
                        print(f"MATCH: {text}")
                        found = True
            
            if not found:
                print("No matches found on Wikipedia page.")
                
        # 2. Check WikiShia
        print("\nChecking WikiShia...")
        wikishia_url = f"https://en.wikishia.net/view/{h_month_name}"
        print(f"Fetching {wikishia_url}")
        resp = requests.get(wikishia_url, headers=headers, timeout=5)
        if resp.status_code == 200:
             soup = BeautifulSoup(resp.content, 'html.parser')
             # WikiShia usually lists events clearly.
             # Structure might be headings or lists.
             # Let's search for "16 Rajab" text in the page
             text_content = soup.get_text()
             if f"{h_day} {h_month_name}" in text_content:
                 print(f"Found '{h_day} {h_month_name}' in text content!")
             
             # Try to find specific LI
             for li in soup.find_all('li'):
                 text = li.get_text(strip=True)
                 if text.startswith(f"{h_day} {h_month_name}") or text.startswith(f"{h_day}th {h_month_name}"):
                     print(f"WikiShia Match: {text}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_history()
