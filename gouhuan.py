import json

import requests







def check(ll, dolt,headers):
    for id in ll:
        data = {
            'id': id,
            'doIt': dolt
        }
        resp = requests.post("http://120.26.197.64:8980/pigeonDataCollect/admin/check/alreadyChecked.html", data=data,headers=headers)
        print(resp.text)


data = {
    'proId': 1,
    'type': 9,
    'pageIndex': 0,
    'pageSize': 100,
    'sortField': '',
    'sortOrder': ''
}

headers = {
    "Cookie": 'JSESSIONID=03861FAE75F3C7AFE40480CBA2CE3622',
    'Host': '120.26.197.64:8980',
    'Pragma': 'no-cache',
    'Referer': 'http://120.26.197.64:8980/pigeonDataCollect/superLogin.html',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
}
response = requests.post("http://120.26.197.64:8980/pigeonDataCollect/admin/check/getUncheckList.html", data=data,
                         headers=headers)
#print(response.text)
result = json.loads(response.text)
#print(result)
rows = result['data']

ll = []
target = '2021年春季特比环售环暗插单'

for row in rows:
    print(row)
    if row['title'] == target:
        ll.append(row['id'])

()
print(len(ll))
print(ll)


headers2 = {
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh,en-US;q=0.9,en;q=0.8,zh-TW;q=0.7',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Length': '20',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'JSESSIONID=03861FAE75F3C7AFE40480CBA2CE3622',
    'Host': '120.26.197.64:8980',
    'Origin': 'http://120.26.197.64:8980',
    'Pragma': 'no-cache',
    'Referer': 'http://120.26.197.64:8980/pigeonDataCollect/admin/check/unCheckList.html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}
check(ll,3, headers2)
