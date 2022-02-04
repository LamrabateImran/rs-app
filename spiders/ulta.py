import json
import requests
from bs4 import BeautifulSoup
import pandas as pd


class Ulta:
    def __init__(self, url):
        self.url = url

    # parse the ld+json that contain product information from teh html source page
    def parse_ld_json(self, soup):
        ld_json = soup.findAll('script', {'type': 'application/ld+json'})
        ld_json = [json.loads(ld.text) for ld in ld_json if 'product' in ld.text.lower()]
        if len(ld_json) != 0:
            ld_json = ld_json[0]
        else:
            ld_json = None
        return ld_json

    def parse_review(self, rev):
        parsed_review = dict()
        review = rev['details']
        metrics = rev['metrics']
        parsed_review['product_url'] = self.url
        if review.get('comments'):
            parsed_review['comments'] = review['comments']
        else:
            parsed_review['comments'] = None
        if review.get('headline'):
            parsed_review['headline'] = review['headline']
        else:
            parsed_review['headline'] = None
        if review.get('brand_base_url'):
            parsed_review['brand_base_url'] = review['brand_base_url']
        else:
            parsed_review['brand_base_url'] = None
        if review.get('brand_name'):
            parsed_review['brand_name'] = review['brand_name']
        else:
            parsed_review['brand_name'] = None
        if review.get('nickname'):
            parsed_review['nickname'] = review['nickname']
        else:
            parsed_review['nickname'] = None
        if review.get('source'):
            parsed_review['source'] = review['source']
        else:
            parsed_review['source'] = None
        if review.get('location'):
            parsed_review['location'] = review['location']
        else:
            parsed_review['location'] = None
        if review.get('created_date'):
            parsed_review['created_date'] = review['created_date']
        else:
            parsed_review['created_date'] = None
        if review.get('updated_date'):
            parsed_review['updated_date'] = review['updated_date']
        else:
            parsed_review['updated_date'] = None
        if review.get('bottom_line'):
            parsed_review['bottom_line'] = review['bottom_line']
        else:
            parsed_review['bottom_line'] = None
        if review.get('product_page_id'):
            parsed_review['product_page_id'] = review['product_page_id']
        else:
            parsed_review['product_page_id'] = None
        if metrics.get('helpful_votes'):
            parsed_review['helpful_votes'] = metrics['helpful_votes']
        else:
            parsed_review['helpful_votes'] = None
        if metrics.get('not_helpful_votes'):
            parsed_review['not_helpful_votes'] = metrics['not_helpful_votes']
        else:
            parsed_review['not_helpful_votes'] = None
        if metrics.get('rating'):
            parsed_review['rating'] = metrics['rating']
        else:
            parsed_review['rating'] = None
        if metrics.get('helpful_score'):
            parsed_review['helpful_score'] = metrics['helpful_score']
        else:
            parsed_review['helpful_score'] = None
        return parsed_review

    def check_review(self, ld_json):
        if ld_json.get('aggregateRating'):
            product_rating_value = ld_json['aggregateRating']['ratingValue']
            product_review_count = ld_json['aggregateRating']['reviewCount']
        else:
            product_rating_value = None
            product_review_count = None
        return product_rating_value, product_review_count

    def scrap_product_info(self):
        product = None
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            ld_json = self.parse_ld_json(soup)
            if ld_json:
                product_id = ld_json['productID']
                product_name = ld_json['name']
                product_description = ld_json['description']
                product_brand = ld_json['brand']
                price = ld_json['offers']['price']
                product_rating_value, product_review_count = self.check_review(ld_json)
                product_image = ld_json['image']
                product = {
                    'product_id': product_id,
                    'product_name': product_name,
                    'product_description': product_description,
                    'product_brand': product_brand,
                    'price': price,
                    'product_rating_value': product_rating_value,
                    'product_review_count': product_review_count,
                    'product_image': product_image,
                }
            else:
                print('No ld_json found, contact us or check if there is an ld_json in the html page source code')
        elif str(response.status_code)[:2] == '40':
            print('url not found')
        return product

    def scrap_reviews(self):
        reviews = []
        pimprod = self.url.split('-')[-1]
        api_url = f'https://display.powerreviews.com/m/6406/l/en_US/product/{pimprod}/reviews?paging.from=0&paging.size=25&filters=&search=&sort=Newest&image_only=false&_noconfig=true&apikey=daa0f241-c242-4483-afb7-4449942d1a2b'
        response = requests.get(api_url)
        data = response.json()
        pages_total = data['paging']['pages_total']
        next_from = 0
        for _ in range(pages_total):
            next_page = f'https://display.powerreviews.com/m/6406/l/en_US/product/{pimprod}/reviews?paging.from={next_from}&paging.size=20&filters=&search=&sort=Newest&image_only=false&_noconfig=true&apikey=daa0f241-c242-4483-afb7-4449942d1a2b'
            response = requests.get(next_page)
            data = response.json()
            reviews_list = data['results'][0]['reviews']
            for review in reviews_list:
                reviews.append(self.parse_review(review))
            next_from += 25
        return reviews
