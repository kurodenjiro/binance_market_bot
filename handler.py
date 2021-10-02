import sys
import random
import threading
import time
import requests

from datetime import datetime, timedelta

from product import Product


def headers_is_right(headers: dict) -> None:
    url_user_info = 'https://www.binance.com/bapi/accounts/v1/private/account/user/base-detail'
    response = requests.post(url_user_info, headers=headers)

    if response.status_code == 200:
        print('Successfully connected')
    else:
        print('Something wrong...')
        print('Check please: COOKIE, CSRFTOKEN, headers')
        sys.exit(1)

def get_random_proxy() -> str:
    try:
        with open('proxies.txt', 'r') as file:
            proxies = [proxy.replace('\n', '') for proxy in file.readlines()]
            return random.choice(proxies)
    except FileExistsError:
        print('Create file `proxies.txt` in file `nft_bot`')
        return ''

# ToDo: refactoring
def send_buy_requests(product_id: str = '', amount: str = '') -> None:
    threads = list()
    product = Product(amount=50)
    start_sale_time = product.get_start_time()

    while True:
        current_time = datetime.today()
        if start_sale_time >= (current_time + timedelta(seconds=12)):
            count_requests = 0
            for _ in range(1, 1000):
                count_requests += 1
                new_product = Product(amount=50)
                request = threading.Thread(
                    target=new_product.buy_product,
                    args=(get_random_proxy(),)
                )
                request.start()
                threads.append(request)
                time.sleep(0.13)

                if count_requests == 100:
                    time.sleep(10000)

                if start_sale_time <= (current_time - timedelta(seconds=3)):
                    print('The sale is over!')
                    sys.exit(0)

            for thread in threads:
                thread.join()
