# Sample AI Conversation - Python Development Help

## Human:
I'm struggling with web scraping in Python. Can you help me understand the best practices and recommend some libraries?

## Claude:
I'd be happy to help you with Python web scraping! Here are the key libraries and best practices:

**Essential Libraries:**

1. **requests** - For making HTTP requests
2. **BeautifulSoup** - For parsing HTML
3. **Selenium** - For JavaScript-heavy sites
4. **Scrapy** - For large-scale scraping projects

**Best Practices:**

1. **Respect robots.txt** - Always check the site's robots.txt file
2. **Rate limiting** - Add delays between requests
3. **User agents** - Rotate user agent strings
4. **Error handling** - Handle network errors gracefully

**Basic Example:**

```python
import requests
from bs4 import BeautifulSoup
import time

def scrape_website(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract data here
        titles = soup.find_all('h2', class_='title')
        
        return [title.text.strip() for title in titles]
        
    except requests.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return []
    
    finally:
        time.sleep(1)  # Be respectful
```

## Human:
This is really helpful! What about handling dynamic content that loads with JavaScript?

## Claude:
Great question! JavaScript-rendered content requires different approaches:

**Option 1: Selenium (Most Common)**

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_dynamic_content(url):
    # Setup Chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run without GUI
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(url)
        
        # Wait for dynamic content to load
        wait = WebDriverWait(driver, 10)
        element = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "dynamic-content"))
        )
        
        # Now scrape the loaded content
        content = driver.find_elements(By.CSS_SELECTOR, ".data-item")
        
        return [item.text for item in content]
        
    finally:
        driver.quit()
```

**Option 2: Find the API (Best When Possible)**

Instead of scraping the rendered page, find the underlying API:

1. Open browser dev tools (F12)
2. Go to Network tab
3. Reload the page
4. Look for XHR/Fetch requests
5. Find the JSON API endpoint
6. Make direct requests to the API

```python
import requests

# Direct API call (much faster!)
api_url = "https://example.com/api/data"
response = requests.get(api_url)
data = response.json()
```

**Performance Tips:**
- Always try to find APIs first
- Use headless mode for better performance
- Implement proper waiting strategies
- Consider using browser pools for concurrent scraping