# -*- coding: utf-8 -*-

import requests
from lxml import etree

prefix = "https://w.linovelib.com";
cookies = {
    'night': '0',
    'Hm_lvt_d29ecd95ff28d58324c09b9dc0bee919': '1662254581',
    '_ga': 'GA1.2.1284147034.1662254582',
    '_gid': 'GA1.2.1212734172.1662254582',
    'jieqiVisitId': 'article_articleviews%3D2939%7C2547%7C2014%7C2552%7C1375%7C4%7C2646',
    '__gads': 'ID=66025a53cb10478c-22fa15592dd6004d:T=1662254758:RT=1662254758:S=ALNI_MakO06Lx3kqXwz7joQn3KtnOCsaeg',
    '__gpi': 'UID=0000096f6ea6225c:T=1662254758:RT=1662254758:S=ALNI_MZZRZpQ8JqQxyd0g_OitwY4C51jQw',
    'PHPSESSID': 'b6pgbkd6n6vqslop1ntqgnf9gn',
    'jieqiUserInfo': 'jieqiUserId%3D757713%2CjieqiUserUname%3Dhuthe%2CjieqiUserName%3Dhuthe%2CjieqiUserGroup%3D3%2CjieqiUserGroupName%3D%E6%99%AE%E9%80%9A%E4%BC%9A%E5%91%98%2CjieqiUserVip%3D0%2CjieqiUserHonorId%3D1%2CjieqiUserHonor%3D%E5%A4%A9%E7%84%B6%2CjieqiUserToken%3D3c8f91a2a3ad1b8481db5cd1b00cf390%2CjieqiCodeLogin%3D0%2CjieqiCodePost%3D0%2CjieqiUserLogin%3D1662254807',
    'jieqiVisitInfo': 'jieqiUserLogin%3D1662254807%2CjieqiUserId%3D757713',
    'jieqiRecentRead': '2646.120661.0.1.1662255932.757713-1375.51987.0.1.1662256087.757713-2552.93021.0.3.1662256435.757713',
    'Hm_lpvt_d29ecd95ff28d58324c09b9dc0bee919': '1662256436',
}

headers = {
    'authority': 'w.linovelib.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'night=0; Hm_lvt_d29ecd95ff28d58324c09b9dc0bee919=1662254581; _ga=GA1.2.1284147034.1662254582; _gid=GA1.2.1212734172.1662254582; jieqiVisitId=article_articleviews%3D2939%7C2547%7C2014%7C2552%7C1375%7C4%7C2646; __gads=ID=66025a53cb10478c-22fa15592dd6004d:T=1662254758:RT=1662254758:S=ALNI_MakO06Lx3kqXwz7joQn3KtnOCsaeg; __gpi=UID=0000096f6ea6225c:T=1662254758:RT=1662254758:S=ALNI_MZZRZpQ8JqQxyd0g_OitwY4C51jQw; PHPSESSID=b6pgbkd6n6vqslop1ntqgnf9gn; jieqiUserInfo=jieqiUserId%3D757713%2CjieqiUserUname%3Dhuthe%2CjieqiUserName%3Dhuthe%2CjieqiUserGroup%3D3%2CjieqiUserGroupName%3D%E6%99%AE%E9%80%9A%E4%BC%9A%E5%91%98%2CjieqiUserVip%3D0%2CjieqiUserHonorId%3D1%2CjieqiUserHonor%3D%E5%A4%A9%E7%84%B6%2CjieqiUserToken%3D3c8f91a2a3ad1b8481db5cd1b00cf390%2CjieqiCodeLogin%3D0%2CjieqiCodePost%3D0%2CjieqiUserLogin%3D1662254807; jieqiVisitInfo=jieqiUserLogin%3D1662254807%2CjieqiUserId%3D757713; jieqiRecentRead=2646.120661.0.1.1662255932.757713-1375.51987.0.1.1662256087.757713-2552.93021.0.3.1662256435.757713; Hm_lpvt_d29ecd95ff28d58324c09b9dc0bee919=1662256436',
    'pragma': 'no-cache',
    'referer': 'https://w.linovelib.com/novel/2552/93021_3.html',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
}

# response = requests.get('https://w.linovelib.com/novel/2552/93021_2.html', cookies=cookies, headers=headers)
# response = requests.get('https://w.linovelib.com/novel/2552/catalog', cookies=cookies, headers=headers)

def fetch_novel(n_id):
    print(f"will fetch {n_id}")
    resp = requests.get(f'https://w.linovelib.com/novel/{n_id}/catalog', cookies=cookies, headers=headers)
    doc = etree.HTML(resp.text)
    l = doc.xpath('//li[@class="chapter-li jsChapter"]')
    pend = []
    for i in l:
        title = i.xpath("./a/span")[0].text
        ref = i.xpath("./a")[0].get("href")
        if not ref.endswith(".html"):
            last_ref = pend[-1][-1]
            idx = last_ref.rindex('/')
            num = int(last_ref[last_ref.rindex('/') + 1:len(last_ref) - 5]) + 1
            ref = last_ref[:idx] + '/' + str(num) + '.html'
            print(f"WARN: complete url:{ref} for {title}")

        pend.append((title, ref))
    print(pend)
    for i, j in pend:
        fetch_chapter(i, j)
    return doc

def fetch_chapter(title, ref):
    print(f'fetching {title}')
    url = prefix + ref
    i = 1
    res = [title + '\n']
    while True:
        print(f"{title}_{i}")
        resp = requests.get(f'{url[:-5]}_{i}.html', cookies=cookies, headers=headers)
        doc = etree.HTML(resp.text)
        l = [i.text.replace('\r', '\n') for i in doc.xpath("//p") if i.text is not None ][:-3]
        res.extend(l)
        a_list = [i.text for i in doc.xpath("//a")]
        if not '下一页' in a_list:
            break
        i = i + 1
    print(f'fetch {title} success')
    return res

if __name__ == "__main__":
    res = fetch_novel("2552")


