# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 20:45:03 2020

@author: WZYWXYWLY
"""

import requests
from lxml import etree
import json
import pandas as pd
import datetime
import csv
import time
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np

def get_inner_html(node):                                                                                                                                                  
    html = etree.tostring(node, encoding="utf8").decode('utf8')            
    p_begin = html.find('>') + 1                                               
    p_end = html.rfind('<')                                                    
    return html[p_begin: p_end]

def getChineseFont():
    return FontProperties(fname ='C:/Windows/Fonts/simsun.ttc')

def remove_duplicate(one_list):
    '''
    使用排序的方法，清除重复项
    '''
    result_list=[]
    temp_list=sorted(one_list)
    i=0
    while i<len(temp_list):
        if temp_list[i] not in result_list:
            result_list.append(temp_list[i])
        else:
            i+=1
    return result_list
##本机Headers。cookies自行登录后填写。
headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh,zh-TW;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
        'Connection': 'keep-alive',
        'Cookie':   '_ntes_nnid=fc7d2371b30ac58e7990dfaa1ee300a6,1560145275865;'
        '_ntes_nuid=fc7d2371b30ac58e7990dfaa1ee300a6; UM_distinctid=16fd5dad70d5c'
        '-03d463be05c26a-b383f66-1fa400-16fd5dad70e98f; vinfo_n_f_l_n3=a0eb2d288d62'
        'd624.1.1.1579840886280.1579840941043.1579854278756; nts_mail_user=kongcongw'
        'en27@163.com:-1:1; mail_psc_fingerprint=ec57a74f997505057a4ed5f0c7467cd6; mp'
        '_MA-9ADA-91BF1A6C9E06_hubble=%7B%22sessionReferrer%22%3A%20%22https%3A%2F%2Fc'
        'ampus.163.com%2Fapp%2Findex%22%2C%22updatedTime%22%3A%201585455034684%2C%22ses'
        'sionStartTime%22%3A%201585455034681%2C%22sendNumClass%22%3A%20%7B%22allNum%22%'
        '3A%202%2C%22errSendNum%22%3A%200%7D%2C%22deviceUdid%22%3A%20%226ac01d1d-68c4-4'
        'ce9-9f90-8bca75038391%22%2C%22persistedTime%22%3A%201585455034677%2C%22LASTEVEN'
        'T%22%3A%20%7B%22eventId%22%3A%20%22da_screen%22%2C%22time%22%3A%201585455034684'
        '%7D%2C%22sessionUuid%22%3A%20%227814867a-1461-4461-bfcc-ca92d8690870%22%7D; Dev'
        'ice-Id=tgkWWxTOA1x6NLKQMzSr; _ga=GA1.2.1321289725.1585829397; _gid=GA1.2.633512'
        '683.1585829397; Locale-Supported=zh-Hans; game=csgo; NTES_YD_SESS=RqrZBIOm4bXTzx'
        'yraxmhMd3CK6wND3PS3zHh6j7S6glJ490e4zw3CZpUU6Te6G.7VI1Qt1XjtzHfA2_szyttgnLZne8DQV'
        'uRBa3kWJ6qYaXdrr9tofWSPqaIzPSk3Q8mwYJRRn77suSwZRhVzGNFpvhKOC_Lt0lhXwl3jyOMNymlN4'
        'gG2PtWOdon.Sx9chRlP4tvl5OiJ.wcMSrEQYFJX6X1Flp7yZ30MUL2H7a5zLFMp; S_INFO=15859096'
        '38|0|3&80##|18965804660; P_INFO=18965804660|1585909638|0|netease_buff|00&99|fuj&15'
        '85829475&netease_buff#fuj&350200#10#0#0|&0|null|18965804660; session=1-ypzL2MGXb75VC'
        'n4BJSk-ybGdduNbzATCRtTrl6ExJGPu2046253215; _gat_gtag_UA_109989484_1=1; csrf_token=ImU'
        'zNDhkZTI3OGU5NGM2NTk5ZDYxZTUyNjMyZTU2OGJhOGVjZGU4ZGEi.EWiilQ.oWMrV9TOi2UryWtPQY6sn4fpQLw',
        'Host': 'buff.163.com',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36}'
        }

max_num = 4000
for total_num in range(max_num):
    no = 42000+total_num  ##饰品代码从42000开始，到46000结束。但总饰品范围远不止这些
    url1 = 'https://buff.163.com/api/market/goods/price_history/buff?game=csgo&goods_id='+str(no)
    url2 = 'https://buff.163.com/market/goods?goods_id='+str(no)+'&from=market#tab=selling'
    r = requests.get(url1,headers = headers)
    ## https://buff.163.com/market/goods?goods_id=42981&from=market#tab=selling
    ro = requests.get(url2,headers = headers)
    tree = etree.HTML(ro.text)
    try:
        gametype = get_inner_html(tree.xpath("//*[@class='w-Select']/h3")[0])[-5:]
        name = get_inner_html(tree.xpath("//*[@class='cru-goods']")[0])
    except:
        continue
    ##判断是否是CSGO饰品
    if total_num % 10 == 0:
        print('Searching No.%d / %d price history.'%(total_num+1,max_num))
    if gametype != 'CS:GO' or name[:2] == '印花':
        continue
    rresult = json.loads(r.text)
    price_history = rresult['data']['price_history']
    
    '''
    # 使用time
    timeStamp = 1381419600
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
    print(otherStyleTime)   # 2013--10--10 23:40:00
    # 使用datetime
    timeStamp = 1381419600
    dateArray = datetime.datetime.fromtimestamp(timeStamp)
    otherStyleTime = dateArray.strftime("%Y--%m--%d %H:%M:%S")
    print(otherStyleTime)   # 2013--10--10 23:40:00
     # 使用datetime，指定utc时间，相差8小时
    timeStamp = 1381419600
    dateArray = datetime.datetime.utcfromtimestamp(timeStamp)
    otherStyleTime = dateArray.strftime("%Y--%m--%d %H:%M:%S")
    print(otherStyleTime)   # 2013--10--10 15:40:00
    '''
    price_index = []
    price_values = []
    for j,i in enumerate(price_history):
        get_time = datetime.datetime.fromtimestamp(i[0]/1000)
        strtime = get_time.strftime('%Y-%m-%d %H:%M:%S')
        price_history[j][0] = strtime
        price_index.append(get_time)
        price_values.append(i[1])
    
    ''' 画图
    price_history_df = pd.DataFrame(data = price_values, index = price_index)
    price_history_df.plot(figsize = (12,6))
    plt.title(name,fontproperties = getChineseFont())
    plt.legend('Price')
    '''
    
    '''
    写入CSV文件
    '''
    name = name.replace('|','')
    name = name.replace('*','')
    name = name.replace(':','')
    name = name.replace('"','')
    fileopen = 0
    try:
        open(file=name+'.csv')
    except:
        fileopen = 1
    
    '''
    第一次写入
    '''
    if fileopen == 1:
        with open(name+'.csv','w',encoding = 'utf-8',newline = '') as f:
            csv_writer = csv.writer(f)
            for i in range(len(price_index)):
                csv_writer.writerow([price_index[i],price_values[i]])
    else:
        with open(name+'.csv','r') as f:
            f_csv = csv.reader(f)
            price_list = []
            for row in f_csv:
                for i in row:
                    row[1] = float(row[1])
                price_list.append(row)
        price_list.extend(price_history)
        
        price_list = remove_duplicate(price_list) ## 重复数据删除数据更新
        with open(name+'.csv','w',encoding = 'utf-8',newline = '') as f:
            csv_writer = csv.writer(f)
            for i in range(len(price_list)):
                csv_writer.writerow([price_list[i][0],price_list[i][1]])
    
