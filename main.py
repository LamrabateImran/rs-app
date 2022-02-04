from spiders.ulta import Ulta

# Simple test of the class
if __name__ == '__main__':
    # url example
    url = 'https://www.ulta.com/p/double-wear-makeup-pump-xlsImpprod16321438'
    ulta = Ulta(url)
    product_info = ulta.scrap_product_info()
    product_reviews = ulta.scrap_reviews()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
