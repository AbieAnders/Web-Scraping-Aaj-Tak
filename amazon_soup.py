import requests
from bs4 import BeautifulSoup

def main():
    url = "https://www.amazon.in/dp/B0932R8ZGD/"
    response = requests.get(url)
    if response.status_code == 200:
        webpage_html = BeautifulSoup(response.text, 'html.parser')
        with open('souped_html.txt', 'w', encoding = 'utf-8') as file:
            file.write(str(webpage_html))
        print("Souped HTML content has been saved to 'souped_html.txt'.")
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")

if __name__ == "__main__":
    main()