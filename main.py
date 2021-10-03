from handler import headers_is_right, send_buy_requests
from settings import headers


headers_is_right(headers)

product_id = str(input('Enter productId: '))
amount = str(input('Enter nft`s price: '))

print('Start waiting')

send_buy_requests(product_id, amount)
