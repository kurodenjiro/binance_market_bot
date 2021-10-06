import threading
from twocaptcha import TwoCaptcha

from settings import BINANCE_SITEKEY, CAPTCHA_API_KEY, COUNT_REQUESTS


class Recaptcha:

    def __init__(self):
        self.captcha_results = list()

    def resolve_captcha(self, product_id: str) -> str:
        """result: dict = {'captchaId': '12345678', 'code': '03dAf...'}"""

        # your own API KEY from https://2captcha.com/enterpage
        solver = TwoCaptcha(apiKey=CAPTCHA_API_KEY)
        url = 'https://www.binance.com/en/nft/goods/detail?productId='

        result = solver.recaptcha(
            sitekey=BINANCE_SITEKEY,
            url=url + str(product_id) + '&isProduct=1',
            version='v3',
            score='0.3'
        )
        code = result['code']
        return code

    def wrapped_captcha(self, product_id: str) -> None:
        captcha = self.resolve_captcha(product_id)
        self.captcha_results.append(captcha)

    def prepare_captcha(self, product_id: str) -> list:
        threads = [None] * COUNT_REQUESTS

        for i in range(len(threads)):
            threads[i] = threading.Thread(
                target=self.wrapped_captcha,
                args=(product_id, ),
            )
            threads[i].start()

        for i in range(len(threads)):
            threads[i].join()

        return self.captcha_results
