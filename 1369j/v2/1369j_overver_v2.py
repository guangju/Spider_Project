import requests
from lxml import etree
import pymysql
import json
import conf_v2 as conf
import os
import time
import random
import re
import sys
#qq部分


import win32gui
import win32con
import win32clipboard as w
import time


def getText():
    """获取剪贴板文本"""
    w.OpenClipboard()
    d = w.GetClipboardData(win32con.CF_UNICODETEXT)
    w.CloseClipboard()
    return d


def setText(aString):
    """设置剪贴板文本"""
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
    w.CloseClipboard()


def send_qq(to_who, msg):
    """发送qq消息
    to_who：qq消息接收人
    msg：需要发送的消息
    """
    # 将消息写到剪贴板
    setText(msg)
    # 获取qq窗口句柄
    qq = win32gui.FindWindow(None, to_who)
    # 投递剪贴板消息到QQ窗体
    win32gui.SendMessage(qq, 258, 22, 2080193)
    win32gui.SendMessage(qq, 770, 0, 0)
    # 模拟按下回车键
    win32gui.SendMessage(qq, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    win32gui.SendMessage(qq, win32con.WM_KEYUP, win32con.VK_RETURN, 0)

def my_conn(host,user,passwd,port,db):
    conn = pymysql.connect(
        host=host,
        user=user,
        passwd=passwd,
        port=port,
        db=db,
        charset='utf8mb4',
        cursorclass = pymysql.cursors.DictCursor
    )

    return conn
def my_close(conn):
    conn.close()
def my_delete(conn):
    cursor = conn.cursor()
    sql = 'TRUNCATE TABLE 1369j_data_test'
    cursor.execute(sql)
    conn.commit()
def my_insert(conn,data):
    keys_sql = ','.join(data.keys())
    values_sql = []
    for v in data.values():
        # v = ''.join(v)
        values_sql.append('"%s"' % v)
    a = ','.join(values_sql)
    sql = "INSERT INTO 1369j_data_test(%s) VALUES (%s)" % (keys_sql, a)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
def my_select(conn):
    sql = 'select number1,number2,number3,number4,number5,number6,number7,number8,number9,number10 FROM 1369j_data_test ORDER BY id desc LIMIT 1'
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchone()
    return data
def get_data(conn,old_data,new_data,old_number,len_item):
    global number_dict

    out_data = new_data

    # for len_item in conf.len_number_list:
    old_if_data = []
    for old_n in len_item:
        if old_n ==10:
            old_n = 0
        old_if_data.append('%s'%old_data['number%s' % old_n])
    all_if_data = []
    for new_n in range(1, 11):
        all_if_data.append(old_data['number%s' % new_n])
    other_list = []
    for item in len_item:
        item_number = '%s'%out_data['number%s'%item]
        if str(item_number) == '10':
            item_number = 0
        other_list.append(str(item_number))

    other_list.sort()
        # for old_number in conf.new_if_list:
    print('第%s-%s列 与 这组%s ----%s'%(old_number,out_data['number%s'%old_number],old_if_data,len_item))
    if str(out_data['number%s'%old_number]) not in old_if_data:
        number_dict['%s'%old_number] = int(number_dict['%s'%old_number]) + 1
    else:
        number_dict['%s' % old_number] = 0
    for number_key in number_dict:
        if number_dict[number_key] >=conf.alert:
            monitor_number = out_data['number%s'%number_key]
            if number_key == 10:
                number_key=0
            msg = '监测%s 第%s道 %s,现在记录是%s次,超过%s次报警,对比的是%s,建议' % (out_data['time_'], number_key, monitor_number, number_dict[number_key], conf.alert, old_if_data,)
            if str(number_key) == '10':
                number_key_out = '0'
            else:
                number_key_out= number_key
            jianyi_number = conf.jianyi_dict.get('%s'%number_dict[number_key])
            msg1 = '%s.%s.%s' % (number_key_out, ''.join(other_list),jianyi_number)
            print(msg,msg1)
            send_qq(conf.to_who, msg)
            time.sleep(1)
            send_qq(conf.to_who, msg1)

            time.sleep(1)
    fw = open('%s/number.conf'%root_dir, 'w', encoding='utf-8')
    fw.write(json.dumps(number_dict,ensure_ascii=False))
    fw.close()
if __name__ == '__main__':

    url = 'https://www.1396j.com/xyft/kaijiang'
    wb_data = requests.get(url=url)
    et = etree.HTML(wb_data.text)
    all_list= []
    for i, time_ in zip(et.xpath('//*[@id="history"]//tr/td[2]/div'), et.xpath('//*[@id="history"]//tr/td[1]')):
        count = 1
        out_data = {}
        for number in i.xpath('string()').strip().split():
            out_data['number%s' % count] = number
            count += 1
        out_data['time_'] = time_.xpath('string()')
        all_list.append(out_data)
    all_list.reverse()
    all_list.append(0)
    conn = my_conn(host='www.muming8.com', user='zhang', passwd='zhang.123', port=3306, db='kehu')
    for old_number in conf.new_if_list:
        root_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
        number_dict = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0}
        fw = open('%s/number_col%s.conf' % (root_dir, old_number), 'w', encoding='utf-8')
        fw.write(json.dumps(number_dict, ensure_ascii=False))
        fw.close()
        for len_item in conf.len_number_list:
            for old_data,new_data in zip(all_list,all_list[1:-1]):
                # print(old_data,new_data)
                get_data(conn=conn,new_data=new_data,old_data=old_data,old_number=old_number,len_item=len_item)
    my_delete(conn=conn)
    my_close(conn=conn)



    while True:
        # try:

            conn = my_conn(host='www.muming8.com', user='zhang', passwd='zhang.123', port=3306, db='kehu')
            old_data = my_select(conn=conn)
            url = 'https://www.1396j.com/xyft/kaijiang'
            wb_data = requests.get(url=url)
            et = etree.HTML(wb_data.text)
            new_data = {}
            for i, time_ in zip(et.xpath('//*[@id="history"]//tr/td[2]/div'), et.xpath('//*[@id="history"]//tr/td[1]')):
                count = 1
                for number in i.xpath('string()').strip().split():
                    new_data['number%s' % count] = number
                    count += 1
                new_data['time_'] = time_.xpath('string()')
                break
            insert_count = 0
            # print(old_data)
            if str(old_data)  =='None':
                insert_count =10
                my_insert(conn=conn, data=new_data)
            else:
                for i, i1 in zip(old_data.keys(), new_data.keys()):
                    if str(new_data[i]) == str(old_data[i1]):
                        insert_count += 1

            if insert_count <= 9:
                my_insert(conn=conn, data=new_data)
                for old_number in conf.new_if_list:
                    root_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
                    f = open('%s/number_col%s.conf' % (root_dir, old_number), 'r', encoding='utf-8')
                    number_dict = json.load(f)
                    for len_item in conf.len_number_list:
                        # for old_data, new_data in zip(all_list, all_list[1:-1]):
                        get_data(conn=conn, new_data=new_data, old_data=old_data, old_number=old_number, len_item=len_item)
                print('运行完成一次,等待一分钟')
                time.sleep(60)
            else:
                print('未检测到新数据更新，等待一分钟')
                time.sleep(60)
            my_close(conn=conn)
        # except Exception as e:
        #     print(e)

