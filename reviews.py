from selectorlib import Extractor
import requests 
import json 
from time import sleep
import csv
from dateutil import parser as dateparser
import bs4 as bs
# Create an Extractor by reading from the YAML file
headers = {
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }
e = Extractor.from_yaml_file('D:/pypj/amazon-review-scraper/selectors.yml')
ee = Extractor.from_yaml_file('D:/pypj/amazon-review-scraper/productCode.yml')
#keword = input("상품명을 입력해주세요:").replace(' ','+')
#productListUrl = 'https://www.amazon.com/s?k='+keword+'&s = review-rank' #상품 리스트 검색
testurl='https://www.amazon.com/s?k=rtx+4070+ti&s=review-rank'

def scrape(url):    
    # Download the page using requests
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    # Pass the HTML of the page and create 
    data = e.extract(r.text)
    print(data)
    return data

def scrapeProductCode():
    r = requests.get(testurl, headers=headers)
    if r.status_code > 500:
        if "상품 코드 파싱실패" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%productListUrl)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(productListUrl,r.status_code))
        return None
    soup = bs.BeautifulSoup(r.text, 'lxml')
    divList = soup.find_all('div', {'data-asin':True})
    return divList[7]

print(scrapeProductCode())

# product_data = []
# with open('D:/pypj/amazon-review-scraper/urls.txt','r', encoding='utf8') as urllist, open('D:/pypj/amazon-review-scraper/data.csv','w',encoding='utf8') as outfile:
#     writer = csv.DictWriter(outfile, fieldnames=["title","content","date","variant","images","verified","author","rating","product","url"],quoting=csv.QUOTE_ALL)
#     writer.writeheader()
#     for url in urllist.readlines():
#         data = scrape(url) 
#         if data:
#             for r in data['reviews']:
#                 r["product"] = data["product_title"]
#                 r['url'] = url
#                 if 'verified' in r:
#                     if 'Verified Purchase' in r['verified']:
#                         r['verified'] = 'Yes'
#                     else:
#                         r['verified'] = 'Yes'
#                 r['rating'] = r['rating'].split(' out of')[0]
#                 date_posted = r['date'].split('on ')[-1]
#                 if r['images']:
#                     r['images'] = "\n".join(r['images'])
#                 r['date'] = dateparser.parse(date_posted).strftime('%d %b %Y')
#                 writer.writerow(r)
#             # sleep(5)
    