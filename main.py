import argparse
from importlib import import_module
from utils import convert_file_to_list, save_as

# Simple test of the class
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--spider', action='store', dest='spider_name', help='Select which spider to use', required=True)
    parser.add_argument('--url', action='store', dest='product_url', help='Product url')
    parser.add_argument('--file', action='store', dest='file_location', help='Source file that contain list of products')
    parser.add_argument('--info', action='store_true', default=False, dest='product_info', help='Product details')
    parser.add_argument('--reviews',  action='store_true', dest='product_reviews', default=False, help='Product reviews')
    parser.add_argument('--save', action='store', dest='save_as', help='Save scraped data as')
    parser.add_argument('--version', action='version', version='ERS 1.0')
    args = parser.parse_args()
    spider_name = args.spider_name.lower()
    spider = getattr(import_module(f'spiders.{args.spider_name}'), spider_name.capitalize())
    # Check if a source to scrap is provided either single url or a file that contain multiple urls
    if not ((args.product_url or args.file_location) and (args.product_info or args.product_reviews)):
        exit("error: Please specify --url or --file parameters as well as --info or --reviews.")
    # Check if the supported file extension is provided.
    elif args.save_as:
        if args.save_as not in ['csv', 'xlsx', 'json']:
            exit('error: only csv, xlsx and json are supported now.')
    elif args.product_url:
        url = args.product_url
        data = spider(url=url)
        save_as(data, 'product_details', args.save_as)
    elif args.file_location:
        filelocation = args.file_location
        urls = convert_file_to_list(filelocation)
        data = spider(urls=urls)
        save_as(data, 'product_details', args.save_as)

