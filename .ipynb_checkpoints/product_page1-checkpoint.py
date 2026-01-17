"""""
For_rent_product_page_scraper
-steps:
   1. HTTP request
   2. Headers
   3. HTML parsing
   4. Data extraction
   5. Pagination handling
"""

from camoufox.sync_api import Camoufox
from playwright.sync_api import TimeoutError as playwrightTimeoutError
import json
import random
from pathlib import Path
from datetime import datetime
import time

with Camoufox(
    headless=True,
    persistent_context=True,
    user_data_dir="user_data_dir",
    os=("windows",),
    i_know_what_im_doing=True
    
) as browser:

    # Starting URL
    page = browser.new_page()
    
    base_url = "https://www.forrent.com"
    current_url = "https://www.forrent.com/find/NY/metro-NYC/New+York"
    
    rental_list = []
    page_count = 0
    
    while current_url:
        page_count+= 1
        print(f"\n Scraping page {page_count}...")
        
        # HTTP Request
        page.goto(current_url)
        
        # Human engineering behavior Simulation
        page.mouse.move(random.randint(0, 800), random.randint(0, 600))
        page.wait_for_timeout(random.randint(2000, 5000)) 

        # Header & Response Handling (ensure XHR/fetch completed)
        page.wait_for_load_state("networkidle", timeout=30000)
        
        # HTML Parsing / J-S render confirmation (Dom manipulation wait time)
        page.wait_for_timeout(random.randint(1000, 3000))
        
        # Additional Human engineering behavior Simulation
        human_delay = random.uniform(1.0, 3.0)
        time.sleep(human_delay)
        
        # Data Extraction
        listings = page.locator('article.fr-placard')
        
        for list in listings.all():
            # rental_type_text = list.locator('div.flex.gap-2.mr-6.mb-1 p.font-semibold.truncate').inner_text().strip()
            # address_text = list.locator('h2.text-sm.font-normal').inner_text().strip()
            rental_text = list.locator('p.border-l.border-border.px-2.uppercase').inner_text().strip()
            price_text = list.locator('p.pr-2.font-semibold').inner_text().strip()
            bath_text = list.locator('p.border-l.border-border.pl-2.uppercase').inner_text().strip()
            contact_text = list.locator('a span.hidden.sm\\:inline').inner_text().strip()
  
            data = {
                # 'rental_type': rental_type_text,
                # 'address': address_text,
                'Price': price_text,
                'rental_size': rental_text,
                'Bath_size': bath_text,
                'contact': contact_text
            }
            rental_list.append(data)
            
        print(f"Extracted {listings.count()} listings from page {page_count} (Total: {len(rental_list)})")
            
    # Write JSON to file
    out_dir = Path(r"C:\Users\Mteto\Desktop\Practice\forrentcamoufox")
    out_dir.mkdir(exist_ok=True, parents=True)
    out_file = out_dir / f"imdb_250movies_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_file.write_text(json.dumps(rental_list, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved to: {out_file}")

    page.close()
