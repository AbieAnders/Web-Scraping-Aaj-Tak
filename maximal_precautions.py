import requests
from stem import Signal
from stem.control import Controller

import time
import random
from fake_useragent import UserAgent

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import urllib.robotparser
from urllib.request import urlopen

def can_fetch_bot(url, user_agent = '*'):
    rp = urllib.robotparser.RobotFileParser()
    robots_url = url + "/robots.txt"
    try:
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch(user_agent, url)
    except Exception as e:
        print(f"Error accessing {robots_url}: {e}")
        return False

# Function to signal a new Tor circuit
def change_tor_circuit():
    with Controller.from_port(port = 9151) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)

# Function to mimic human-like interaction on a webpage using Selenium
def human_like_interaction(driver):
    # Scroll down to simulate user scrolling
    driver.execute_script("window.scrollTo(0, 500);")
    time.sleep(random.uniform(1, 3))  # Random sleep to simulate thinking time
    
    # Simulate mouse movement to random position
    action = ActionChains(driver)
    action.move_by_offset(random.randint(0, 100), random.randint(0, 100)).perform()
    time.sleep(random.uniform(1, 2))  # Sleep after mouse movement

def main():
    # Introduce a random sleep to simulate human-like delay
    #time.sleep(random.uniform(1, 3))

    # Change the Tor circuit for anonymity
    change_tor_circuit()

    # Set up proxies to route traffic through Tor
    _proxies = {
        'http': 'socks5h://127.0.0.1:9150',
        'https': 'socks5h://127.0.0.1:9150',
    }

    # Make a request using the Tor proxy and random User-Agent
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    response = requests.get('http://google.com', headers = headers, proxies = _proxies)
    print("IP via requests with User-Agent: \n", response.text)

    # Set up Selenium WebDriver with Chrome to use the Tor proxy
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (no GUI)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size = 1920x1080')
    options.add_argument('--proxy-server = socks5://127.0.0.1:9150')  # Use Tor proxy for Selenium

    # Initialize WebDriver and navigate to the page
    driver = webdriver.Chrome(service = ChromeService(ChromeDriverManager().install()), options = options)
    driver.get('http://google.com')

    print("Page title via Selenium: \n", driver.title)

    # Simulate human-like interaction on the webpage
    human_like_interaction(driver)
    
    driver.quit()

# Check if scraping a particular URL is allowed according to robots.txt
url = 'http://google.com'
if can_fetch_bot(url):
    print(f"Scraping allowed for {url}")
else:
    print(f"Scraping blocked for {url}")

if __name__ == "__main__":
    main()