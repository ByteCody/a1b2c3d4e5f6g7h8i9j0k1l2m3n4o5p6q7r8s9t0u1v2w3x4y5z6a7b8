'''
自行捉包把api.tianjinzhitongdaohe.com里面的token(一般在请求头里)填到变量 nnck 中, 多账号@隔开
export nnck="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

cron: 2 6,11,17,21 * * *
const $ = new Env("牛牛饭点补贴");
'''

import os
import requests

fixed_headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 12; 21091116UC Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/127.0.6533.64 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/29.09091)',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'Content-Type': 'application/x-www-form-urlencoded'
}


def get_headers(token=None):
    headers = fixed_headers.copy()  
    if token:
        headers["token"] = token  
    return headers


def nnfb(token):
    url = 'https://api.tianjinzhitongdaohe.com/sqx_fast/app/integral/eatGold'
    headers = get_headers(token=token)  

    try:
        
        response = requests.get(url, headers=headers)

        
        if response.status_code == 200:
            
            data = response.json()

            
            if data.get('code') == 0:

                print("领取金币成功")


            else:
                
                print("领取金币失败")
        else:
            
            print(f"请求失败，状态码: {response.status_code}")
    except requests.exceptions.Timeout:
        print("请求超时，请稍后重试")
    except requests.exceptions.RequestException as e:
        print(f"请求出现错误: {e}")





def main():
    
    token_vars = os.environ.get('nnck')
    
    if token_vars is None:
        print("请设置 nnck 环境变量")
        return

    tokens = token_vars.split('@')  
    
    
    for index, token in enumerate(tokens, start=1):
        account_id = f"账号{index}"
        print(f"\n开始运行 {account_id}")
        nnfb(token)  


if __name__ == "__main__":
    main()
