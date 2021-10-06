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

        self.list_product_ids = ['8488265', '8487868', '8487744', '8487562', '8487438', '8487207', '8487070', '8485486', '8486232', '8484334', '8486343', '8486369', '8479174', '8486952', '8486795', '8486770', '8478929', '8476989', '8476391', '8472878', '8469844', '8471012', '8477962', '8477940', '8477922', '8472535', '8471925', '8471855', '8471838', '8471670', '8473284', '8473478', '8474093', '8474134', '8475921', '8490391', '8490261', '8490022', '8489980', '8488798', '8469814', '8470841', '8439724', '8479259', '8478999', '8477977', '8474108', '8475951', '8475978', '8472324', '8472142', '8471709', '8471076', '8487360', '8487144', '8487039', '8485531', '8479333', '8483804', '8486092', '8483833', '8486161', '8486454', '8484647', '8490321', '8488178', '8489730', '8488948', '8489957', '8489859', '8490374', '8490222', '8490061', '8490082', '8489930', '8489593', '8489287', '8488619', '8487841', '8490410', '8486981', '8479098', '8479071', '8479027', '8486820', '8473240', '8475901', '8469829', '8470811', '8477317', '8477058', '8476977', '8476730', '8476687', '8476645', '8472820', '8485444', '8486201', '8472480', '8471551',
        '8471061', '8487490', '8487457', '8487406', '8487023', '8483718', '8483768', '8483577', '8485702', '8486122', '8483987', '8472698', '8484357', '8486616', '8471688', '8471658', '8471526', '8471494', '8501254', '8490349', '8490241', '8490177', '8490097', '8490003', '8489903', '8488924', '8488853', '8488766', '8488659', '8488364', '8488341', '8488231', '8487699', '8487587', '8483782', '8485761', '8483659', '8483873', '8486276', '8484384', '8439761', '8469407', '8477844', '8476817', '8472648', '8486649', '8479271', '8479245', '8486844', '8478964', '8478028', '8476370', '8473228', '8472889', '8473443', '8475876', '8487539', '8487322', '8487285', '8490332', '8490296', '8490284', '8490117', '8490044', '8488245', '8487763', '8487716', '8489706', '8489680', '8489443', '8489045', '8489007', '8488978', '8488328', '8487669', '8487607', '8487341', '8487125', '8485860', '8483644', '8483361', '8486073', '8483844', '8486330', '8477826', '8477287', '8477167', '8477072', '8476387', '8471032', '8439784', '8469523', '8484686', '8476348', '8484667', '8484998', '8478948', '8478055', '8478012', '8477993'
        ]
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
                "rows": 100,
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
