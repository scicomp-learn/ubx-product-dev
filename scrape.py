import argparse

import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError

import ubmerce.scrabl as bl
import ubtools.ubtools as ubtools


BL_SOURCE = [
    'https://www.bukalapak.com/c/handphone',
]
BL_BASE = 'https://bukalapak.com'


def get_user_input():
    """Read user query input."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'query', action='store', help='Query keywords',
        type=str
    )

    arg = parser.parse_args()

    return arg


def bl_data(url, param=None):
    """Collect data product from bukalapak."""
    soup, soup_url = bl.bl_make_soup(url=url, params=param)
    print(f'- [DONE] Scraping from {soup_url}')
    print('-- Extracting data..')
    basic_product = soup.find(name='div', class_='basic-products')
    product_title = pd.Series(
        [product_card.find('a', class_='product__name')['title']
            for product_card in basic_product.find_all(
                'article', class_='product-display'
            )],
        name='product title'
    )
    product_href = pd.Series(
        [BL_BASE + product_card.find('a', class_='product__name')['href']
            for product_card in basic_product.find_all(
                'article', class_='product-display'
        )],
        name='product url'
    )
    data_product = pd.concat([product_title, product_href], axis=1)
    print('- [DONE] Extracted')

    return data_product


if __name__ == "__main__":
    arg = get_user_input()
    PARAM = {
        'search[keywords]': arg.query,
        'page': 1,
    }
    print('-- Start scraping --')
    data = bl_data(url=BL_SOURCE[0], param=PARAM)
    ubtools.bl_to_csv(data)
