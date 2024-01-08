import requests

ss_proxy = "socks5://:6a75d911-8cc1-42a2-a886-f69fb838f218@117.164.185.174:36652"

# 构建代理参数
proxies = {
    'http': ss_proxy,
    'https': ss_proxy
}


def get_proxy():
    # proxy = requests.get("http://127.0.0.1:5010/get").json()
    # return {"http": "http://{}".format(proxy)}
    return proxies

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

if __name__ == '__main__':
    count = 0;
    for i in range(10):
        try:
            proxy = get_proxy()
            print(proxy)
            html = requests.get('https://www.mangabz.com', proxies = proxies)
            print(html)
        except Exception as e:
            print(e)
            count = count + 1
            print(count)
