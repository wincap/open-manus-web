"""googlesearch is a Python library for searching Google, easily."""
from time import sleep
from bs4 import BeautifulSoup
from requests import get
from urllib.parse import unquote # to decode the url
import requests
import json

def get_useragent():
    """
    Generates a random user agent string mimicking the format of various software versions.

    The user agent string is composed of:
    - Lynx version: Lynx/x.y.z where x is 2-3, y is 8-9, and z is 0-2
    - libwww version: libwww-FM/x.y where x is 2-3 and y is 13-15
    - SSL-MM version: SSL-MM/x.y where x is 1-2 and y is 3-5
    - OpenSSL version: OpenSSL/x.y.z where x is 1-3, y is 0-4, and z is 0-9

    Returns:
        str: A randomly generated user agent string.
    """
    lynx_version = f"Lynx/{random.randint(2, 3)}.{random.randint(8, 9)}.{random.randint(0, 2)}"
    libwww_version = f"libwww-FM/{random.randint(2, 3)}.{random.randint(13, 15)}"
    ssl_mm_version = f"SSL-MM/{random.randint(1, 2)}.{random.randint(3, 5)}"
    openssl_version = f"OpenSSL/{random.randint(1, 3)}.{random.randint(0, 4)}.{random.randint(0, 9)}"
    return f"{lynx_version} {libwww_version} {ssl_mm_version} {openssl_version}"

def _req(term, results, lang, start, proxies, timeout, safe, ssl_verify, region):

    url = "https://api.bochaai.com/v1/web-search"

    payload = json.dumps({
        "query":  term,
        "summary": True,
        "count": 10,
        "page": 1
    })

    headers = {
        'Authorization': 'Bearer 你的博查apikey',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()


class SearchResult:
    def __init__(self, url, title, description):
        self.url = url
        self.title = title
        self.description = description

    def __repr__(self):
        return f"SearchResult(url={self.url}, title={self.title}, description={self.description})"


def search(term, num_results=10, lang="en", proxy=None, advanced=False, sleep_interval=0, timeout=5, safe="active", ssl_verify=None, region=None, start_num=0, unique=False):
    """Search the Google search engine"""

    # Proxy setup
    proxies = {"https": proxy, "http": proxy} if proxy and (proxy.startswith("https") or proxy.startswith("http")) else None

    start = start_num
    fetched_results = 0  # Keep track of the total fetched results
    fetched_links = set() # to keep track of links that are already seen previously

    # Send request
    resp = _req(term, num_results - start,
        lang, start, proxies, timeout, safe, ssl_verify, region)
        
    # put in file - comment for debugging purpose
    # with open('google.html', 'w') as f:
    #     f.write(resp.text)
        
    # Parse
    new_results = 0  # Keep track of new results in this iteration
    result_block =  resp["data"]["webPages"]["value"] 

    # link title description
    for result in result_block:

        #{'id': 'https://api.bochaai.com/v1/#WebPages.9', 'name': '大回暖进行时!最高气温冲刺25!如何防范花粉过敏?_苏南地区_全省_天气', 'url': 'https://www.sohu.com/a/873500886_121123734', 'displayUrl': 'https://www.sohu.com/a/873500886_121123734', 'snippet': '大回暖 过程持续发力 与此同时 天气回暖,万物复苏 大量花粉肆意播散 过敏季也随之而来 易过敏者要多加防范￬￬￬ 升温 虽然早晨还有寒意 白天在暖阳助力下 气温回升步伐加快 午后大部地区达到了13~1...', 'summary': '大回暖 过程持续发力 与此同时 天气回暖,万物复苏 大量花粉肆意播散 过敏季也随之而来 易过敏者要多加防范￬￬￬ 升温 虽然早晨还有寒意 白天在暖阳助力下 气温回升步伐加快 午后大部地区达到了13~15℃ 西北角沛县高达17.3℃ 暖意扑面而来 这才是开始 接下来几天升温根本停不下来 明天全省最高气温将突破20℃ 到了周六 不少城市气温将冲刺25℃ 本次升温过程的最高值 将冲刺常年5月中旬的状态 白天升温的同时昼夜温差将拉大 昼夜温差能超过15℃ 大家一定要注意合理的增减衣物 全省天气 未来三天全省以晴好天气为主,气温逐步回升｡ 3月19日20时到3月20日20时 全省晴｡最高温度:沿江和苏南地区20℃左右,其他地区21~22℃;最低温度:淮河以南地区5℃左右,其他地区3~4℃｡最高温度:全省23℃左右;', 'siteName': '搜狐', 'siteIcon': 'https://th.bochaai.com/favicon?domain_url=https://www.sohu.com/a/873500886_121123734', 'dateLastCrawled': '2025-03-20T11:24:00Z', 'cachedPageUrl': None, 'language': None, 'isFamilyFriendly': None, 'isNavigational': None}

        link = result["url"]
            # Check if the link has already been fetched and if unique results are required
        if link in fetched_links and unique:
            continue  # Skip this result if the link is not unique
        # Add the link to the set of fetched links
        fetched_links.add(link)
        # Extract the title text
        title = result["name"] 
        # Extract the description text
        description = result["snippet"] 
        # Increment the count of fetched results
        fetched_results += 1
        # Increment the count of new results in this iteration
        new_results += 1
        # Yield the result based on the advanced flag
        if advanced:
            yield SearchResult(link, title, description)  # Yield a SearchResult object
        else:
            yield link  # Yield only the link

        if fetched_results >= num_results:
            break  # Stop if we have fetched the desired number of results

        if new_results == 0:
            #If you want to have printed to your screen that the desired amount of queries can not been fulfilled, uncomment the line below:
            #print(f"Only {fetched_results} results found for query requiring {num_results} results. Moving on to the next query.")
            break  # Break the loop if no new results were found in this iteration

        sleep(sleep_interval)

