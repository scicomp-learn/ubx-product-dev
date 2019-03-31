"""Module comprises utility functions."""

from contextlib import closing
import os

import pandas as pd
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup


def get_html(url, param=None, time_out=None):
    """Attempts to get the html at `url` via HTTP GET Requests.

    Parameters
    ----------
    url : str
        URL or API URI
    param : dict
        key-value pair to be attached to url
    timeout : float or int or tuple of both
        time limit to establish a connection. If a tuple (2,5) is given, then
        2 is time limit to estalbish a connection and 5 is time limit to wait
        on a response.

    Returns
    -------
    str
        Raw HTML
    str
        Complete URL
    """
    try:
        with closing(
            requests.get(url, params=param, timeout=time_out, stream=True)
        ) as response:
            response.raise_for_status()
            if is_good_response(response):
                return response.text, response.url
            else:
                return None
    except RequestException as request_error:
        error_log(url, params=param, msg=request_error)
        return None


def is_good_response(response):
    """Evaluate response.

    If response seems to be HTML with status 200, return True.
    else, return False

    Parameters
    ----------
    response
        Requests response

    Returns
    -------
    bool
        Response quality
    """
    content_type = response.headers['Content-Type'].lower()
    return (
        response.status_code == 200
        and content_type is not None
        and content_type.find('html') > -1
    )


def error_log(url, params=None, msg=None):
    """Print error message and log them if exist.

    Parameters
    ----------
    url : str
        URL string
    params : dict
        key-value pair attached to url
    msg : str
        Error message based on `RequestException`
    """
    print(
        f'Error occured during request to {url}',
        f'with paremeter {params}',
        f'Error Message {msg}',
        sep='\n'
    )


def bl_to_csv(data):
    """Export collected data into csv file.

    Parameters
    ----------
    data : pandas.DataFrame
        Collected data
    """
    filename = os.path.join('data/bukalapak/raw', 'bl_data_product.csv')
    cols = list(data.columns)
    print(f'- Saving data to {filename}..')
    try:
        data.to_csv(
            filename, columns=cols, index=False
        )
    except Exception as error:
        print(f'Error while saving: {error}')
    else:
        print(f'- [DONE] Saved in {filename}')
