import urllib3
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import json


def read_page(company, page_idx, headers, http):
    url = 'https://www.patenthub.cn/s'

    fields = {
        'p': str(page_idx),
        'q': company,
        'dm': 'list',
        's': 'score!',
        'ds': 'cn'
    }

    ret = http.request('GET', url, fields=fields, headers=headers)

    with StringIO(ret.data.decode('utf-8')) as f:
        tb_list = pd.read_html(f)

    return tb_list[0]


def main():
    http = urllib3.PoolManager()

    with open('./headers.json', 'r') as f:
        headers = json.load(f)

    with open('./query_list.txt', 'r') as f:
        query_list = f.readlines()

    for query in query_list:
        table_list = []

        query = query.strip()
        print(f"Searching for {query}...")

        idx = 0
        while True:
            idx += 1
            try:
                tb = read_page(query, idx, headers, http)
                tb = tb.loc[tb.apply(lambda row: query in row['申请人'], axis=1), :]
                table_list.append(tb)
            except:
                break
        tb = pd.concat(table_list)
        print(f'{tb.shape[0]} patents are found.')
        tb.to_csv(f'./output/{query}.csv', index=False)


# def test():
#     http = urllib3.PoolManager()
#
#     with open('./headers.json', 'r') as f:
#         headers = json.load(f)
#
#     read_page("海底捞控股有限公司", 100, headers, http)

if __name__=='__main__':
    main()
    # test()
