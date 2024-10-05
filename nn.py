import datetime
import os
import random
import time
import requests
from datetime import datetime

fixed_headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 12; 21091116UC Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/127.0.6533.64 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/29.09091)',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'Content-Type': 'application/x-www-form-urlencoded'
}

fixed1_headers = {
   "user-agent": "Mozilla/5.0 (Linux; Android 9; Redmi Note 8 Pro Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/128.0.6613.88 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/27.636364)",
    "Content-Type": "application/json",
    "Content-Length": "64",
    "Host": "api.tianjinzhitongdaohe.com",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip"
}

def get_headers(token=None):
    headers = fixed_headers.copy()  
    if token:
        headers["token"] = token  
    return headers

def get1_headers(token=None):
    headers = fixed1_headers.copy()  
    if token:
        headers["token"] = token  
    return headers

def rwjc(token):
    url = 'https://api.tianjinzhitongdaohe.com/sqx_fast/app/user/selectUserById'
    headers = get_headers(token=token)  

    try:
        response = requests.get(url, headers=headers, timeout=10)  

        if response.status_code == 200:
            try:
                data = response.json()
            except ValueError as e:
                print(f"解析JSON数据时出错: {e}")
                return

            if data.get('code') == 0:
                user_data = data.get('data', {})
                user_name = user_data.get('userName', '未知')
                phone = user_data.get('phone', '未知')
                userId = user_data.get('userId', '未知')

                lookDayVideoNum = int(user_data.get('lookDayVideoNum') or 0)
                okLookVideoNum = int(user_data.get('okLookVideoNum') or 0)
                goodVideo = int(user_data.get('goodVideo') or 0)
                okGoodVideo = int(user_data.get('okGoodVideo') or 0)
                collectVideo = int(user_data.get('collectVideo') or 0)
                okCollectVideo = int(user_data.get('okCollectVideo') or 0)
                shareVideo = int(user_data.get('shareVideo') or 0)
                okShareVideo = int(user_data.get('okShareVideo') or 0)

                print(f"用户名: {user_name}")
                print(f"手机号: {phone}")
                print("\n-----每日任务 ------")
                qd(token, userId)  

                lookDayVideoLimit = 20
                okLookVideoLimit = 5
                goodVideoLimit = 2

                if lookDayVideoNum <= lookDayVideoLimit:
                    remaining_videos = lookDayVideoLimit - lookDayVideoNum
                    print(f"看视频广告领金币({lookDayVideoNum}/{lookDayVideoLimit})")
                    for _ in range(remaining_videos):
                        delay = random.randint(30, 70)
                        print(f"{delay} 秒后去完成观看视频广告任务")
                        time.sleep(delay)
                        kgg(token)  

                if okLookVideoNum < okLookVideoLimit:
                    delay = random.randint(3, 10)
                    print(f"{delay} 秒后去领取看视频广告金币")
                    time.sleep(delay)
                    lqz = "lookVideoNum" 
                    kgg1(token, lqz) 

                if goodVideo <= goodVideoLimit:
                    remaining_videos = goodVideoLimit - goodVideo
                    print(f"点赞剧集({goodVideo}/{goodVideoLimit})")

                    course_ids = dz(token)
                    if not course_ids:
                        print("未获取到ID，任务终止")
                        return
                    
                    for i in range(min(remaining_videos, len(course_ids))):
                        delay = random.randint(3, 10)
                        print(f"{delay} 秒后去完成点赞剧集任务")
                        time.sleep(delay)

                        course_id = course_ids[i]  
                        course_details_id = dz1(token, course_id)  
                        if course_details_id:
                            id = "2" 
                            dz2(token, id , course_id, course_details_id)   

                if okGoodVideo < goodVideoLimit:
                    delay = random.randint(3, 10)
                    print(f"{delay} 秒后去领取点赞剧集金币")
                    time.sleep(delay)
                    lqz = "goodVideo" 
                    kgg1(token, lqz)

                if collectVideo <= goodVideoLimit:
                    remaining_videos = goodVideoLimit - collectVideo
                    print(f"收藏新剧({collectVideo}/{goodVideoLimit})")

                    course_ids = dz(token)
                    if not course_ids:
                        print("未获取到ID，任务终止")
                        return
                    
                    for i in range(min(remaining_videos, len(course_ids))):
                        delay = random.randint(3, 10)
                        print(f"{delay} 秒后去完成收藏新剧任务")
                        time.sleep(delay)

                        course_id = course_ids[i]
                        if course_id:  
                            sc(token, course_id)
                        else:
                            print(f"无效的视频ID: {course_id}")

                if okCollectVideo < goodVideoLimit:
                    delay = random.randint(3, 10)
                    print(f"{delay} 秒后去领取收藏新剧金币")
                    time.sleep(delay)
                    lqz = "collectVideo" 
                    kgg1(token, lqz)

                if shareVideo <= goodVideoLimit:
                    remaining_videos = goodVideoLimit - shareVideo
                    print(f"分享新剧({shareVideo}/{goodVideoLimit})")

                    
                    for i in range(remaining_videos):
                        delay = random.randint(3, 10)
                        print(f"{delay} 秒后去完成分享新剧任务")
                        time.sleep(delay)
                        fx(token)  

                if okShareVideo < goodVideoLimit:
                    delay = random.randint(3, 10)
                    print(f"{delay} 秒后去领取分享新剧金币")
                    time.sleep(delay)
                    lqz = "shareVideo" 
                    kgg1(token, lqz)

                print("\n-----资产查询 ------")
                zc(token)


            else:
                print("token 已失效")
        else:
            print(f"请求失败，状态码: {response.status_code}")

    except requests.exceptions.Timeout:
        print("请求超时，请稍后重试")
    except requests.exceptions.RequestException as e:
        print(f"请求出现错误: {e}")


def kgg(token):
    url = 'https://api.tianjinzhitongdaohe.com/sqx_fast/app/integral/addLookVideoNum'
    headers = get_headers(token=token)  

    try:
        
        response = requests.get(url, headers=headers)

        
        if response.status_code == 200:
            
            data = response.json()

            
            if data.get('code') == 0:

                print("看广告成功")


            else:
                
                print("看广告失败")
        else:
            
            print(f"请求失败，状态码: {response.status_code}")
    except requests.exceptions.Timeout:
        print("请求超时，请稍后重试")
    except requests.exceptions.RequestException as e:
        print(f"请求出现错误: {e}")

def kgg1(token, lqz):
    url = f'https://api.tianjinzhitongdaohe.com/sqx_fast/app/integral/{lqz}'
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


def qd(token, userId):
    url = 'https://api.tianjinzhitongdaohe.com/sqx_fast/app/integral/selectIntegralDay'
    params = {
        'classify': 1,
        'userId': userId
    }
    headers = get_headers(token=token)  

    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return
    except Exception as e:
        print(f"请求过程中出现异常: {e}")
        return

    
    if data.get('msg') == 'success' and data.get('code') == 0:
        sign_ins = data.get('data', [])
        today = datetime.now().strftime('%Y-%m-%d')
        today_signed_in = False

        
        for sign_in in sign_ins:
            if sign_in and sign_in.get('signTime') == today:
                today_signed_in = True
                print("今天已经签到过了")
                break  

        if not today_signed_in:
            print(f"今天（{today}）还没有签到")
            qd1(token, today)  
    else:
        print(f"处理数据失败: {data.get('msg')}")

def qd1(token, today):
    url = f'https://api.tianjinzhitongdaohe.com/sqx_fast/app/integral/signIn?date={today}'
    headers = get_headers(token=token)  

    try:
        
        response = requests.get(url, headers=headers)

        
        if response.status_code == 200:
            
            data = response.json()

            
            if data.get('code') == 0:
                msg = data.get('msg')
                print(f"签到成功，状态: {msg}")
            else:
                msg = data.get('msg')
                print(f"签到失败，状态: {msg}")
        else:
            
            print(f"请求失败，状态码: {response.status_code}")
    except requests.exceptions.Timeout:
        print("请求超时，请稍后重试")
    except requests.exceptions.RequestException as e:
        print(f"请求出现错误: {e}")


def dz(token):
    url = "https://api.tianjinzhitongdaohe.com/sqx_fast/app/course/selectCourse"
    params = {
        "limit": 12,
        "page": 1,
        "sort": 3,
        "classifyId": ""
    }
    headers = get_headers(token=token)

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)

        if response.status_code == 200:
            response_data = response.json()
            if response_data.get('code') == 0:
                data = response_data.get('data', {})
                course_list = data.get('list', [])

                if course_list:
                    
                    return [course.get('courseId') for course in course_list if course.get('courseId') is not None]
                else:
                    print("没有找到ID")
            else:
                print(f"获取数据失败，错误代码: {response_data.get('code')}, 错误信息: {response_data.get('message', '未知错误')}")
        else:
            print(f"请求失败，HTTP状态码: {response.status_code}")

    except requests.exceptions.Timeout:
        print("请求超时，请稍后重试")
    except requests.exceptions.RequestException as e:
        print(f"请求出现错误: {e}")

    return []

def dz1(token, course_id):
    url = "https://api.tianjinzhitongdaohe.com/sqx_fast/app/course/selectCourseDetailsByCourseId"
    params = {'id': course_id, 'token': token}
    headers = get_headers(token=token)

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 0:
                course_data = data.get('data', {})
                return course_data.get('courseDetailsId')
            else:
                print(f"获取ID失败，错误代码: {data.get('code')}, 错误信息: {data.get('message', '未知错误')}")
        else:
            print(f"请求失败，状态码: {response.status_code}")

    except requests.exceptions.Timeout:
        print("请求超时，请稍后重试")
    except requests.exceptions.RequestException as e:
        print(f"请求出现错误: {e}")

    return None

def dz2(token, id, course_id, course_details_id):
    url = 'https://api.tianjinzhitongdaohe.com/sqx_fast/app/courseCollect/insertCourseCollect'
    headers = get1_headers(token=token)
    data = {
        "courseId": course_id, 
        "courseDetailsId": course_details_id, 
        "classify": id, 
        "type": 1
    }
    


    try:
        response = requests.post(url, json=data, headers=headers)
        

        if response.status_code == 200:
            response_data = response.json()
            if response_data.get('code') == 0:
                print("成功")
            else:
                print(f"失败，错误码: {response_data.get('msg')}")
        else:
            print(f"请求失败，状态码: {response.status_code}，响应内容: {response.text}")

    except requests.exceptions.Timeout:
        print("请求超时，请稍后重试")
    except requests.exceptions.RequestException as e:
        print(f"请求出现错误: {e}")

def sc(token, course_id):
    url = 'https://api.tianjinzhitongdaohe.com/sqx_fast/app/courseCollect/insertCourseCollect'
    headers = get1_headers(token=token)
    data = {
        "courseId": course_id, 
        "classify": 1, 
        "type": 1
    }
    

    try:
    
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            if response_data.get('code') == 0:
                print("收藏成功")
            else:
                print(f"收藏失败，错误码: {response_data.get('code')}")
        else:
            print(f"请求失败，状态码: {response.status_code}")

    except requests.exceptions.Timeout:
        print("请求超时，请稍后重试")
    except requests.exceptions.RequestException as e:
        print(f"请求出现错误: {e}")

def fx(token):
    url = "https://api.tianjinzhitongdaohe.com/sqx_fast/app/user/shareCourse"

    
    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 12; 21091116UC Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/127.0.6533.64 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/29.09091)",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "0",
        "Host": "api.tianjinzhitongdaohe.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        'token': token
    }

    try:
        
        response = requests.post(url, headers=headers)

        
        if response.status_code == 200:
            try:
                
                response_data = response.json()
                
                
                if response_data.get('code') == 0:
                    print("分享成功")
                else:
                    print(f"分享失败，错误码: {response_data.get('code')}")
            except ValueError:
                
                print("响应非JSON格式")
        else:
            print(f"请求失败，状态码: {response.status_code}")

    except requests.exceptions.Timeout:
        print("请求超时，请稍后重试")
    except requests.exceptions.RequestException as e:
        print(f"请求出现错误: {e}")

def zc(token):
    url = "https://api.tianjinzhitongdaohe.com/sqx_fast/app/integral/selectByUserId"
    
    headers = get_headers(token=token)
    
    # 发送GET请求
    response = requests.get(url, headers=headers)
    
    # 检查请求状态码是否为200
    if response.status_code == 200:
        try:
            # 尝试将响应转换为JSON格式
            response_data = response.json()
            
            # 判断响应中的 code 是否为 0，代表成功
            if response_data['code'] == 0:
                integral_num = response_data['data']['integralNum']
                print(f"今日金币:{integral_num}")
                money_sum = zc1(token)
                if money_sum:
                    print(f"总余额:{money_sum}元")
            else:
                # 打印错误消息
                print("查询资产失败，消息：", response_data['msg'])
        except ValueError:
            print("响应不是有效的JSON格式。")
    else:
        print(f"请求失败，状态码：{response.status_code}")

# 查询邀请奖励函数
def zc1(token):
    url = "https://api.tianjinzhitongdaohe.com/sqx_fast/app/invite/selectInviteMoney"
    
    headers = get_headers(token=token)
    
    # 发送GET请求
    response = requests.get(url, headers=headers)
    
    # 检查请求状态码是否为200
    if response.status_code == 200:
        try:
            # 尝试将响应转换为JSON格式
            response_data = response.json()
            
            # 判断响应中的 code 是否为 0，代表成功
            if response_data['code'] == 0:
                money_sum = response_data['data']['inviteMoney']['moneySum']
                return money_sum
            else:
                # 打印错误消息
                print("查询邀请奖励失败，消息：", response_data['msg'])
        except ValueError:
            print("响应不是有效的JSON格式。")
    else:
        print(f"请求失败，状态码：{response.status_code}")
    return None


def main():
    
    token_vars = os.environ.get('nnck')
    
    if token_vars is None:
        print("请设置 nnck 环境变量")
        return

    tokens = token_vars.split('@')  
    
    
    for index, token in enumerate(tokens, start=1):
        account_id = f"账号{index}"
        print(f"\n开始运行 {account_id}")
        rwjc(token)  


if __name__ == "__main__":
    main()
