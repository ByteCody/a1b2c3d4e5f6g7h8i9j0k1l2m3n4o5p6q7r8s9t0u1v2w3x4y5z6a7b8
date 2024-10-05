from asyncio import Task
import re
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

def handle_tasks(datas):
    url = "https://freevideo.zqqds.cn/free-video-portal/portal/1301"
    data = {"signText": 1, "bookReads": {"41000101734": 36}}

    data_str = json.dumps(data)
    encrypted_data = aes_encrypt(data_str)
    headers = get_headers(datas)

    try:
        response = requests.post(url, headers=headers, data=encrypted_data)
        response.raise_for_status()
        response_json = response.json()
        
        encrypted_response_data = response_json.get('data')
        if encrypted_response_data:
            decrypted_data = aes_decrypt(encrypted_response_data)
            try:
                decrypted_json = json.loads(decrypted_data)
                all_tasks_completed = process_tasks(decrypted_json, datas)
                
                if all_tasks_completed:
                    print("所有任务已完成")
                    
            except json.JSONDecodeError:
                print("解密后的数据不是有效的JSON，原始数据:", decrypted_data)
        else:
            print("未能获取加密的响应数据")

    except requests.RequestException as e:
        print(f"请求出现异常: {e}")
        if 'response' in locals():
            print(f"响应状态码: {response.status_code}")
            print(f"响应内容: {response.text}")

def process_tasks(decrypted_json, datas):
    all_tasks_completed = True
    
    task_sets = decrypted_json.get("taskSetList", [])
    for task_set in task_sets:
        print(f"\n-----{task_set.get('taskSetTitle')}------")
        tasks = task_set.get("taskList", [])
        for task in tasks:
            task_status_completed = process_task(task, datas)
            if not task_status_completed:
                all_tasks_completed = False

    cashAmount = float(decrypted_json.get("cashAmount", 0))
    cashBalance = float(decrypted_json.get("cashBalance", 0))

    print(f"\n-----资产查询------")
    print(f"今天赚了 {cashAmount:.2f} 元")
    print(f"总余额: {cashBalance:.2f} 元")

    if cashBalance > 0.3:
        print(f"\n-----准备提现------")
        

    return all_tasks_completed

def handle_regular_sign_in_task(datas, task):
    print("去完成签到任务")
    task_id = task.get("taskId")
    task_action = task.get("taskAction")
    pqd(datas, task_id, task_action)

def process_task(task, datas):
    taskTitle = task.get("taskTitle")
    taskStatus = task.get("taskStatus")
    status_text = get_status_text(taskStatus)
    
    print(f"{taskTitle} 当前状态: {status_text}")
    
    if taskStatus != 3:  
        if "新人签到" in taskTitle:
            handle_sign_in_task(datas, task)  
        elif "签到" in taskTitle:  
            handle_regular_sign_in_task(datas, task)
        elif "定时宝箱" in taskTitle:
            complete_Chest_task(datas, task)

        elif "看小视频领金币" in taskTitle:
            complete_vi_task(datas, task)
        elif "分享领金币" in taskTitle:
            complete_share_task(datas, task)

        return False
    return True  

def get_status_text(taskStatus):
    return "进行中" if taskStatus != 3 else "已完成"

def handle_sign_in_task(datas, task):
    task_id = task.get("taskId")
    task_action = task.get("taskAction")
    sign_award_vos = task.get("signAwardVos", [])
    today_sign = next((award for award in sign_award_vos if award.get("day") == 1), None)
    
    if today_sign:
        day = today_sign.get("day")
        print(f"今天的签到任务是第 {day} 天，准备签到")
        qd(datas, task_id, task_action, day)
    else:
        print("未找到今天的签到任务。")

def complete_vi_task(datas, task):
    task_id = task.get("taskId")
    taskAction = task.get("taskAction")
    proNum = task.get("proNum", 0)    
    totalNum = task.get("totalNum", 0)  
    remaining_calls = max(0, totalNum - proNum)

    print(f"还需要再看 {remaining_calls} 视频广告")

    for i in range(remaining_calls):
        kxsp(datas, task_id, taskAction)
        print(f"第 {i + 1} 次看视频广告")

        wait_time = random.randint(660, 680)
        print(f"等待 {wait_time} 秒后再尝试...")
        time.sleep(wait_time)


def complete_share_task(datas, task):
    task_id = task.get("taskId")
    task_action = task.get("taskAction")
    print("去完成分享任务")
    fx0(datas, task_action)
    delay = random.uniform(64, 73)
    print(f"等待 {delay:.2f} 秒后领取奖励")
    time.sleep(delay)
    fx(datas, task_id, task_action)  


def complete_Chest_task(datas, task):
    print("去完成开宝箱任务")
    
    task_id = task.get("taskId")
    task_action = task.get("taskAction")
    max_attempts = 15 
    
    for i in range(max_attempts):
        print(f"第 {i+1} 次开宝箱...")
        
        try:
            decrypted_json = kbx1(datas, task_id, task_action) 
            
            if decrypted_json:
                message = decrypted_json.get('message', '')
                
                numbers = re.findall(r'\d+', message)
                
                if not numbers:
                    print("开宝箱上限，停止任务。")
                    break

            else:
                print("开宝箱任务失败，停止任务。")
                break

        except Exception as e:
            print(f"发生错误: {e}")
            
            continue

        
        if i < max_attempts - 1:
            print("等待 10 分钟后再开宝箱")
            time.sleep(600)
    
    print("已达到最大尝试次数，任务结束")




def pqd(datas, task_id, task_action):
    url = "https://freevideo.zqqds.cn/free-video-portal/portal/1302"

    
    data = {"action":task_action,"taskId":task_id}
        
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
                        message = decrypted_json.get('msg')
                        print(f"签到状态：{message}")
                        delay = random.uniform(64, 73)
                        print(f"等待 {delay:.2f} 秒后看完广告")
                        time.sleep(delay)    
                        pqd1(datas)
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


def pqd1(datas):
    url = "https://freevideo.zqqds.cn/free-video-portal/portal/1303"
    current_timestamp = int(time.time() * 1000)
    
    data = {"taskId":102,"awardVideoToken":None,"taskAction":14,"buttonClickTime":current_timestamp}
    
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
                        print(f"签到看广告状态：{message}")
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


def qd(datas, task_id, task_action, day):
    url = "https://freevideo.zqqds.cn/free-video-portal/portal/1303"
    current_timestamp = int(time.time() * 1000)
    
    data = {"taskId": task_id, "buttonClickTime": current_timestamp, "signDay": day, "taskAction": task_action}
        
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
                        print(f"签到状态：{message}")
                        delay = random.uniform(64, 73)
                        print(f"等待 {delay:.2f} 秒后看完广告")
                        time.sleep(delay)    
                        qd1(datas, award_video_token)
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


def qd1(datas, award_video_token):
    url = "https://freevideo.zqqds.cn/free-video-portal/portal/1303"
    current_timestamp = int(time.time() * 1000)
    
    data = {"taskId":99, "awardVideoToken": award_video_token,"taskAction":27,"buttonClickTime": current_timestamp}
    
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
                        print(f"签到看广告状态：{message}")
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


def kxsp(datas, task_id, taskAction):
    url = "https://freevideo.zqqds.cn/free-video-portal/portal/1303"
    current_timestamp = int(time.time() * 1000)
    
    data = {"taskId":task_id,"awardVideoToken":None,"taskAction":taskAction,"breakIce":0,"buttonClickTime":current_timestamp}
        
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
                        print(f"看小视频领金币状态：{message}")

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


def fx0(datas, taskAction):
    url = "https://freevideo.zqqds.cn/free-video-portal/portal/1302"
    
    data = {"action": taskAction}
        
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
                        
                        status = decrypted_json.get("status")
                        
                        if status == 2:
                            print("分享成功")
                        else:
                            print("分享失败")
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


def kbx1(datas, task_id, task_action):
    url = "https://freevideo.zqqds.cn/free-video-portal/portal/1303"
    current_timestamp = int(time.time() * 1000)
    
    data = {"taskId": task_id, "buttonClickTime": current_timestamp, "signDay": None, "taskAction": task_action}
    data_str = json.dumps(data)
    encrypted_data = aes_encrypt(data_str)
    headers = get_headers(datas)

    try:
        response = requests.post(url, headers=headers, data=encrypted_data)
        response.raise_for_status()  

        response_json = response.json()
        encrypted_response_data = response_json.get('data')
        if not encrypted_response_data:
            print("响应中未找到 'data' 字段")
            return None

        decrypted_data = aes_decrypt(encrypted_response_data)
        decrypted_json = json.loads(decrypted_data)
        message = decrypted_json.get('message')
        print(f"开宝箱状态：{message}")

        award_video_token = decrypted_json.get('awardVideoToken')
        if award_video_token:
            time.sleep(random.uniform(60, 70))  
            kbx2(datas, award_video_token)
        
        return decrypted_json  

    except json.JSONDecodeError:
        print("解密后的数据不是有效的JSON格式")
    except requests.exceptions.RequestException as e:
        print(f"请求失败，错误信息：{e}")
    
    return None  


def kbx2(datas, award_video_token):
    url = "https://freevideo.zqqds.cn/free-video-portal/portal/1303"
    current_timestamp = int(time.time() * 1000)
    
    data = {
        "taskId": 97,
        "awardVideoToken": award_video_token,
        "buttonClickTime": current_timestamp
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
                        message = decrypted_json.get('message')
                        print(f"开宝箱看广告状态：{message}")
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



def fx(datas, task_id, task_action):
    url = "https://freevideo.zqqds.cn/free-video-portal/portal/1303"
    current_timestamp = int(time.time() * 1000)
    
    data = { "taskId": task_id, "buttonClickTime": current_timestamp, "signDay":None, "taskAction": task_action}
        
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
                        print(f"分享领取奖励状态：{message}")
                        delay = random.uniform(64, 73)
                        print(f"等待 {delay:.2f} 秒后看完广告")
                        time.sleep(delay)   
                        fx1(datas, award_video_token)
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


def fx1(datas, award_video_token):
    url = "https://freevideo.zqqds.cn/free-video-portal/portal/1303"
    current_timestamp = int(time.time() * 1000)
    
    data = {"taskId":99,"awardVideoToken":award_video_token,"taskAction":27,"buttonClickTime":current_timestamp}
    
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
                        print(f"分享看广告状态：{message}")
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



def tx0(datas):
    url = "https://freevideo.zqqds.cn/free-video-portal/portal/1854"
    
    
    data = {}
    encrypted_data = aes_encrypt(json.dumps(data))  
    
    headers = get_headers(datas)  
    
    try:
        
        response = requests.post(url, headers=headers, data=encrypted_data)
        response.raise_for_status()  
        
        
        response_json = response.json()
        encrypted_response_data = response_json.get('data')
        if encrypted_response_data:
            decrypted_data = aes_decrypt(encrypted_response_data)
            try:
                decrypted_json = json.loads(decrypted_data)               
                cash_out_amount_list = decrypted_json.get("cashOutAmountList", [])
                target_amount = 0.3
                
                for option in cash_out_amount_list:
                    if option.get('cashoutAmount') == target_amount:
                        data_hash_val = option.get('dataHashVal')
                        if data_hash_val:
                            print(f"找到提现0.3元的选项")
                            delay = random.uniform(10, 15)  
                            print(f"等待 {delay:.2f} 秒后提现")
                            time.sleep(delay)  
                            tx(datas, data_hash_val)  
                            return data_hash_val
                
                print("没有提现0.3元的选项")
                return None
                
            except json.JSONDecodeError:
                print("解密后的数据不是有效的JSON格式")
                return None
        else:
            print("响应中未找到 'data' 字段")
            return None
    
    except requests.exceptions.RequestException as e:
        print("请求失败，错误信息：", e)
        return None

def tx(datas, data_hash_val):
    if data_hash_val:
        url = "https://freevideo.zqqds.cn/free-video-portal/portal/1856"
        
        data = {
            "amountId": 81,  
            "dataHashVal": data_hash_val,  
            "paymentType": 1,  
            "type": "cash"  
        }
        
        encrypted_data = aes_encrypt(json.dumps(data))  
        headers = get_headers(datas)  
        
        try:
            
            response = requests.post(url, headers=headers, data=encrypted_data)
            response.raise_for_status()  
            
            
            response_json = response.json()
            encrypted_response_data = response_json.get('data')
            if encrypted_response_data:
                decrypted_data = aes_decrypt(encrypted_response_data)
                try:
                    decrypted_json = json.loads(decrypted_data)
                    msg = decrypted_json.get('msg')
                    print(f"提现状态：{msg}")
                except json.JSONDecodeError:
                    print("解密后的数据不是有效的JSON格式")
            else:
                print("响应中未找到 'data' 字段")
        
        except requests.exceptions.RequestException as e:
            print(f"提现请求失败，错误信息：{e}")
    else:
        print("无法进行提现操作，因为未获取到有效的dataHashVal")




def main():
    datas_vars = os.environ.get('hmck')
    if datas_vars is None:
        print("请设置 hmck 环境变量")
        return

    datas_list = datas_vars.split('@')
    
    for index, datas in enumerate(datas_list, start=1):
        account_id = f"账号{index}"
        print(f"\n开始运行 {account_id}")

   

        handle_tasks(datas)

if __name__ == "__main__":
    main()