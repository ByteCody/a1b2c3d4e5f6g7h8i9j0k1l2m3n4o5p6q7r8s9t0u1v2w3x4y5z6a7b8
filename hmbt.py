'''
自行捉包把freevideo.zqqds.cn里面的datas(一般在请求头里)填到变量 hmck 中, 多账号@隔开
export hmck="97681251ccd8dae69d664486e49xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

cron: 0 6,11,17,21 * * *
const $ = new Env("河马饭点补贴");
'''

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import binascii
import requests
import time
import json
import random
import os

key = b'dzkjgfyxgshylgzm'  
iv = b'apiupdownedcrypt'   

def aes_encrypt(data):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(data.encode('utf-8'), AES.block_size, style='pkcs7')
    encrypted = cipher.encrypt(padded_data)
    return binascii.hexlify(encrypted).decode('utf-8')

def aes_decrypt(encrypted_data):
    encrypted_bytes = binascii.unhexlify(encrypted_data)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_padded = cipher.decrypt(encrypted_bytes)
    decrypted = unpad(decrypted_padded, AES.block_size, style='pkcs7')
    return decrypted.decode('utf-8')

fixed_headers = {
    'Host': 'freevideo.zqqds.cn',
    'content-type': 'application/json; charset=utf-8',
    'accept-encoding': 'gzip',
    'user-agent': 'okhttp/4.10.0'
}

def get_headers(datas):
    headers = fixed_headers.copy()
    headers["datas"] = datas
    return headers

def fd1(datas):
    url = "https://freevideo.zqqds.cn/free-video-portal/portal/1303"
    current_timestamp = int(time.time() * 1000)
    
    data = {
  "taskId": 128,
  "buttonClickTime": current_timestamp,
  "signDay": None,
  "taskAction": 74
}
        
    data_str = json.dumps(data)
    encrypted_data = aes_encrypt(data_str)
    headers = get_headers(datas)
    
    try:
        response = requests.post(url, headers=headers, data=encrypted_data)
        if response.status_code == 200:
            try:
                response_json = response.json()
                encrypted_response_data = response_json.get('data')
                if encrypted_response_data:
                    decrypted_data = aes_decrypt(encrypted_response_data)
                    try:
                        decrypted_json = json.loads(decrypted_data)
                        award_video_token = decrypted_json.get('awardVideoToken')
                        message = decrypted_json.get('message')
                        print(f"饭点看剧领补贴状态：{message}")
                        time.sleep(random.uniform(60, 70))
                        fd2(datas, award_video_token)
                    except json.JSONDecodeError:
                        print("解密后的数据不是有效的JSON格式")
                else:
                    print("响应中未找到 'data' 字段")
            except json.JSONDecodeError:
                print("响应不是有效的JSON格式")
        else:
            print("请求失败，状态码：", response.status_code)
    except requests.exceptions.RequestException as e:
        print("请求失败，错误信息：", e)

def fd2(datas, award_video_token):
    url = "https://freevideo.zqqds.cn/free-video-portal/portal/1303"
    current_timestamp = int(time.time() * 1000)
    
    data = {"taskId":95,"awardVideoToken":award_video_token,"taskAction":27,"buttonClickTime":current_timestamp}
    
    data_str = json.dumps(data)
    encrypted_data = aes_encrypt(data_str)
    headers = get_headers(datas)
    
    try:
        response = requests.post(url, headers=headers, data=encrypted_data)
        if response.status_code == 200:
            try:
                response_json = response.json()
                encrypted_response_data = response_json.get('data')
                if encrypted_response_data:
                    decrypted_data = aes_decrypt(encrypted_response_data)
                    try:
                        decrypted_json = json.loads(decrypted_data)
                        message = decrypted_json.get('message')
                        print(f"看广告领取状态：{message}")
                    except json.JSONDecodeError:
                        print("解密后的数据不是有效的JSON格式")
                else:
                    print("响应中未找到 'data' 字段")
            except json.JSONDecodeError:
                print("响应不是有效的JSON格式")
        else:
            print("请求失败，状态码：", response.status_code)
    except requests.exceptions.RequestException as e:
        print("请求失败，错误信息：", e)

def main():
    datas_vars = os.environ.get('hmck')
    if datas_vars is None:
        print("请设置 hmck 环境变量")
        return

    datas_list = datas_vars.split('@')
    
    for index, datas in enumerate(datas_list, start=1):
        account_id = f"账号{index}"
        print(f"\n开始运行 {account_id}")
        fd1(datas)

if __name__ == "__main__":
    main()
