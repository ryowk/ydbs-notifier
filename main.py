import os

import requests
from bs4 import BeautifulSoup
from slack_sdk import WebClient

PRODUCT_ID = os.environ['PRODUCT_ID']
SLACK_TOKEN = os.environ['SLACK_TOKEN']
SLACK_CHANNEL = os.environ['SLACK_CHANNEL']


def in_stock(soup: BeautifulSoup) -> bool:
    element = soup.select_one('#otodokeID')
    if element is None or 'お取り寄せ' in element.text:
        return False
    return True


if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    }
    url = f'https://www.yodobashi.com/product/{PRODUCT_ID}/'
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    if in_stock(soup):
        client = WebClient(token=SLACK_TOKEN)
        client.chat_postMessage(
            channel=SLACK_CHANNEL,
            text=f'<!channel>\n{url} is in stock'
        )
