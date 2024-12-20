import asyncio
import json
import pandas as pd
import httpx
from icecream import ic

async def getdata(dict1):
    filename = dict1["filename"]
    url = dict1["url"]

    # cookies = {
    #     'sajssdk_2015_cross_new_user': '1',
    #     'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22193d23afa3475-0ef24df5770b968-1e525636-1296000-193d23afa359ce%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22193d23afa3475-0ef24df5770b968-1e525636-1296000-193d23afa359ce%22%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkzZDIzYjAxM2NiMzEtMGQzZTUwN2NiYmYxYWMtMWU1MjU2MzYtMTI5NjAwMC0xOTNkMjNiMDEzZGUzNCJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%7D',
    #     'Hm_lvt_a19fd7224d30e3c8a6558dcb38c4beed': '1734404193',
    #     'HMACCOUNT': '9AB16716FC5BB47C',
    #     'acw_tc': '1a0c39d517344041940112848e0143fa67906f4c52c3aa30c08470c45426bb',
    #     'Hm_lpvt_a19fd7224d30e3c8a6558dcb38c4beed': '1734404279',
    # }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        # 'Cookie': 'sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22193d23afa3475-0ef24df5770b968-1e525636-1296000-193d23afa359ce%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22193d23afa3475-0ef24df5770b968-1e525636-1296000-193d23afa359ce%22%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkzZDIzYjAxM2NiMzEtMGQzZTUwN2NiYmYxYWMtMWU1MjU2MzYtMTI5NjAwMC0xOTNkMjNiMDEzZGUzNCJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%7D; Hm_lvt_a19fd7224d30e3c8a6558dcb38c4beed=1734404193; HMACCOUNT=9AB16716FC5BB47C; acw_tc=1a0c39d517344041940112848e0143fa67906f4c52c3aa30c08470c45426bb; Hm_lpvt_a19fd7224d30e3c8a6558dcb38c4beed=1734404279',
        'Origin': 'https://www.newrank.cn',
        'Referer': 'https://www.newrank.cn/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'content-type': 'application/json',
        'contenttype': 'application/json;charset=UTF-8',
        'n-token': '3b2f8f99af0545cc989cfae76477d9bf',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    json_data = {
        'rankType': 1,
        'rankDate': '2024-12-16',
        'type': '',
        'size': 50,
        'start': 1,
        'photoType': '',
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            # cookies=cookies,
            headers=headers,
            json=json_data,
        )
        try:
            # print(response.json())
            # response_json = json.loads(response.text)
            # # todo 转化为dict
            result_dict = response.json()
            my_list = result_dict.get('data').get('list')
            ic(len(my_list))
            # # todo 转化为DataFrame
            df = pd.DataFrame(my_list)
            # # todo 保存为xlsx文件
            df.to_excel(f'{filename}.xlsx', index=False)

        except json.JSONDecodeError:
            ic("json.JSONDecodeError")


async def main():
    xhs = "https://gw.newrank.cn/api/mainRank/nr/mainRank/hotContent/getXhsHotContent"
    weixin = "https://gw.newrank.cn/api/mainRank/nr/mainRank/hotContent/getWxHotContent"
    dy = "https://gw.newrank.cn/api/mainRank/nr/mainRank/hotContent/getDyHotContent"
    sph = "https://gw.newrank.cn/api/mainRank/nr/mainRank/hotContent/getSphHotContent"
    ks = "https://gw.newrank.cn/api/mainRank/nr/mainRank/hotContent/getKsHotContent"
    bilibili = "https://gw.newrank.cn/api/mainRank/nr/mainRank/hotContent/getBiliHotContent"

    dict_list = [
        {
            "filename": "xhs",
            "url": xhs
        },
        {
            "filename": "weixin",
            "url": weixin
        },
        {
            "filename": "dy",
            "url": dy
        },
        {
            "filename": "sph",
            "url": sph
        },
        {
            "filename": "ks",
            "url": ks
        },
        {
            "filename": "bilibili",
            "url": bilibili
        }
    ]

    tasks = []
    for dict1 in dict_list:
        task = getdata(dict1)
        tasks.append(task)

    # 使用gather方法进行并发

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())

