from time import sleep

import datetime
import re

import requests
import itchat

LOCATION = '重庆'  # 地址
REMARK_NAME = ''  # 微信上对方的备注名

# 获取天气数据接口
WEATHER_API = "https://www.sojson.com/open/api/weather/json.shtml?city={}"
# 设置requests请求头
HEADERS = {
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; "
                  "Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0",
}
MORNING_MSG = '今天是{},天气{},最高温度{},最低温度{}\n{}\n'  # 符号是微信表情包的符号表示
EVENING_MSG = '明天最高温度{},最低温度{}\n天气{},{}'
SEND_TIME = 9  # 目标早九点晚九点发信息


# 获取用户名 微信网页客户端对用户名进行了处理
def get_username():
    user_list = str(itchat.search_friends(remarkName=REMARK_NAME))
    pattern = re.compile(r'username=(@\w+)&')
    username = pattern.findall(user_list)[0]
    return username


# 获取天气资源，JSON格式
def gte_res_api():
    weather_info = requests.get(WEATHER_API.format(LOCATION, headers=HEADERS)).json()
    forecast = weather_info['data']['forecast']
    return forecast


# 早间信息，获取今天的信息发送
def send_mo_msg(forecast, username):
    # date 日期 type 天气类型 high 最高温 low 最低温 notice 温馨提示
    msg = MORNING_MSG.format(forecast[0]['date'],
                             forecast[0]['type'],
                             forecast[0]['high'],
                             forecast[0]['low'],
                             forecast[0]['notice'])
    itchat.send_msg(msg, toUserName=username)


# 晚间信息，获取明天的天气发送
def send_eve_msg(forecast, username):
    msg = EVENING_MSG.format(forecast[1]['high'],
                             forecast[1]['low'],
                             forecast[1]['type'],
                             forecast[1]['notice'])
    itchat.send_msg(msg, toUserName=username)


def main():
    # 保存登陆状态 会自动打开图片扫描登陆即可
    # 需发送二维码到终端 添加enableCmdQR=True
    # 如果二维码乱码设置因为字符格式 试试enableCmdQR=2
    itchat.auto_login(hotReload=True)
    forecast = gte_res_api()
    username = get_username()
    now = datetime.datetime.now()
    while True:
        if SEND_TIME == now.hour and now.minute == 0 and now.second == 0:
            send_mo_msg(forecast, username)
            sleep(60)   # 设置一个等待时间避免重复发出信息甚至导致错误信息 因为运行速度比秒速更快
        elif now.hour == SEND_TIME + 12 and now.minute == 0 and now.second == 0:
            send_eve_msg(forecast, username)
            sleep(60)


if __name__ == '__main__':
    main()
