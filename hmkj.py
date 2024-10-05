
'''
自行捉包把freevideo.zqqds.cn里面的datas(一般在请求头里)填到变量 hmck 中, 多账号@隔开
export hmck="97681251ccd8dae69d664486e49xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

cron: 2 16 * * *
const $ = new Env("河马看剧");
'''

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
import datetime


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
                process_tasks(decrypted_json, datas)
            except json.JSONDecodeError:
                print("解密后的数据不是有效的JSON，原始数据:", decrypted_data)
        else:
            print("未能获取加密的响应数据")

    except requests.RequestException as e:
        print(f"请求出现异常: {e}")
        if 'response' in locals():
            print(f"响应状态码: {response.status_code}")
            print(f"响应内容: {response.text}")


last_video_infos = []  

def process_tasks(decrypted_json, datas):
    all_tasks_completed = True
    task_sets = decrypted_json.get("taskSetList", [])

    for task_set in task_sets:
        task_set_title = task_set.get("taskSetTitle", "")
        
        
        if task_set_title == "日常任务":
            print(f"\n-----{task_set_title}------")
            tasks = task_set.get("taskList", [])
            
            
            for task in tasks:
                taskTitle = task.get("taskTitle")
                if "看下方剧10分钟领金币" in taskTitle:
                    task_status_completed = process_task(task, datas)
                    if not task_status_completed:
                        all_tasks_completed = False

            for task in tasks:
                taskTitle = task.get("taskTitle")
                if "看剧领金币" in taskTitle:
                    task_status_completed = process_task(task, datas)
                    if not task_status_completed:
                        all_tasks_completed = False
    
    return all_tasks_completed

def process_task(task, datas):
    global last_video_infos  

    taskTitle = task.get("taskTitle")
    taskStatus = task.get("taskStatus")
    status_text = get_status_text(taskStatus)
    
    
    if "看剧领金币" in taskTitle or "看下方剧10分钟领金币" in taskTitle:
        print(f"{taskTitle} 当前状态: {status_text}")

    
    videoInfos = task.get("videoInfos", [])

    
    if "看下方剧10分钟领金币" in taskTitle:
        if videoInfos:
            last_video_infos = videoInfos  
        else:
            print("没有找到视频信息")
    
    
    if "看剧领金币" in taskTitle:
        if not videoInfos:  
            videoInfos = last_video_infos

    
    if taskStatus != 3:  
        if "看下方剧10分钟领金币" in taskTitle:
            handle_sign_in_task(datas, task, videoInfos)  
        elif "看剧领金币" in taskTitle:  
            handle_regular_sign_in_task(datas, task, videoInfos)
        return False
    
    return True  

def get_status_text(taskStatus):
    return "进行中" if taskStatus != 3 else "已完成"


def cjb(datas):
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
                cjb1(decrypted_json,datas)
            except json.JSONDecodeError:
                print("解密后的数据不是有效的JSON，原始数据:", decrypted_data)
        else:
            print("未能获取加密的响应数据")

    except requests.RequestException as e:
        print(f"请求出现异常: {e}")
        if 'response' in locals():
            print(f"响应状态码: {response.status_code}")
            print(f"响应内容: {response.text}")


def cjb1(decrypted_json,datas):
    task_set_list = decrypted_json.get("taskSetList", [])
    for task_set in task_set_list:
        task_list = task_set.get("taskList", [])
        for task in task_list:
            
            if task.get("taskTitle") == "看剧领金币":
                taskTitle = task.get("extraGold", {}).get("taskTitle", 0)
                task_award = task.get("extraGold", {}).get("taskAward", 0)  
                stage_num = task.get("extraGold", {}).get("stageNum", 0)  
                taskId = task.get("extraGold", {}).get("taskId", 0)  
                taskAction = task.get("extraGold", {}).get("taskAction", 0)                 
                
                if taskTitle == "看短剧额外存金币":
                    print("已开启看短剧存金币: ")
                    print(f"需要看剧存: {task_award} 金币")
                    print(f"当前已存: {stage_num} 金币")
                    if stage_num >= task_award:
                        print("条件满足，去领取金币")
                        delay = random.randint(60, 74)  
                        print(f"等待 {delay} 秒后看完广告")
                        time.sleep(delay)  
                        lq(datas, taskId, taskAction) 
                    else:
                        print("不满足领取条件")

                else:
                    print("未开启看剧存金币的任务")

                return 


def handle_sign_in_task(datas, task, videoInfos):
    proNum = task.get("proNum")
    proNum_seconds = proNum * 60  

    if proNum_seconds >= 900:
        print("今日已看完10分钟，去领取金币奖励") 
        kj(datas, task.get("taskId"), task.get("taskAction"))
    else:
        target_duration = 900  
        total_watched = proNum_seconds
        videoInfos = [video for video in videoInfos if video.get('bookId')]

        while total_watched < target_duration:
            if not videoInfos:
                print("没有找到视频信息")
                break
            
            for video in videoInfos:
                bookId = video.get('bookId')
                if not bookId:
                    print("视频信息缺少 bookId")
                    continue
                
                wait_sec = random.randint(60, 80)
                video_sec = wait_sec

                mnkj(datas, bookId, video_sec)

                total_watched += video_sec
                remaining_videos = target_duration - total_watched

                
                print(f"总观看时间: {total_watched}秒，剩余时间: {remaining_videos}秒")
                print(f"等待 {wait_sec} 秒后继续看剧")
                time.sleep(wait_sec)
                if total_watched >= target_duration:
                    break

        if total_watched >= 900:
            kj(datas, task.get("taskId"), task.get("taskAction"))


def handle_regular_sign_in_task(datas, task, videoInfos):
    proNum = task.get("proNum")
    proNum_seconds = proNum * 60  

    if proNum_seconds >= 10860: 
        print("今日已看完181分钟，去领取金币奖励") 
        unclaimed_awards = lqcs(datas)  
        if unclaimed_awards and unclaimed_awards > 0:
            for _ in range(unclaimed_awards):
                delay = random.randint(6, 14)  
                print(f"等待 {delay} 秒后继续领取金币奖励")
                time.sleep(delay)                 
                try:
                    kj(datas, task.get("taskId"), task.get("taskAction"))  
                except Exception as e:
                    print(f"领取奖励时发生错误: {e}")
    else:
        target_duration = 10860  
        total_watched = proNum_seconds  
        videoInfos = [video for video in videoInfos if video.get('bookId')]  

        if not videoInfos:
            print("没有找到视频信息")
            return

        wait_sec = random.randint(60, 80)  

        while total_watched < target_duration:
            for video in videoInfos:
                bookId = video.get('bookId')
                if not bookId:
                    print("视频信息缺少 bookId")
                    continue

                
                video_sec = wait_sec

                
                mnkj(datas, bookId, video_sec)

               
                total_watched += video_sec
                remaining_videos = target_duration - total_watched

                
                print(f"总观看时间: {total_watched}秒，剩余时间: {remaining_videos}秒")

                
                if total_watched >= target_duration:
                    print("观看时间已满足 181 分钟，任务完成")
                    break

                
                wait_sec = random.randint(60, 80)
                print(f"等待 {wait_sec} 秒后继续看剧")
                time.sleep(wait_sec)

        
        if total_watched >= 10860:
            unclaimed_awards = lqcs(datas)  
            if unclaimed_awards and unclaimed_awards > 0:
                for _ in range(unclaimed_awards):
                    delay = random.randint(6, 14)  
                    print(f"等待 {delay} 秒后继续领取金币奖励")
                    time.sleep(delay)  
                    try:
                        kj(datas, task.get("taskId"), task.get("taskAction"))  
                    except Exception as e:
                        print(f"领取奖励时发生错误: {e}")


def mnkj(datas, bookId, random_seconds):
    url = "https://freevideo.zqqds.cn/free-video-portal/portal/1301"
    
    
    data = {"signText": 1, "bookReads": {bookId: random_seconds}}  
    data_str = json.dumps(data)
    
   
    encrypted_data = aes_encrypt(data_str)
    
    
    headers = get_headers(datas)

    
    try:
        response = requests.post(url, headers=headers, data=encrypted_data)
        response.raise_for_status()  
        
        
        response_data = response.json()
        if 'data' in response_data:
            print("看剧成功")
        else:
            print("看剧失败")
    except json.JSONDecodeError:
        print("响应内容不是有效的JSON格式。")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP请求错误: {http_err}")
    except Exception as err:
        print(f"发生错误: {err}")

def lq(datas, taskId, taskAction):
    url = "https://freevideo.zqqds.cn/free-video-portal/portal/1303"
    current_timestamp = int(time.time() * 1000)
    
    data = {"taskId":taskId,"awardVideoToken":None,"taskAction":taskAction,"buttonClickTime":current_timestamp}
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
        print(f"领取金币状态：{message}")

    except json.JSONDecodeError:
        print("解密后的数据不是有效的JSON格式")
    except requests.exceptions.RequestException as e:
        print(f"请求失败，错误信息：{e}")
    
    return None  
    
def kj(datas, taskId, taskAction):
    url = "https://freevideo.zqqds.cn/free-video-portal/portal/1303"
    current_timestamp = int(time.time() * 1000)
    
    data = {"taskId":taskId,"buttonClickTime":current_timestamp,"signDay":None,"taskAction":taskAction}

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
        print(f"领取金币状态：{message}")

        award_video_token = decrypted_json.get('awardVideoToken')
        if award_video_token:
            delay = random.randint(60, 70)  
            print(f"等待 {delay} 秒后看完广告")
            time.sleep(delay)  
            kj2(datas, award_video_token)
        
        return decrypted_json  

    except json.JSONDecodeError:
        print("解密后的数据不是有效的JSON格式")
    except requests.exceptions.RequestException as e:
        print(f"请求失败，错误信息：{e}")
    
    return None  


def kj2(datas, award_video_token):
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
                        print(f"看广告状态：{message}")
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
    
def lqcs(datas):
    url = "https://freevideo.zqqds.cn/free-video-portal/portal/1301"
    data = {"signText": 1, "bookReads": {"41000101734": 36}}

    
    try:
        data_str = json.dumps(data)
        encrypted_data = aes_encrypt(data_str)
    except Exception as e:
        print(f"数据加密失败: {e}")
        return

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
                unclaimed_awards = 0

                
                task_set_list = decrypted_json.get('taskSetList', [])

                
                for task_set in task_set_list:
                    task_list = task_set.get('taskList', [])
                    for task in task_list:
                        
                        if 'stageReadAwardList' in task:
                            stage_list = task['stageReadAwardList']
                            for stage in stage_list:
                               
                                if stage['status'] == 2:
                                    unclaimed_awards += 1
                print("----看剧领取金币奖励--------")
                print(f"未领取的奖励次数: {unclaimed_awards} 次")
                return unclaimed_awards

            except json.JSONDecodeError:
                print("解密后的数据不是有效的JSON，原始数据:", decrypted_data)
        else:
            print("请检查datas是否正确")

    except requests.RequestException as e:
        print(f"请求出现异常: {e}")
        if 'response' in locals():
            print(f"响应状态码: {response.status_code}")
            print(f"响应内容: {response.text}")



def gq(datas):
    print("----国庆限时活动----已开启")
    url = "https://freevideo.zqqds.cn/free-video-portal/portal/1157"
    data = {}
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

        playAccumulate = json.loads(decrypted_data).get('playAccumulate')
        dailyAccumulate = json.loads(decrypted_data).get('dailyAccumulate')
        if dailyAccumulate is None or playAccumulate is None:
            print("获取国庆活动数据失败")
            return None
        print(f"累计天数: {dailyAccumulate} 天")
        print(f"累计观看时间: {playAccumulate} 分钟")  
        dailyRafflePrizeId = json.loads(decrypted_data).get('dailyRafflePrizeId')   
        dailyRaffle = json.loads(decrypted_data).get('dailyRaffle', [])

        prizeName = None

        for raffle in dailyRaffle:
            if raffle['id'] == dailyRafflePrizeId:
                prizeName = raffle['prizeName']
                break

        if prizeName:
            print(f"今天抽中的奖品: {prizeName}")
        else:
            print("今日还没有抽奖")
            delay = random.randint(6, 10)  
            print(f"等待 {delay} 秒后去抽奖")
            time.sleep(delay)  
            gq1(datas)

    except json.JSONDecodeError:
        print("解密后的数据不是有效的JSON格式")
    except requests.exceptions.RequestException as e:
        print(f"请求失败，错误信息：{e}")
    
    return None  

def gq1(datas):
    url = "https://freevideo.zqqds.cn/free-video-portal/portal/1159"
    data = {"type":1}
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
        msg = json.loads(decrypted_data).get('msg')
        if msg:
            print(f"抽奖成功: {msg}")
        else:
            print("抽奖失败")

    except json.JSONDecodeError:
        print("解密后的数据不是有效的JSON格式")
    except requests.exceptions.RequestException as e:
        print(f"请求失败，错误信息：{e}")
    
    return None 



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

        cjb(datas)
        
        current_datetime = datetime.datetime.now()
        current_date = current_datetime.date()
        activity_start_date = datetime.date(2024, 10, 1)
        activity_end_date = datetime.date(2024, 10, 7)

        if activity_start_date <= current_date <= activity_end_date:
            gq(datas)
        else:
            print("----国庆限时活动----已关闭")

if __name__ == "__main__":
    main()



