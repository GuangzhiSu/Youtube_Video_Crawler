import json

# 加载 cookies JSON 文件
with open('Youtube_video_Scrape/cookies.json', 'r') as json_file:
    cookies = json.load(json_file)

# 创建一个新的 cookies.txt 文件
with open('Youtube_video_Scrape/cookies.txt', 'w') as txt_file:
    txt_file.write("# Netscape HTTP Cookie File\n")
    txt_file.write("# This is a generated file! Do not edit.\n\n")
    for cookie in cookies:
        domain = cookie.get('domain', '')
        flag = 'TRUE' if domain.startswith('.') else 'FALSE'
        path = cookie.get('path', '/')
        secure = 'TRUE' if cookie.get('secure', False) else 'FALSE'
        expiration = str(int(cookie.get('expirationDate', 0)))
        name = cookie.get('name', '')
        value = cookie.get('value', '')
        txt_file.write(f"{domain}\t{flag}\t{path}\t{secure}\t{expiration}\t{name}\t{value}\n")
