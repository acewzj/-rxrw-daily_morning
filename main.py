from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

def get_iciba_everyday_chicken_soup():
    url = 'http://open.iciba.com/dsapi/'  # 词霸免费开放的jsonAPI接口
    all_content = requests.get(url).json()  # 获取到json格式的内容，内容很多,json.loads: 将str转成dict
    English = all_content['content']  # 提取json中的英文鸡汤
    Chinese = all_content['note']  # 提取json中的中文鸡汤
    everyday_soup = English + '\n' + Chinese  # 合并需要的字符串内容
    return everyday_soup  # 返回结果
  

client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)

# wea, temperature = get_weather(city)
wea = "晴"
temperature = get_iciba_everyday_chicken_soup()

data = {
  "city":{"value": city, "color":get_random_color()},
  "weather":{"value":wea, "color":get_random_color()},
  "temperature":{"value":temperature, "color":get_random_color()},
  "love_days":{"value":get_count(), "color":get_random_color()},
  "birthday_left":{"value":get_birthday(), "color":get_random_color()},
  "words":{"value":get_words(), "color":get_random_color()}
}
res = wm.send_template(user_id, template_id, data)
print(res)
