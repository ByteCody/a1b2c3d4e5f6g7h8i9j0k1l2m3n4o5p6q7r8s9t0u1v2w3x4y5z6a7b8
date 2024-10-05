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


def get_headers(token=None):
    headers = fixed_headers.copy()  
    if token:
        headers["token"] = token  
    return headers




def rwjc(token):
    url = 'https://api.tianjinzhitongdaohe.com/sqx_fast/app/user/selectUserById'
    headers = get_headers(token=token)

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 0:
                user_data = data.get('data', {})
                user_name = user_data.get('userName', '未知')
                phone = user_data.get('phone', '未知')
                video_sec = int(user_data.get('videoSec') or 0)

                print(f"用户名: {user_name}")
                print(f"手机号: {phone}")
                print("\n-----每日任务 ------")

                all_courses_count = 10
                good_video_limit = 9080  

                if video_sec < good_video_limit:
                    total_watched = video_sec
                    print(f"看视频领取金币({video_sec}/{good_video_limit}秒)")

                    course_index = 0  

                    while total_watched < good_video_limit and course_index < all_courses_count:
                        print("----获取剧集数据中----状态")
                        course_id = tj(token)  
                        if not course_id:
                            print("无法获取短剧ID")
                            return None

                        episode_count, course_details_id = tj1(token, course_id)  
                        print(f"短剧共有 {episode_count} 集")

                        start_course_details_id = course_details_id
                        end_course_details_id = start_course_details_id + episode_count - 1

                        for i in range(episode_count):
                            wait_sec = random.randint(60, 80)  
                            current_course_details_id = start_course_details_id + i

                            if current_course_details_id > end_course_details_id:
                                print(f"已完成第 {course_index+1} 个短剧的所有剧集观看任务")
                                break

                            video_sec = wait_sec
                            if total_watched + video_sec > good_video_limit:
                                video_sec = good_video_limit - total_watched
                            print("----模拟看剧中----状态")
                            tj2(token, video_sec, course_id, current_course_details_id)
                            print(f"当前观看时长: {video_sec} 秒")

                            total_watched += video_sec
                            remaining_videos = good_video_limit - total_watched

                            print(f"总观看时长: {total_watched} 秒, 剩余观看时长: {remaining_videos} 秒")

                            if total_watched >= good_video_limit:
                                print(f"已完成所有任务，共观看 {total_watched} 秒视频")
                                break

                            print(f"等待 {wait_sec} 秒后继续看剧")
                            time.sleep(wait_sec)

                       
                        course_index += 1

                       
                        if course_index >= all_courses_count:
                            print("课程索引超出范围，没有更多的短剧可供选择")
                            return 

                    
                    response = requests.get(url, headers=headers)
                    if response.status_code == 200:
                        data = response.json()
                        updated_video_sec = int(data.get('data', {}).get('videoSec', 0))
                        if updated_video_sec >= good_video_limit:
                            print(f"已成功完成每日任务，当前观看时长为 {updated_video_sec}/{good_video_limit} 秒")
                    else:
                        print(f"验证请求失败，状态码: {response.status_code}")
                        return None
                else:
                    print(f"已达到每日视频观看上限 ({video_sec}/{good_video_limit})")
                    return None
            else:
                print("token 已失效")
                return None
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return None
    except requests.exceptions.Timeout:
        print("请求超时，请稍后重试")
        return None
    except requests.exceptions.RequestException as e:
        print(f"请求出现错误: {e}")
        return None






def tj(token):
    url = "https://api.tianjinzhitongdaohe.com/sqx_fast/app/common/type/922"
    headers = get_headers(token=token)

    try:
        
        response = requests.get(url, headers=headers, timeout=10)

        
        if response.status_code == 200:
            response_data = response.json()

            
            if response_data.get('code') == 0:
                data = response_data.get('data', {})
                course_list = data.get('courseList', [])

                if course_list:
                    
                    first_course = course_list[0]
                    course_id = first_course.get('courseId')
                    print(f"第一个短剧ID: {course_id}")
                    return course_id
                else:
                    print("没有找到更多短剧")
                    return None
            else:
                print(f"响应失败，错误代码: {response_data.get('code')}")
                return None
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return None

    except requests.exceptions.Timeout:
        print("请求超时，请检查网络连接或稍后重试")
        return None
    except requests.exceptions.RequestException as e:
        print(f"请求发生错误: {e}")
        return None




def tj1(token, course_id):
    url = "https://api.tianjinzhitongdaohe.com/sqx_fast/app/course/selectCourseDetailsById"
    params = {'id': course_id, 'token': token}
    
    headers = get_headers(token=token)  

    try:
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        
        if response.status_code == 200:
            data = response.json()
            
           
            lists_detail = data.get("data", {}).get("listsDetail", [])
            if not lists_detail:
                print("未获取到剧集数据")
                return 0
            
            
            episode_count = len(lists_detail) 

            
            first_course_details_id = lists_detail[0].get("courseDetailsId") if lists_detail else None
               
            return episode_count, first_course_details_id
        
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return 0

    except requests.RequestException as e:
        print(f"请求过程中出现异常: {e}")
        return 0


def tj2(token, video_sec, course_id, current_course_details_id):
    
    url = "https://api.tianjinzhitongdaohe.com/sqx_fast/app/user/updateUserSec"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; 21091116UC Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/127.0.6533.64 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/29.09091)',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/x-www-form-urlencoded',
        'token': token
    }
    data = {
        'videoSec': video_sec,
        'courseId': course_id,
        'courseDetailsId': current_course_details_id
    }
    try:
        
        response = requests.post(url, headers=headers, data=data)
        
        
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get('code') == 0:
                print("观看进度更新成功")
            else:
                print(f"更新失败: {response_data.get('msg', '无详细错误信息')}")
        else:
            print(f"请求失败: 状态码 {response.status_code}")

    except requests.RequestException as e:
        print(f"请求异常: {e}")


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


