import requests
import time
import random
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import urllib.robotparser

# Function to check if scraping is allowed based on robots.txt
def can_fetch(url, user_agent='*'):
    rp = urllib.robotparser.RobotFileParser()
    robots_url = url + "/robots.txt"
    try:
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch(user_agent, url)
    except Exception as e:
        print(f"Error accessing {robots_url}: {e}")
        return False

# Function to mimic human-like interaction
def human_like_interaction(driver):
    driver.execute_script("window.scrollTo(0, 500);")  # Scroll down
    time.sleep(random.uniform(1, 3))  # Random sleep
    action = ActionChains(driver)
    action.move_by_offset(random.randint(0, 100), random.randint(0, 100)).perform()  # Random mouse move

# Function to make a simple HTTP request with random User-Agent
def fetch_page(url, proxies=None):
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    response = requests.get(url, headers=headers, proxies=proxies)
    time.sleep(random.uniform(1, 3))  # Mimic delay between requests
    return response

def main():
    url = 'http://google.com'
    
    # Check if scraping is allowed by robots.txt
    if can_fetch(url):
        print(f"Scraping allowed for {url}")
    else:
        print(f"Scraping blocked for {url}")
        return
    
    # Make a request using random User-Agent
    response = fetch_page(url)
    print("Page content fetched via requests: \n", response.text[:100])  # Print first 100 chars of the page content

    # Set up Selenium WebDriver (for JS-heavy sites)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode for performance
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
    driver.get(url)
    print("Page title via Selenium: \n", driver.title)

    # Simulate human-like interaction
    human_like_interaction(driver)

    driver.quit()

if __name__ == "__main__":
    main()