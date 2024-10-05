'''
自行捉包把api.tianjinzhitongdaohe.com里面的token(一般在请求头里)填到变量 nnck 中, 多账号@隔开
export nnck="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

cron: 20 8 * * *
const $ = new Env("牛牛开宝箱");
'''


import os
import random
import time
import requests
from concurrent.futures import ThreadPoolExecutor

fixed_headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 12; 21091116UC Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/127.0.6533.64 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/29.09091)',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip'
}

def get_headers(token=None):
    headers = fixed_headers.copy()  
    if token:
        headers["token"] = token  
    return headers

def kbx(token, account_id):
    url = "https://api.tianjinzhitongdaohe.com/sqx_fast/app/integral/userTimer"
    headers = get_headers(token)
    
    retry_count = 0
    max_retries = 5

    while True:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  
            
            response_json = response.json()
            
            if response_json.get('code') == 0:
                data = response_json.get('data')
                
                if isinstance(data, str) and data.isdigit():  
                    print(f"{account_id} 开宝箱成功：{data} 金币")
                    
                    wait_time = random.randint(180, 240)
                    print(f"{account_id} 等待 {wait_time} 秒后继续...")
                    time.sleep(wait_time)
                else:
                    print(f"{account_id} 今天宝箱已开启上限")
                    break
            else:
                print(f"{account_id} 今天宝箱已开启上限")
                break
        except requests.RequestException as e:
            print(f"{account_id} 请求失败，异常信息：{e}。尝试重新请求...")
            retry_count += 1
            if retry_count >= max_retries:
                print(f"{account_id} 达到最大重试次数，停止请求。")
                break
            time.sleep(5)  

def main():
    token_vars = os.environ.get('nnck')
    
    if token_vars is None:
        print("请设置 nnck 环境变量")
        return

    tokens = token_vars.split('@')  
    
    
    with ThreadPoolExecutor(max_workers=len(tokens)) as executor:
        futures = []
        for index, token in enumerate(tokens, start=1):
            account_id = f"账号{index}"
            futures.append(executor.submit(kbx, token, account_id))
        
        
        for future in futures:
            future.result()

if __name__ == "__main__":
    main()
