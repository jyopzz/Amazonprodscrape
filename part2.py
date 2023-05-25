import requests
from bs4 import BeautifulSoup
import sys
import csv

def scrape(url, num_pages):
    headers = {
        'User-Agent': ' ',#user-agent
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    
    All_Items = []

    for page in range(1, num_pages + 1):
        page_url = url + '&page=' + str(page)
        response = requests.get(page_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        items = soup.find_all('div', {'data-component-type': 's-search-result'})
        
        for i in items:
            # Extracting Item URL
            items_url = i.find('a', {'class': 'a-link-normal s-no-outline'}).get('href')
            items_url = 'https://www.amazon.in' + items_url

            # Extracting Item Name
            name = i.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).text.strip()

            # Extracting Item Price
            price_item = i.find('span', {'class': 'a-price-whole'})
            price = price_item.text.strip() if price_item else 'N/A'

            # Extracting i rating
            rating_item = i.find('span', {'class': 'a-icon-alt'})
            rating = rating_item.text.strip() if rating_item else 'N/A'

            # Extracting number of reviews
            review_item = i.find('span', {'class': 'a-size-base'}).text.strip()
            no_of_review = review_item.split()[0]

            i_info = {
                'Item URL': items_url,
                'Item Name': name,
                'Item Price': price,
                'Rating': rating,
                'Number of Reviews': no_of_review
            }

            All_Items.append(i_info)

    return All_Items

def scrape2(items_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    
    response = requests.get(items_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extracting description
    
    description_list = []
    description_elements = soup.find_all('span', {'id': 'productTitle'})
    for description_element in description_elements:
        description = description_element.get_text(strip=True)
        description_list.append(description)

    # Extracting ASIN
    item_asin = soup.find('div', {'data-asin': True})
    asin = item_asin['data-asin'] if item_asin else 'N/A'

    

    # Extracting product description
    productdesc_list = []
    product_descriptions = soup.find_all('ul', {'class': 'a-unordered-list a-vertical a-spacing-mini'})
    for product_description in product_descriptions:
        prod_descr = product_description.get_text(strip=True)
        productdesc_list.append(prod_descr)

    # Extracting manufacturer
    item_manufacturer = soup.find('a', {'id': 'bylineInfo'})
    manufacturer = item_manufacturer.string.strip() if item_manufacturer else 'N/A'
    


    product_details = {
        'Description': description_list,
        'ASIN': asin,
        'Product Description':productdesc_list ,
        'Manufacturer': manufacturer
    }

    return product_details

#url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1'
num_pages = 20
url = input("Enter your url: ")
print("Generating the data...")
print("please wait...")
items = scrape(url, num_pages)

# Set the correct encoding for printing
sys.stdout.reconfigure(encoding='utf-8')


for i in items:
    print('Item URL:', i['Item URL'])
    print('Item Name:', i['Item Name'].encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding))
    print('Item Price:', i['Item Price'])
    print('Rating:', i['Rating'])
    print('Number of Reviews:', i['Number of Reviews'])
    print('***********************************')
print("Generating second data and write to csv file")
print("Please wait...")
#convert the data to CSV format
filename = 'itemlist2.csv'

with open(filename, 'w', encoding='utf-8', newline='') as csvfile:
    fieldnames = ['Item Name', 'Item URL','Item Price', 'Rating', 'Number of Reviews','Description', 'ASIN', 'Product Description', 'Manufacturer']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for i in items:
        item_url = i['Item URL']
        product_details = scrape2(item_url)
        i.update(product_details)
        writer.writerow(i)

print('Data exported :', filename)