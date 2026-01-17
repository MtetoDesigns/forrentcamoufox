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
    
    current_url = "https://www.forrent.com/"
    base_url = "https://www.forrent.com/find/NY/metro-NYC/New+York"
    rental_list = []
    page_count = 0
    
    while current_url:
        page_count+= 1
        print(f"\n📖 Scraping page {page_count}...")
        
        # HTTP Request
        page.goto(current_url)
        
        
        
        
    

