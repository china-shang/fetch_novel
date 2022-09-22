# -*- coding: utf-8 -*-

from time import sleep
import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
import threading
import traceback

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

response = requests.get('https://w.linovelib.com/novel/2552/catalog', cookies=cookies, headers=headers)
# response = requests.get('https://w.linovelib.com/novel/2552/93021_2.html', cookies=cookies, headers=headers)

def fetch_novel(n_id, book):
    print(f"will fetch {n_id}")
    try:
        while True:
            try:
                resp = requests.get(f'https://w.linovelib.com/novel/{n_id}/catalog',timeout=10, cookies=cookies, headers=headers)
                break
            except :
                continue
        doc = etree.HTML(resp.text)
        # l = doc.xpath('//li[@class="chapter-li jsChapter"]')
        l = doc.xpath('//ol[@class="chapter-ol chapter-ol-catalog"]/li')
        count = 0
        with open(book + '.txt', "w", encoding="utf8") as fp:
            for i in l:
                count += 1
                if i.text is not None:
                    print(f"write {book}.{i.text}")
                    fp.write(f"\n## {i.text}\n")
                    continue
                title = i.xpath("./a/span")[0].text
                ref = i.xpath("./a")[0].get("href")
                if not ref.endswith(".html"):
                    idx = last_ref.rindex('/')
                    num = int(last_ref[last_ref.rindex('/') + 1:len(last_ref) - 5]) + 1
                    ref = last_ref[:idx] + '/' + str(num) + '.html'
                    print(f"WARN: complete url:{ref} for {title}")
                data = fetch_chapter(book, title, ref)
                print(f"{book}: {count}/{len(l)}")
                fp.writelines(data)
                fp.flush()
                last_ref = ref
        print(f"{book} finish")
        return doc
    except Exception as e:
        print(f"FATEL EEROR {e}")
        traceback.print_exc()

def fetch_novel_multi(n_id, book):
    print(f"will fetch {n_id}")
    result = []
    pool = ThreadPoolExecutor(max_workers=32)
    try:
        while True:
            try:
                resp = requests.get(f'https://w.linovelib.com/novel/{n_id}/catalog',timeout=10, cookies=cookies, headers=headers)
                break
            except :
                continue
        doc = etree.HTML(resp.text)
        # l = doc.xpath('//li[@class="chapter-li jsChapter"]')
        l = doc.xpath('//ol[@class="chapter-ol chapter-ol-catalog"]/li')
        count = 0
        idx = 0
        for i in l:
            count += 1
            if i.text is not None:
                print(f"write {book}.{i.text}")
                result.append('')
                result[idx] = f"\n## {i.text}\n"
                idx += 1
                continue
            title = i.xpath("./a/span")[0].text
            ref = i.xpath("./a")[0].get("href")
            if not ref.endswith(".html"):
                t = last_ref.rindex('/')
                num = int(last_ref[last_ref.rindex('/') + 1:len(last_ref) - 5]) + 1
                ref = last_ref[:t] + '/' + str(num) + '.html'
                print(f"WARN: complete url:{ref} for {title}")
            print("will submit")
            result.append('')
            pool.submit(fetch_chapter_by_multi,book, title, ref, result, idx)
            idx += 1
            print(f"{book}: {count}/{len(l)}")
            last_ref = ref

        pool.shutdown(wait=True)
        with open(book + '.txt', "w", encoding="utf8") as fp:
            for data in result:
                fp.writelines(data)
                fp.flush()
        print(f"{book} finish")
        return doc
    except Exception as e:
        print(f"FATEL EEROR {e}")
        traceback.print_exc()

def fetch_chapter_by_multi(book, title, ref, res, idx):
    print(f"will fetch {book}.{title}.{idx} by thread" )
    res[idx] = fetch_chapter(book, title, ref)

def fetch_chapter(book, title, ref):
    while True:
        try:
            print(f'fetching {book}.{title}')
            url = prefix + ref
            i = 1
            res = ['\n### ' + title + '\n']
            while True:
                while True:
                    try:
                        print(f"fetching {book}.{title}_{i}")
                        resp = requests.get(f'{url[:-5]}_{i}.html', timeout=6, cookies=cookies, headers=headers)
                        break
                    except :
                        print(f"MEET EXCEPTION WILL RETRY: {book}.{title}_{i}")
                        continue
                doc = etree.HTML(resp.text)
                l = [i.text.strip('\r').strip('\n') + '\n' for i in doc.xpath("//p") if i.text is not None ][:-3]
                res.extend(l)
                a_list = [i.text for i in doc.xpath("//a")]
                if not '下一页' in a_list:
                    break
                i = i + 1
            print(f'fetch {book}.{title} success')
            return res
        except:
            print(f"MEET EXCEPTION WILL RETRY: {book}.{title}")
            pass

if __name__ == "__main__":
    import os
    os.chdir("C:/Users/win10/Desktop/fetch_novel")
    print(os.getcwd())
    pool = ThreadPoolExecutor(max_workers=10)
    pool.submit(fetch_novel_multi,"2552", "魔王学院的不适任者2")
    # pool.submit(fetch_novel_multi,"1860", "魔法科高中的劣等生")
    # pool.submit(fetch_novel,"4", "精灵使的剑舞")
    # pool.submit(fetch_novel,"1892", "噬血狂袭")
    # pool.submit(fetch_novel,"1375", "灼眼的夏娜")
    # pool.submit(fetch_novel,"2811", "学园都市")
    # pool.submit(fetch_novel,"2894", "魔法禁书目录SS 生物黑客篇")
    # pool.submit(fetch_novel,"2407", "只要长得可爱，即使是变态你也喜欢吗？")
    # pool.submit(fetch_novel,"23", "我的妹妹哪有这么可爱")
    # pool.submit(fetch_novel,"2117", "不正经的魔术讲师与禁忌教典")
    # pool.submit(fetch_novel,"2014", "不正经的魔术讲师与禁忌教典")
    # pool.submit(fetch_novel,"54", "新妹魔王的契约者")
    # pool.submit(fetch_novel,"71", "平凡职业造就世界最强")
    # pool.submit(fetch_novel,"2356", "魔女之旅")
    # pool.submit(fetch_novel,"1420", "机巧少女不会受伤")
    # pool.submit(fetch_novel,"204", "落第骑士英雄谭")
    # pool.submit(fetch_novel,"1915", "新约 魔法禁书目录")
    # pool.submit(fetch_novel,"104", "最弱无败神装机龙《巴哈姆特》")
    # pool.submit(fetch_novel,"824", "魔法禁书目录")
    sleep(100000)
    pool.shutdown(wait=True)
    print("all finish")

