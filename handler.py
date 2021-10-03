import sys
import threading
import time
import requests

from datetime import datetime, timedelta

from settings import PROXY
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

# ToDo: refactoring
def send_buy_requests(product_id: str, amount: str) -> None:
    threads = list()
    product = Product(product_id=product_id,amount=amount)
    start_sale_time = product.get_start_time()

    while True:
        current_time = datetime.today()
        if start_sale_time <= (current_time + timedelta(seconds=11.5)):
            count_requests = 0
            for _ in range(1, 1000):
                count_requests += 1
                request = threading.Thread(
                    target=product.buy_product,
                    args=(PROXY,)
                )
                request.start()
                threads.append(request)
                time.sleep(0.13)

                if count_requests == 100:
                    print('The sale is over! Click CTRL+C or CTRL+Z')
                    time.sleep(10000)

            for thread in threads:
                thread.join()
