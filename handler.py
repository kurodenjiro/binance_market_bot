import sys
import threading
import time
from datetime import datetime, timedelta

import requests

from product import Product
from recaptcha import Recaptcha
from settings import COUNT_REQUESTS


def headers_is_right(headers: dict) -> None:
    url_user_info = 'https://www.binance.com/bapi/accounts/v1/private/account/user/base-detail'
    response = requests.post(url_user_info, headers=headers)

    if response.status_code == 200:
        print('Successfully connected')
    else:
        print('Something wrong...')
        print('Check please: COOKIE, CSRFTOKEN, headers')
        sys.exit(1)

def send_buy_requests(product_id: str, amount: str) -> None:
    product = Product(product_id, amount)
    captcha = Recaptcha()
    start_sale_time = product.get_start_time()
    threads = list()

    while True:
        current_time = datetime.today()
        if start_sale_time <= (current_time + timedelta(seconds=30)):
            print('Prepare captcha')
            captcha_list = captcha.prepare_captcha(product_id)
            print('Prepare completed')
            break

    while True:
        current_time = datetime.today()
        if start_sale_time <= (current_time + timedelta(seconds=3)):
            print('Start sale')
            for _ in range(0, COUNT_REQUESTS):
                request = threading.Thread(
                    target=product.buy_product,
                    args=(captcha_list.pop(), )
                )

                request.start()
                threads.append(request)
                time.sleep(0.14)

            for thread in threads:
                thread.join()

            print('Sale has been ended')
            sys.exit(0)
