# 浏览器请求头，其中的cookie需要小伙伴更新为自己的cookie
request_headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    # 请将自己的cookie粘贴到下面
    'cookie': "",
    'origin': 'https://message.bilibili.com',
    'referer': 'https://message.bilibili.com/',
    'sec-ch-ua': "'Chromium';v='110', 'Not A(Brand';v='24', 'Google Chrome';v='110'",
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': "macOS",
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}

# B站相关接口地址
# stat是用户信息接口，可以获得用户的用户名、粉丝量、关注量等信息
stat_url = 'https://api.bilibili.com/x/relation/stat?vmid={}'
# followings是关注列表接口，可以最多获得100个用户的关注用户，可以获得关注用户的用户id和用户名等信息；
following_url = 'https://api.bilibili.com/x/relation/followings?vmid={}&pn={}&ps=50&order=desc'
