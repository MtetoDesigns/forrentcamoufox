import asyncio
import random
import csv
import time
from camoufox.async_api import AsyncCamoufox

async def scrape_forrent_california():
    property_urls = set()
    scraped_data = []
    
    print("Starting scraper for ForRent.com California listings...")

    async with AsyncCamoufox(headless=False) as browser:
        page = await browser.new_page()
        
        # --- STAGE 1: PAGINATION & URL COLLECTION ---
        print("\n--- STAGE 1: PAGINATION & URL COLLECTION ---")
        
        for page_num in range(1, 4):  # Loop pages 1 to 3
            if page_num == 1:
                url = "https://www.forrent.com/find/CA/extras-View"
            else:
                url = f"https://www.forrent.com/find/CA/{page_num}/extras-View"
            
            print(f"Navigating to Page {page_num}...")
            try:
                await page.goto(url)
                await page.wait_for_load_state('networkidle')
                await asyncio.sleep(random.uniform(3, 6))
                
                # Extract property listing URLs
                # XPath: //div[@class="box-border relative flex flex-col justify-between pb-3 h-56"]/a/@href
                # We select the 'a' tag and then get the href attribute
                elements = await page.query_selector_all('xpath=//div[@class="box-border relative flex flex-col justify-between pb-3 h-56"]/a')
                
                page_urls_count = 0
                for element in elements:
                    href = await element.get_attribute('href')
                    if href:
                        full_url = f"https://www.forrent.com{href}"
                        property_urls.add(full_url)
                        page_urls_count += 1
                
                print(f"Page {page_num}/3 - Found {page_urls_count} URLs")
                
            except Exception as e:
                print(f"Error scraping page {page_num}: {e}")

        unique_urls_list = list(property_urls)
        print(f"\nStage 1 Complete. Total unique URLs found: {len(unique_urls_list)}")
        
        # --- STAGE 2: DETAIL EXTRACTION ---
        print("\n--- STAGE 2: DETAIL EXTRACTION ---")
        
        total_urls = len(unique_urls_list)
        
        for index, property_url in enumerate(unique_urls_list, 1):
            print(f"Scraping {index}/{total_urls}: {property_url}")
            
            property_data = {
                "URL": property_url,
                "Price": "N/A",
                "Address": "N/A",
                "Date": "N/A",
                "Contact": "N/A",
                "Bedrooms": "N/A",
                "Bathrooms": "N/A",
                "SqFt": "N/A",
                "Availability": "N/A"
            }
            
            try:
                await page.goto(property_url)
                await page.wait_for_load_state('networkidle')
                await asyncio.sleep(random.uniform(3, 6))
                
                # Helper to safely extract text
                async def get_text(xpath):
                    try:
                        el = await page.query_selector(f'xpath={xpath}')
                        return await el.inner_text() if el else "N/A"
                    except:
                        return "N/A"

                # Helper to safely extract attribute
                async def get_attr(xpath, attr):
                    try:
                        el = await page.query_selector(f'xpath={xpath}')
                        return await el.get_attribute(attr) if el else "N/A"
                    except:
                        return "N/A"

                # Extract details
                property_data["Price"] = await get_text('//span[@class="text-heading font-semibold text-4xl"]')
                property_data["Address"] = await get_text('//h1[@class="address text-base font-normal"]')
                property_data["Date"] = await get_attr('//time[@datetime]', 'datetime')
                property_data["Contact"] = await get_text('//a[@class="text-primary-text text-1.5xl font-semibold underline"]')
                
                # List items for details
                property_data["Bedrooms"] = await get_text('//ul[@class="grid grid-cols-2 sm:grid-cols-3 gap-2 mt-4 mb-3 md:flex"]/li[2]')
                property_data["Bathrooms"] = await get_text('//ul[@class="grid grid-cols-2 sm:grid-cols-3 gap-2 mt-4 mb-3 md:flex"]/li[3]')
                property_data["SqFt"] = await get_text('//ul[@class="grid grid-cols-2 sm:grid-cols-3 gap-2 mt-4 mb-3 md:flex"]/li[4]')
                property_data["Availability"] = await get_text('//ul[@class="grid grid-cols-2 sm:grid-cols-3 gap-2 mt-4 mb-3 md:flex"]/li[5]')
                
                scraped_data.append(property_data)
                
            except Exception as e:
                print(f"Error scraping details for {property_url}: {e}")
        
        # --- SAVE TO CSV ---
        csv_filename = 'forrent_ca_properties.csv'
        if scraped_data:
            fieldnames = ["URL", "Price", "Address", "Date", "Contact", "Bedrooms", "Bathrooms", "SqFt", "Availability"]
            try:
                with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(scraped_data)
                print(f"\nScraping complete! {len(scraped_data)} properties saved to {csv_filename}")
            except Exception as e:
                print(f"Error saving CSV: {e}")
        else:
            print("\nNo data scraped to save.")

if __name__ == "__main__":
    asyncio.run(scrape_forrent_california())
