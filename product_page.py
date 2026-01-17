"""
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
    max_pages = 50  # Safety limit
    
    while current_url and page_count < max_pages:
        page_count += 1
        print(f"\nScraping page {page_count}...")
        print(f"URL: {current_url}")
        
        # HTTP Request
        page.goto(current_url, wait_until="domcontentloaded", timeout=60000)
        
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
        
        # Wait for listings
        page.wait_for_selector('article.fr-placard', timeout=10000)
        
        # Data Extraction
        listings = page.locator('article.fr-placard')
        listings_count = listings.count()
        
        print(f"Found {listings_count} listings...")
        
        for list in listings.all():
            # Rental Type with fallback
            rental_type_locator = list.locator('div.flex.gap-2.mr-6.mb-1')
            if rental_type_locator.count() == 0:
                rental_type_locator = list.locator('p.font-semibold.truncate').first
            rental_type_text = rental_type_locator.inner_text().strip()
            
            # Address with fallback
            address_locator = list.locator('h2.text-sm.font-normal')
            if address_locator.count() == 0:
                address_locator = list.locator('address.text-sm.truncate').first
            address_text = address_locator.inner_text().strip()
            
            # Price
            price_locator = list.locator('p.pr-2.font-semibold')
            if price_locator.count() == 0:
                price_text = "N/A"
            else:
                price_text = price_locator.inner_text().strip()
            
            # Rental Size
            rental_size_locator = list.locator('p.border-l.border-border.px-2.uppercase')
            if rental_size_locator.count() == 0:
                rental_size_text = "N/A"
            else:
                rental_size_text = rental_size_locator.inner_text().strip()
            
            # Bath Size
            bath_size_locator = list.locator('p.border-l.border-border.pl-2.uppercase')
            if bath_size_locator.count() == 0:
                bath_size_text = "N/A"
            else:
                bath_size_text = bath_size_locator.inner_text().strip()
            
            # Contact
            contact_locator = list.locator('a span.hidden.sm\\:inline')
            if contact_locator.count() == 0:
                contact_text = "N/A"
            else:
                contact_text = contact_locator.inner_text().strip()

            data = {
                'rental_type': rental_type_text,
                'address': address_text,
                'Price': price_text,
                'rental_size': rental_size_text,
                'Bath_size': bath_size_text,
                'contact': contact_text
            }
            rental_list.append(data)
            
        print(f"Extracted {listings_count} listings from page {page_count} (Total: {len(rental_list)})")
        
        # Pagination handling
        next_button = page.locator('a.pagination-btn.right')
        
        if next_button.count() > 0:
            next_href = next_button.get_attribute('href')
            
            if next_href:
                if next_href.startswith('http'):
                    current_url = next_href
                elif next_href.startswith('/'):
                    current_url = base_url + next_href
                else:
                    current_url = base_url + '/' + next_href
                
                print(f"Next page found: {current_url}")
                page.wait_for_timeout(random.randint(3000, 6000))
            else:
                print("Next button has no href. Ending scrape.")
                current_url = None
        else:
            print("No next button found. Reached last page.")
            current_url = None
            
    # Write JSON to file
    out_dir = Path(r"C:\Users\Mteto\Desktop\Practice\forrentcamoufox")
    out_dir.mkdir(exist_ok=True, parents=True)
    out_file = out_dir / f"forrent_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_file.write_text(json.dumps(rental_list, indent=2, ensure_ascii=False), encoding="utf-8")
    
    print(f"\n{'='*60}")
    print(f"Scraping completed!")
    print(f"Total pages scraped: {page_count}")
    print(f"Total listings: {len(rental_list)}")
    print(f"Saved to: {out_file}")
    print(f"{'='*60}")

    page.close()