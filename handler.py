import sys
import threading
import time
from datetime import datetime, timedelta

import requests

from product import Product
from recaptcha import resolve_captcha
from settings import PROXY


COUNT_REQUESTS = 5
captcha_results = list()


def headers_is_right(headers: dict) -> None:
    url_user_info = 'https://www.binance.com/bapi/accounts/v1/private/account/user/base-detail'
    response = requests.post(url_user_info, headers=headers)

    if response.status_code == 200:
        print('Successfully connected')
    else:
        print('Something wrong...')
        print('Check please: COOKIE, CSRFTOKEN, headers')
        sys.exit(1)

def wrapped_captcha(product_id, captcha_results):
    captcha = resolve_captcha(product_id)
    captcha_results.append(captcha)

def prepare_captcha(product_id):
    threads = [None] * COUNT_REQUESTS

    for i in range(len(threads)):
        threads[i] = threading.Thread(
            target=wrapped_captcha,
            args=(product_id, captcha_results),
        )
        threads[i].start()

    for i in range(len(threads)):
        threads[i].join()

    return captcha_results

# ToDo: refactoring
def send_buy_requests(product_id: str, amount: str) -> None:
    product = Product(product_id=product_id,amount=amount)
    start_sale_time = product.get_start_time()
    captcha_list = prepare_captcha(product_id)
    threads = list()

    while True:
        current_time = datetime.today()
        if start_sale_time >= (current_time + timedelta(seconds=0.2)):
            print('Start sale')
            for _ in range(0, COUNT_REQUESTS):
                request = threading.Thread(
                    target=product.buy_product,
                    args=(PROXY, captcha_list.pop())
                )
                request.start()
                threads.append(request)
                time.sleep(0.15)

            for thread in threads:
                thread.join()

            print('Sale has been ended')
            sys.exit(0)
