import requests
from bs4 import BeautifulSoup
from typing import List
from langdetect import DetectorFactory, detect, detect_langs
DetectorFactory.seed = 0

def remove_br_tag(p_tag = "<strong>यह भी पढ़ें: <a href=https://www.aajtak.in/technology/tech-tips-and-tricks-/story/do-smartphones-cause-brain-cancer-who-new-study-reveals-truth-ttec-2031766-2024-09-05>क्या स्मार्टफोन से होता है ब्रेन कैंसर? WHO की लेटेस्ट रिपोर्ट में हुआ बड़ा खुलासा</a></strong>"):
    for br_tag in p_tag.find_all('br'):
        br_tag.decompose()
    return p_tag.get_text(strip = True)

def filter_text_by_language(text: str, target_language: str) -> List:
    try:
        if(len(text) < 5):
            print("Text too short to detect language reliably.")
            return False
        detected_language = detect_langs(text)
        #return detected_language == target_language
        return detected_language
    except Exception as e:
        print(f"Error detecting language: {e}")
        return False

def find_text(webpage_html: BeautifulSoup):
    extracted_text = []
    for tag in webpage_html.descendants:
        if tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'figcaption']:
            text = tag.get_text(strip = True)
            if text:
                extracted_text.append(text)
        elif tag.name == 'div':                                                      #<div class = "end_story_embed_label">
            if 'end_story_embed_label' in tag.get('class', []):
                text = tag.get_text(strip = True)
                if text:
                    extracted_text.append(text)
        elif tag.name == 'a':                                                        #<a title = "">
            if tag.get('title', []):
                text = tag.get_text(strip = True)
                if text:
                    extracted_text.append(text)
        #-------------------------------------------------------
        elif tag.name == 'p':
            processed_text = ""
            for nested_tag in tag.descendants:
                if nested_tag.name in ['br', 'strong', 'ul', 'a']:
                    processed_text += nested_tag.get_text(strip = True)
                if nested_tag.name == 'a' and nested_tag.get('title'):
                    processed_text += nested_tag.get('title', '')
            if processed_text.strip():
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
        #-------------------------------------------------------
    for text in extracted_text:
        print(text)

def main():
    print(filter_text_by_language("होम भारत उत्तर प्रदेश बिहार दिल्ली मध्य प्रदेश राजस्थान पंजाब हरियाणा पश्चिम बंगाल हिमाचल प्रदेश महाराष्ट्र झारखंड उत्तरा खंड छत्तीसगढ़ गुजरात जम्मू कश्मीर तेलंगाना मनोरंजन बॉलीवुड साउथ सिनेमा बिग बॉस", 'hi'))
    url = "https://www.aajtak.in/technology/tech-news/story/government-agency-cert-in-has-warning-for-android-users-ttec-dskc-2069715-2024-10-14"
    response = requests.get(url)
    webpage_html = BeautifulSoup(response.text, 'html.parser')
    find_text(webpage_html)

if __name__ == '__main__':
    main()