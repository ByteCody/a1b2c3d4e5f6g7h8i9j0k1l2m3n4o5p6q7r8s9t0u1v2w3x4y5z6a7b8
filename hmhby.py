from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import binascii
import requests
import time
import json
import random
import os
import re

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
    
    data = {"taskId": 317, "buttonClickTime": current_timestamp, "signDay": None, "taskAction": 82}
        
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
                        awardVideoToken = decrypted_json.get('awardVideoToken')
                        message = decrypted_json.get('message')
                        print(f"红包雨状态：{message}")
                        return message,awardVideoToken
                    except json.JSONDecodeError:
                        print("解密后的数据不是有效的JSON格式")
                        return None
                else:
                    print("响应中未找到 'data' 字段")
                    return None
            except json.JSONDecodeError:
                print("响应不是有效的JSON格式")
                return None
        else:
            print("请求失败，状态码：", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print("请求失败，错误信息：", e)
        return None


def fd2(datas, awardVideoToken):
    url = "https://freevideo.zqqds.cn/free-video-portal/portal/1303"
    current_timestamp = int(time.time() * 1000)
    
    data = {"taskId":95,"awardVideoToken":awardVideoToken,"taskAction":27,"buttonClickTime":current_timestamp}
    
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
        
        while True:  
            message, awardVideoToken = fd1(datas)  
            if message is None:        
                print("调用 fd1 失败，退出循环")            
                break  
            if not any(char.isdigit() for char in message):
                print("红包雨已开启上限")
                break  
            else:
                delay = random.randint(60, 74)
                print(f"等待 {delay} 秒后看完广告")
                fd2(datas, awardVideoToken)  
                wait_time = random.randint(1200, 1220)
                print(f"等待 {wait_time} 秒后继续领取红包雨")
                time.sleep(wait_time)  

if __name__ == "__main__":
    main()
