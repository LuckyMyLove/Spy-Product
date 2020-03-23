import pandas as pd
import sys
import tldextract
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def find_row(url):
    shops = {"shop": ["euro", "ceneo", "mediaexpert", "steampowered", "muve", "wearmedicine"],
             "main_container_id": ["product-top", "", "", "", "", ""],
             "main_container_class": ["", "js_product-body", "is-main", "page_content_ctn", "main-content",
                                      "product__cart"],
             "title_element": ["h1", "h1", "div", "div", "h1", "h1"],
             "title_id": ["", "", "", "", "", ""],
             "title_class": ["selenium-KP-product-name", "product-name", "c-offerBox_data", "apphub_AppName",
                             "site-hdr",
                             "product__title"],
             "price_element": ["div", "span", "div", "div", "p", "p"],
             "price_id": ["", "", "", "", "", ""],
             "price_class": ["price-normal", "price-format", "is-normalPrice", "game_purchase_price price", "pb-price",
                             "product__price"]}

    table = pd.DataFrame(data=shops)

    shop_name = tldextract.extract(url).domain

    if shop_name in table.values:
        shop_info = table.loc[table['shop'] == shop_name]
        index = int(shop_info.index.values)

        return shop_info, index

    else:
        print("%s is not on the list of supported stores" % shop_name)
        sys.exit()


def get_info(url: str):
    class product:
        def __init__(self, const_title, const_price, const_url):
            self.title = const_title
            self.price = const_price
            self.url = const_url
            self.date = datetime.now().strftime("%X %x")

    shop_info, index = find_row(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    result = soup.find(id=shop_info["main_container_id"][index]) if shop_info["main_container_class"][index] == "" else soup.find(class_=shop_info["main_container_class"][index])

    title = result.find(shop_info["title_element"][index], id=shop_info["title_id"][index]) if shop_info["title_class"][index] == "" else result.find(shop_info["title_element"][index], class_=shop_info["title_class"][index])
    price = result.find(shop_info["price_element"][index], id=shop_info["price_id"][index]) if shop_info["price_class"][index] == "" else result.find(shop_info["price_element"][index], class_=shop_info["price_class"][index])

    product = product(title.text.strip(), price.text.strip(), url)
    return product
