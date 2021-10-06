import sys
import threading
import time
from datetime import datetime, timedelta

import requests

from product import Product
from recaptcha import resolve_captcha


COUNT_REQUESTS = 50
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

def wrapped_captcha(captcha_results):
    captcha = resolve_captcha()
    captcha_results.append(captcha)

def prepare_captcha():
    threads = [None] * COUNT_REQUESTS

    for i in range(len(threads)):
        threads[i] = threading.Thread(
            target=wrapped_captcha,
            args=(captcha_results, ),
        )
        threads[i].start()

    for i in range(len(threads)):
        threads[i].join()

    return captcha_results

# ToDo: TOTAL refactoring
def send_buy_requests() -> None:
    product = Product()
    start_sale_time = product.get_start_time()
    threads = list()

    while True:
        current_time = datetime.today()
        if start_sale_time <= (current_time + timedelta(seconds=30)):
            print('Prepare captcha')
            captcha_list = prepare_captcha()
            print('Prepare completed')
            break

    while True:
        current_time = datetime.today()
        if start_sale_time <= (current_time + timedelta(seconds=1)):
            print('Start sale')
            counter = 0
            new_product = Product(amount=50)

            for _ in range(0, COUNT_REQUESTS):
                counter += 1
                if counter % 3 == 0:
                    new_product = Product(amount=50)

                request = threading.Thread(
                    target=new_product.buy_product,
                    args=(captcha_list.pop(), )
                )

                request.start()
                threads.append(request)
                time.sleep(0.14)

            for thread in threads:
                thread.join()

            print('Sale has been ended')
            sys.exit(0)
