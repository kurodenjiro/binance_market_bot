from settings import BINANCE_SITEKEY, CAPTCHA_API_KEY

from twocaptcha import TwoCaptcha


def resolve_captcha() -> str:
    """result: dict = {'captchaId': '12345678', 'code': '03dAf...'}"""

    # your own API KEY from https://2captcha.com/enterpage
    solver = TwoCaptcha(apiKey=CAPTCHA_API_KEY)
    url = 'https://www.binance.com/en/nft/goods/detail?productId='

    result = solver.recaptcha(
        sitekey=BINANCE_SITEKEY,
        url=url + '8532619' + '&isProduct=1',
        version='v3',
        score='0.3'
    )
    code = result['code']
    return code
