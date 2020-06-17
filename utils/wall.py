from async_requests import make_requests, RequestData
from bs4 import BeautifulSoup
import asyncio
import json


def get_wall_count(groups):
    table = {}
    urls = [RequestData(url=f"https://m.vk.com/public{group_id}", params={}, headers={}, data={}) for group_id in
            groups]
    loop = asyncio.get_event_loop()

    future = asyncio.ensure_future(make_requests(urls))
    result = loop.run_until_complete(future)
    for page, group_id in zip(result, groups):
        soup = BeautifulSoup(page, "lxml")
        try:
            text = ''.join(soup.find('h3', class_="slim_header_block_top").text.split(' ')[:-1])
            if text.strip() == 'Нет':
                table[group_id] = 0
            else:
                table[group_id] = int(text)
        except Exception as e:
            print(e)
    return table


def get_all_raw_wall(group_id, count):
    posts = ""
    urls = [RequestData(url=f"https://m.vk.com/public{group_id}",
                        params={'offset': 0, 'own': 1},
                        headers={'X-Requested-With': 'XMLHttpRequest'},
                        data={'_ajax': 1})] + \
           [RequestData(url=f"https://m.vk.com/public{group_id}",
                        params={'offset': offset, 'own': 1},
                        headers={'X-Requested-With': 'XMLHttpRequest'},
                        data={'_ajax': 1}) for offset in range(5, count, 10)]
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(make_requests(urls))
    result = loop.run_until_complete(future)
    for r in result:
        data = BeautifulSoup(json.loads(r)['data'][0], "lxml")
        posts += '\n'.join(map(str, data.find_all('div', class_="wall_item"))) + '\n'
    return posts


def process_posts(data):
    soup = BeautifulSoup(data, "lxml")
    print(len(soup.find_all("div", class_="wall_item")))


def get_last_n_posts(filename, n):
    return get_all_posts(filename)[:n]


def get_all_posts(filename):
    with open(filename, "r") as f:
        soup = BeautifulSoup(f.read(), "lxml")
    walls = [i.get('name') for i in soup.select('div.wall_item a.post__anchor')]
    return walls
