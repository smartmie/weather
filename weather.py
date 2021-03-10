import requests
from bs4 import BeautifulSoup
import ast #文本转数组
import re
import pandas as pd
import csv

head = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive",
    "Cookie": "f_city=%E5%8D%97%E6%98%8C%7C101240101%7C; cityListCmp=%E5%8C%97%E4%BA%AC-101010100-20200531%7C%E4%B8%8A%E6%B5%B7-101020100-20200601%7C%E5%B9%BF%E5%B7%9E-101280101-20200602%7C%E6%B7%B1%E5%9C%B3-101280601-20200603%2Cdefault%2C20200531; cityListHty=101240601%7C101240611%7C101010100%7C101020100%7C101280101%7C101280601%7C101010300",
    "DNT": "1",
    "Host": "d1.weather.com.cn",
    "Referer": "http://www.weather.com.cn/weather1d/101240611.shtml",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37"
}

head_2 = {
    "DNT": "1",
    "Referer": "http://www.weather.com.cn/",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37"
}
#泰和天气
url = 'http://www.weather.com.cn/weather1d/101240611.shtml'
s_k = 'http://d1.weather.com.cn/sk_2d/101240611.html?_=1590931254696'

se = requests.session()
text = se.get(url, headers=head_2)
text.encoding = 'utf8'
soup = BeautifulSoup(text.content, 'lxml')
# div = soup.select("[class~=curve_livezs]")#正则
data_1 = soup.find_all(text = re.compile('hour3data'))
data_2 = data_1[0].partition('=')

data_3 = ast.literal_eval(data_2[2])

a=[]
for x in data_3['1d']:
    b = x.split(',')
    del b[1], b[5]
    a.append(b)



s_werther = se.get(s_k,headers = head)
s_werther.encoding = 'utf8'
wear_tai_he = s_werther.text.partition('=')#文本分割
# wear_tai_he = wear_tai_he[2].replace('0.','',1)  文本替换
s_werther = ast.literal_eval(wear_tai_he[2].strip())#清楚前后空格


p_data = "时间:{0}  {1}\n风速:{2}{3} {4}\n湿度:{5}\n天气:{6}\n"
p_data_ = "{0:{5}^}\t{1:^4}\t{2:^6}\t{3:{5}^6}\t{4:^4}"


p_data_list = ["时间",'天气','温度','风向','风速']
print(p_data.format(s_werther['date'], s_werther['time'], s_werther['WD'], s_werther['WS'], s_werther['wse'][4:], s_werther['sd'], s_werther['weather']))



with open('./t.csv','w',newline='') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(p_data_list)
    for y in a:
        new_data = p_data_.format(y[0], y[1], y[2], y[3], y[4], chr(12288))
        print(new_data)
        f_csv.writerow([y[0], y[1], y[2], y[3], y[4]])
        



