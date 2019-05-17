"""Module to scrape bukalapak webpage"""

from boxing.boxfunc import get_html

import pandas as pd
# import requests
# from requests.exceptions import RequestException
from bs4 import BeautifulSoup


def bl_make_soup(url, params=None):
    """Get HTML string using `requests.get()` method.

    Parameters
    ----------
    url: str
        URL target to requests a HTTP GET method
    params: dict
        `param` to pass into `requests.get()` method

    Returns
    -------
    bs4.BeautifulSoup
        BeautifulSoup object
    """
    html, url = get_html(url=url, param=params)

    return BeautifulSoup(html, features='lxml'), url


def bl_count_product(url, param, page=1):
    """Count generaed product in for a `page`.

    Parameters
    ----------
    url: str
        URL target to requests a HTTP GET method
    param: dict
        `param` to pass into `requests.get()` method
    page: int
        Page number. (Default is 1)

    product_amount: `int`
        Amount of product in `page`
    """
    param['page'] = page
    soup = bl_make_soup(url=url, params=param)
    basic_product = soup.find('div', class_='basic-products')
    product_amount = len(basic_product.find_all(
        'article', class_='product-display'))

    return product_amount


def bl_count_page(soup):
    """Count page.

    Parameters
    ----------
    soup: BeautifulSoup
        BeautifulSoup object

    Returns
    -------
    max_page: int
        Number of generated page
    """
    pagination = soup.find('div', class_='pagination')
    last_page = pagination.find('span', class_='last-page')
    if last_page is None:
        max_page = int(pagination.find_all('a')[-2].get_text())
    else:
        max_page = int(last_page.get_text())

    return max_page
