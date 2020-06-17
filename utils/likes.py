from async_requests import make_requests, RequestData
from bs4 import BeautifulSoup
import asyncio
import json


def get_friends_likes(wall_ids, headers):
    table = {}
    loop = asyncio.get_event_loop()
    headers["X-Requested-With"] = "XMLHttpRequest"
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    urls = [
        RequestData(url=f"https://m.vk.com/like?",
                    params={
                        'act': 'members',
                        'object': wall_id,
                        'tab': 'friends'
                    },
                    data={},
                    headers=headers
        )
        for wall_id in wall_ids
    ]
    future = asyncio.ensure_future(make_requests(urls))
    result = loop.run_until_complete(future)

    for wall_id, r in zip(wall_ids, result):
        r = r.decode()
        parsed = json.loads(r)

        if 'type' in parsed:
            if parsed['type'] == 4:
                # token is expired
                raise Exception

        if 'html' in parsed:
            soup = BeautifulSoup(parsed['html'], 'lxml')
            hrefs = [i.get('href') for i in soup.select('div.pcont div.PageBlock div.upanel div.items a.inline_item') or []]
            if hrefs:
                table[wall_id] = hrefs
        else:
            print(parsed)
    return table
