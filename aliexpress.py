

from bs4 import BeautifulSoup
import requests
from lxml import etree
import re

def get_product_link(product):
    base_url = f'https://www.aliexpress.com/wholesale?SearchText={product}'
    print(base_url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36'
    }
    max_attempts = 10  # Maximum number of attempts to find a valid link
    attempt = 1  # Current attempt

    while attempt <= max_attempts:
        try:
            response = requests.get(base_url, headers=headers)
            tree = etree.HTML(response.content)

            all_elements = tree.xpath('//*')
            href_list = []
            if all_elements:
                for element in all_elements:
                    href = element.xpath('./@href')
                    if href:
                        href_list.append(href[0])

                pattern = r'.*//www.aliexpress.com/item/.*'
                filtered_hrefs = [href for href in href_list if re.match(pattern, href)]
                if filtered_hrefs:
                    print(filtered_hrefs[0])
                    break  # Found a valid link, exit the loop

            print('No matching elements found.')
        except Exception as e:
            print(f'Error: {e}')

        attempt += 1

    print('Unable to find a valid link.')

get_product_link('smartwatch')




# def main(product):
#     base_url = f'https://www.aliexpress.com/w/wholesale-{product}.html?catId=0&initiative_id=SB_20230612232047&SearchText={product}&spm=a2g0o.home.1000002.0'
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36'
#     }

#     for _ in range(5):
#         print(base_url)
#         response = requests.get(base_url, headers=headers)
#         soup = BeautifulSoup(response.content, 'html.parser')

#         elements = soup.select('html > body > div:nth-of-type(5) > div:nth-of-type(1) > div > div:nth-of-type(2) > div > div:nth-of-type(2) > div:nth-of-type(3) > a:nth-of-type(2)')

#         if elements:
#             for element in elements:
#                 print(element.text)  # Get the text content of the element
#                 print(element['href'])  # Get the value of the href attribute
#             base_url = 'https:' + elements[-1]['href']
#         else:
#             print("Element not found.")
#             break



# import requests
# from bs4 import BeautifulSoup
# import requests
# from bs4 import BeautifulSoup

# def fetch(url):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36',
#     }

#     payload = {'url': url}

#     r = requests.get('http://api.scraperapi.com', params=payload, timeout=60, headers=headers)

#     if r.status_code == 200:
#         html = r.text.strip()
#         soup = BeautifulSoup(html, 'lxml')
#         links_section = soup.select('._3KNwG')
#         links = [link['href'] for link in links_section]
#         return links

#     return []

# fetch('https://www.aliexpress.com/w/wholesale-smart-watch.html?catId=0&initiative_id=SB_20230612232047&SearchText=smart+watch&spm=a2g0o.home.1000002.0')

