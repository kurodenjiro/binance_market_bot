import json
import random
import requests
from datetime import datetime

from settings import headers, PROXY


class Product:

    def __init__(self, product_id: str = '', amount: str = '50'):
        self.url_nft_list = 'https://www.binance.com/bapi/nft/v1/friendly/nft/artist-product-list'
        self.url_create_order = 'https://www.binance.com/bapi/nft/v1/private/nft/nft-trade/order-create'
        self.url_product_detail = 'https://www.binance.com/bapi/nft/v1/friendly/nft/nft-trade/product-detail'

        self.list_product_ids = self.set_list_products()
        self.product_id = random.choice(self.list_product_ids)
        self.amount = amount

    def set_list_products(self):
        list_products = self.get_list_products()['data']['rows']
        list_product_ids = list()
        for i in range(len(list_products)):
            list_product_ids.append(list_products[i]['productId'])

        return list_product_ids

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
                "rows": 50,
                "creatorId": "238153642"
            })
        )
        assert response.json()['success'] != False, 'Verification failed'
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

    def buy_product(self, captcha: str) -> None:
        headers['x-nft-checkbot-token'] = captcha
        body: dict = {
            'productId': self.product_id,
            'amount': self.amount,
            'tradeType': 0
        }

        response = requests.post(
            url=self.url_create_order, headers=headers,
            data=json.dumps(body), proxies={'http': f'http://{PROXY}/'}
        )
        print(response.json())
