import requests
from bs4 import BeautifulSoup
from typing import List
from langdetect import detect, DetectorFactory

def is_valid_url(url: str) -> bool:
    return url.startswith('http://') or url.startswith('https://')

def fetch_sitemap(url: str) -> List:
    response = requests.get(url)
    if response.status_code == 200:
        '''try:
            soup = BeautifulSoup(response.content, 'lxml-xml') #only xml docs are present.
        except Exception as e:
            print(f"Error with 'lxml-xml' parser: {e}")
            try:
                soup = BeautifulSoup(response.content, 'xml')
            except Exception as e:
                print(f"Error with 'xml' parser: {e}")
                return []'''
        soup = BeautifulSoup(response.content, 'lxml-xml') #only xml docs are present.
        urls = [loc.text for loc in soup.find_all('loc')]
        return urls
    else:
        print(f"Failed to retrieve sitemap: {response.status_code}")
        return []

def remove_nested_br_tags(soup):
    for p_tag in soup.find_all('p'):
        for br_tag in p_tag.find_all('br'):
            br_tag.extract()

def fetch_page_text(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        webpage_html = BeautifulSoup(response.content, 'html.parser')
        #remove_nested_br_tags(webpage_html)
        extracted_text = []
        for tag in webpage_html.descendants:
            if tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'figcaption']:
                text = tag.get_text(strip = True)
                if text:
                    extracted_text.append(text)
            elif tag.name == 'div':
                if 'end_story_embed_label' in tag.get('class', []):
                    text = tag.get_text(strip = True)
                    if text:
                        extracted_text.append(text)
            elif tag.name == 'a':
                if tag.get('title', []):
                    text = tag.get_text(strip = True)
                    if text:
                        extracted_text.append(text)
            elif tag.name == 'p':
                remove_nested_br_tags(tag)

                processed_text = tag.get_text(strip = True)
                if processed_text:
                    extracted_text.append(processed_text)
            elif tag.name == 'li':
                processed_li_text = ""
                for nested_tag in tag.descendants:
                    if nested_tag.name == 'a' and nested_tag.get('title'):
                        processed_li_text += nested_tag.get('title', '')
                    if nested_tag.name == 'p':
                        processed_li_text += nested_tag.get_text(strip = True)
                    if nested_tag.name == 'li':
                        for deeper_nested_tag in nested_tag.descendants:
                            if deeper_nested_tag.name == 'a' and deeper_nested_tag.get('title'):
                                processed_li_text += deeper_nested_tag.get('title', '')
                            if deeper_nested_tag.name == 'p':
                                processed_li_text += deeper_nested_tag.get_text(strip = True)
                if processed_li_text.strip():
                    extracted_text.append(processed_li_text)

        for text in extracted_text:
            print(text)
        return ' '.join(extracted_text)  # Fixed variable name to extracted_text
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error fetching {url}: {e}")
        return ""
    except Exception as e:
        print(f"Error fetching or parsing {url}: {e}")
        return ""

def filter_text_by_language(text: str, target_language: str) -> bool:
    try:
        detected_language = detect(text)
        return detected_language == target_language
    except Exception as e:
        print(f"Error detecting language: {e}")
        return False

def main():
    DetectorFactory.seed = 0
    sitemaps = [
        'https://www.aajtak.in/rssfeeds/sitemap.xml',
        'https://www.aajtak.in/rssfeeds/news-sitemap.xml',
        'https://www.aajtak.in/rssfeeds/video-sitemap.xml',
        'https://www.aajtak.in/rssfeeds/image-sitemap.xml',
        'https://www.aajtak.in/visualstories/sitemap.xml'
    ]
    all_urls = []
    for sitemap_url in sitemaps:
        print(f"Fetching URLs from sitemap: {sitemap_url}")
        urls = fetch_sitemap(sitemap_url)
        all_urls.extend(url.strip() for url in urls)

    for url in all_urls:
        if is_valid_url(url):
            print(f"Fetching and parsing text from {url}")
            page_text = fetch_page_text(url)
            if filter_text_by_language(page_text, 'hi'):
                print(page_text[:500])
            else:
                print(f"Filtered out non-target language text from {url}")
        else:
            print(f"Invalid URL: {url}")

if __name__ == "__main__":
    main()