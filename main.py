from handler import headers_is_right, send_buy_requests
from settings import headers


headers_is_right(headers)

print('Start waiting')

send_buy_requests()
