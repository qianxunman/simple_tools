import requests


def main():
    url = 'http://10.134.42.103/wlcauth/login/?gw_address=10.135.96.6&gw_port=2060&gw_id=20:0C:C8:24:08:1A&ip=10.135.96.74' \
          '&mac=DC:85:DE:97:DE:92&ssid=SmartDorm506'
    header = {
        'Host': '10.134.42.103',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'http://10.134.42.103/cpauth/portal?gw_address=10.135.96.6&gw_port=2060' \
                   '&gw_id=20:0C:C8:24:08:1A&ssid=SmartDorm506&ip=10.135.96.74&mac=DC:85:DE:97:DE:92',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '264',
        'Connection': 'keep-alive',
        'Cookie': 'authpuppy=q3l239gdhasftc0r0bjnqiao57',
        'Upgrade-Insecure-Requests': '1'
    }
    data = {
        'gw_id': '20:0C:C8:24:08:1A',
        'gw_address': '10.135.96.6',
        'gw_port': '2060',
        'mac': 'DC:85:DE:97:DE:92',
        'authenticator': 'apAuthLocalUser',
        'submit[apAuthLocalUserconnect]': '登陆',
        'apAuthLocalUser[username]': 'F3234048',
        'apAuthLocalUser[password]': '147258369'
    }
    # 以上部分为请求的各种参数

    while True:
        try:
            res = requests.request('post', url, headers=header, data=data)
            print(res.content.decode('utf-8'))
            print(res.status_code)
            if res.status_code == 200:
                print('以经登录成功，无需重复登录！')
                input()
                break

        except Exception as e:

            print('program has started,but has some error happened！')
            print(e)
            if str(e).__contains__('403'):
                print('以经重定向，说明登录成功，可以上网！')
            key_value = input()
            if key_value == 'q':  # 用户输入q则退出循环请求
                break

if __name__ == '__main__':
    main()
