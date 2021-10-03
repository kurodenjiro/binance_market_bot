import json
import requests
import random
from datetime import datetime

from recaptcha import resolve_captcha
from settings import headers


class Product:

    def __init__(self, product_id: str, amount: str):
        self.url_nft_list = 'https://www.binance.com/bapi/nft/v1/friendly/nft/artist-product-list'
        self.url_create_order = 'https://www.binance.com/bapi/nft/v1/private/nft/nft-trade/order-create'
        self.url_product_detail = 'https://www.binance.com/bapi/nft/v1/friendly/nft/nft-trade/product-detail'
        self.product_id = product_id
        self.amount = amount

    def get_list_products(self):
        response = requests.post(
            url=self.url_nft_list, headers=headers,
            data=json.dumps({
                "reSale": "",
                "tradeType": 0,
                "currency": "",
                "amountFrom": "",
                "amountTo": "",
                "keyword": "",
                "orderBy": "amount_sort",
                "orderType": 1,
                "page": 1,
                "rows": 96,
                "creatorId": "238153642"
            })
        )
        return response.json()

    def get_info_nft(self) -> dict:
        response = requests.post(
            url=self.url_product_detail,
            data=json.dumps({'productId': self.product_id}), headers=headers
        )
        return response.json()

    def get_start_time(self) -> datetime:
        response = self.get_info_nft()
        start_time = response['data']['productDetail']['setStartTime']
        start_sale_time = datetime.fromtimestamp(start_time/1000)

        return start_sale_time

    def buy_product(self, proxy: str, captcha: str) -> None:
        headers['x-nft-checkbot-token'] = captcha
        body: dict = {
            'productId': self.product_id,
            'amount': self.amount,
            'tradeType': 0
        }

        response = requests.post(
            url=self.url_create_order, headers=headers,
            data=json.dumps(body), proxies={'http': f'http://{proxy}/'}
        )
        print(response.json())
