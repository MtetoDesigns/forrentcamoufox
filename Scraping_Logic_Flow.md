# Scraping Logic Flow - ForRent.com

## Overview
This document outlines the systematic approach for scraping rental property listings from ForRent.com using Camoufox (Firefox-based browser automation with anti-detection features).

---

## Scraping Workflow Checklist

### Step 1: Launch Browser
- [ ] Initialize Camoufox with fingerprint randomization
- [ ] Configure browser settings:
  - [ ] Set `headless=False` for debugging (switch to `True` for production)
  - [ ] Enable `humanize=2.0` for realistic human-like behavior
  - [ ] Set OS fingerprint to `windows`
- [ ] Create browser context with randomized fingerprints (prevents bot detection)

**Purpose**: Establish a stealthy browser session that mimics real user behavior and avoids anti-bot mechanisms.

---

### Step 2: Navigate
- [ ] Navigate to target URL (ForRent.com search results page)
- [ ] Wait for initial page load
- [ ] Monitor network requests (especially `GetViewportInfo` API calls)
- [ ] Verify page loaded successfully (check for error pages or CAPTCHAs)

**Purpose**: Reach the target page and ensure it's fully loaded before attempting to interact with it.

---

### Step 3: Wait for Content
- [ ] Wait for specific elements to appear (property cards, listings, etc.)
- [ ] Use `wait_for_load_state("networkidle")` to ensure all async requests complete
- [ ] Add additional timeout (`wait_for_timeout(10000)`) for JavaScript-rendered content
- [ ] Verify critical elements are present before proceeding

**Why this matters**: Modern websites like ForRent.com use JavaScript frameworks (React, Vue, etc.) that load data asynchronously. The initial HTML may be empty, and actual property data loads via API calls after page load.

---

### Step 4: Interact with Page
- [ ] **Scroll Actions**:
  - [ ] Scroll down to trigger lazy-loading of property listings
  - [ ] Use smooth scrolling to mimic human behavior
  - [ ] Wait between scroll actions (humanization)
  
- [ ] **Click Actions**:
  - [ ] Click "Load More" or "Show More Results" buttons
  - [ ] Handle pagination buttons (Next page, page numbers)
  - [ ] Click filters or sorting options if needed
  
- [ ] **Form Interactions** (if applicable):
  - [ ] Fill search filters (price range, bedrooms, etc.)
  - [ ] Submit search forms
  - [ ] Handle dropdowns and checkboxes

**Purpose**: Trigger dynamic content loading and navigate through multiple pages of results. Many sites only load 20-50 items initially and require interaction to load more.

---

### Step 5: Extract Data
- [ ] **Locate Elements**:
  - [ ] Use CSS selectors or XPath to find property cards
  - [ ] Identify data containers (price, address, bedrooms, etc.)
  
- [ ] **Pull Data**:
  - [ ] Extract text content (property titles, descriptions)
  - [ ] Extract attributes (image URLs, links, data-* attributes)
  - [ ] Parse structured data (JSON-LD, microdata)
  
- [ ] **Store Variables**:
  - [ ] Create data structures (lists, dictionaries)
  - [ ] Validate extracted data (check for None/empty values)
  - [ ] Format data consistently (clean whitespace, normalize formats)

**Data Points to Extract**:
- Property address
- Rental price
- Number of bedrooms/bathrooms
- Square footage
- Amenities
- Property images
- Contact information
- Listing URL

---

### Step 6: Repeat or Clean Up
- [ ] **Pagination Logic**:
  - [ ] Check if "Next" button exists and is enabled
  - [ ] Navigate to next page
  - [ ] Repeat Steps 3-5 for each page
  - [ ] Track current page number to avoid infinite loops
  - [ ] Set maximum page limit (e.g., scrape first 10 pages)
  
- [ ] **Data Storage**:
  - [ ] Save extracted data to file (JSON, CSV, database)
  - [ ] Implement incremental saves (don't lose data if script crashes)
  
- [ ] **Clean Up**:
  - [ ] Close browser context
  - [ ] Release resources
  - [ ] Log completion status

**Purpose**: Systematically collect data from all available pages and ensure proper resource cleanup.

---

## Analysis & Best Practices

### 🎯 Key Challenges for ForRent.com

1. **Anti-Bot Detection**
   - ForRent.com likely uses bot detection services (Cloudflare, PerimeterX, etc.)
   - **Solution**: Camoufox's fingerprint randomization + humanize feature
   - **Additional**: Add random delays between actions, vary mouse movements

2. **Dynamic Content Loading**
   - Property listings load via JavaScript/AJAX after initial page load
   - **Solution**: Use `wait_for_load_state("networkidle")` and element-specific waits
   - **Monitor**: Network requests (especially `GetViewportInfo` API)

3. **Pagination Strategy**
   - Unknown pagination type (infinite scroll vs. numbered pages vs. "Load More" button)
   - **Recommendation**: Inspect the site to determine pagination method
   - **Async Benefit**: Can scrape multiple pages concurrently

4. **Rate Limiting**
   - Too many requests too quickly will trigger blocks
   - **Solution**: Implement delays between page loads (3-5 seconds)
   - **Advanced**: Rotate user agents, use proxy rotation if needed

### 🚀 Async Advantages for Multi-Page Scraping

**Why Async is Essential**:
- **Concurrent Scraping**: Open multiple browser tabs/contexts to scrape different pages simultaneously
- **Efficiency**: While waiting for one page to load, process another
- **Scalability**: Easily scale from 10 pages to 100+ pages
- **Better Resource Usage**: Non-blocking I/O operations

**Example Async Pattern**:
```
Page 1 loading → Page 2 loading → Page 3 loading
    ↓                ↓                ↓
Page 1 extracting → Page 2 extracting → Page 3 extracting
```

Instead of sequential (slow):
```
Page 1 load → extract → Page 2 load → extract → Page 3 load → extract
```

### 📊 Data Quality Considerations

1. **Validation**
   - Check for missing data fields
   - Validate price formats (remove "$", "," characters)
   - Verify URLs are complete and valid

2. **Deduplication**
   - Same property may appear on multiple pages
   - Use unique identifiers (property ID, URL) to deduplicate

3. **Error Handling**
   - Some listings may have incomplete data
   - Handle missing elements gracefully (use try/except)
   - Log errors for later review

### ⚡ Performance Optimization

1. **Selective Loading**
   - Block unnecessary resources (ads, analytics, images if not needed)
   - Reduces page load time and bandwidth

2. **Parallel Processing**
   - Use `asyncio.gather()` to scrape multiple pages concurrently
   - Limit concurrency (e.g., max 5 pages at once) to avoid overwhelming the server

3. **Caching**
   - Cache already-scraped pages to avoid re-scraping
   - Useful for debugging and resuming interrupted scrapes

### 🛡️ Ethical & Legal Considerations

- **Respect robots.txt**: Check ForRent.com's robots.txt file
- **Rate Limiting**: Don't overwhelm their servers (1-2 requests per second max)
- **Terms of Service**: Review ForRent.com's ToS regarding scraping
- **Data Usage**: Only use scraped data for permitted purposes
- **User-Agent**: Identify your bot honestly in the user-agent string

---

## Next Steps

1. **Inspect ForRent.com Structure**
   - [ ] Identify HTML structure of property listings
   - [ ] Determine pagination method
   - [ ] Find API endpoints (if any) for direct data access

2. **Implement Extraction Logic**
   - [ ] Write selectors for each data field
   - [ ] Create data models/schemas
   - [ ] Test extraction on single page

3. **Build Pagination Handler**
   - [ ] Detect last page
   - [ ] Implement page navigation
   - [ ] Add error recovery for failed pages

4. **Scale with Async**
   - [ ] Implement concurrent page scraping
   - [ ] Add rate limiting and delays
   - [ ] Test with multiple pages

5. **Data Pipeline**
   - [ ] Choose storage format (JSON, CSV, Database)
   - [ ] Implement data validation
   - [ ] Add logging and monitoring

---

## Tools & Technologies

- **Browser Automation**: Camoufox (Playwright-based with anti-detection)
- **Language**: Python with async/await
- **Data Processing**: Pandas (for CSV/data manipulation)
- **Storage**: JSON files, SQLite, or PostgreSQL
- **Monitoring**: Logging module for tracking progress and errors
