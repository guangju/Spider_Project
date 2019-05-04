import requests
from lxml import etree
import pymysql
import json
import conf as conf
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
        charset='utf8',
        cursorclass = pymysql.cursors.DictCursor
    )

    return conn
def my_close(conn):
    conn.close()
def my_insert(conn,data):
    keys_sql = ','.join(data.keys())
    values_sql = []
    for v in data.values():
        # v = ''.join(v)
        values_sql.append('"%s"' % v)
    a = ','.join(values_sql)
    sql = "INSERT INTO 1369j_data(%s) VALUES (%s)" % (keys_sql, a)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
def my_select(conn):
    sql = 'select number1,number2,number3,number4,number5,number6,number7,number8,number9,number10 FROM 1369j_data ORDER BY id desc LIMIT 1'
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchone()
    return data
def get_data(conn,old_data):
    url = 'https://www.1396j.com/xyft/kaijiang'
    wb_data = requests.get(url=url)
    et = etree.HTML(wb_data.text)
    number_dict = json.loads(open('%s/number.conf'%root_dir, 'r', encoding='utf-8').readline())
    for i,time_ in zip(et.xpath('//*[@id="history"]//tr/td[2]/div'),et.xpath('//*[@id="history"]//tr/td[1]')):
        count=1
        out_data = {}
        for number in i.xpath('string()').strip().split():
            out_data['number%s'%count] = number
            count+=1
        out_data['time_'] = time_.xpath('string()')
        insert_count = 0
        for i,i1 in zip(old_data.keys(),out_data.keys()):
            if str(out_data[i]) == str(old_data[i1]):
                insert_count+=1
        if insert_count <=9:
            old_if_data = []
            # for old_n in range(conf.start_len, conf.end_len + 1):
            for old_n in conf.len_number:
                if old_n ==10:
                    old_n = 0
                old_if_data.append('%s'%old_data['number%s' % old_n])
            all_if_data = []
            for new_n in range(1, 11):
                all_if_data.append(old_data['number%s' % new_n])
            other_list = []
            # for item in range(conf.start_len, conf.end_len + 1):
            for item in conf.len_number:
                item_number = '%s'%out_data['number%s'%item]
                if str(item_number) == '10':
                    item_number = 0
                other_list.append(str(item_number))

            other_list.sort()
            for old_number in range(1,11):
                if str(out_data['number%s'%old_number]) not in old_if_data:
                    number_dict['%s'%old_number] = int(number_dict['%s'%old_number]) + 1
                else:
                    number_dict['%s' % old_number] = 0
            # print(old_data)
            # print(out_data)
            my_insert(conn=conn, data=out_data)
            for number_key in number_dict:
                if number_dict[number_key] >=conf.alert:
                    monitor_number = out_data['number%s'%number_key]
                    if number_key == 10:
                        number_key=0
                    print('监测%s 第%s道 %s,现在记录是%s次,超过%s次报警,对比的是%s,建议%s.%s.'%(out_data['time_'],number_key,monitor_number,number_dict[number_key],conf.alert,old_if_data,number_key,''.join(other_list)))
                    msg = '监测%s 第%s道 %s,现在记录是%s次,超过%s次报警,对比的是%s,建议'%(out_data['time_'],number_key,monitor_number,number_dict[number_key],conf.alert,old_if_data,)
                    msg1 = '%s.%s'%(number_key,''.join(other_list))
                    send_qq(conf.to_who, msg)
                    time.sleep(1)
                    send_qq(conf.to_who, msg1)

                    time.sleep(1)
            fw = open('%s/number.conf'%root_dir, 'w', encoding='utf-8')
            fw.write(json.dumps(number_dict,ensure_ascii=False))
            fw.close()
            break
        else:
            break


if __name__ == '__main__':
    while True:
        try:
            root_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
            conn = my_conn(host='www.muming8.com', user='zhang', passwd='zhang.123', port=3306, db='kehu')
            old_data =my_select(conn=conn)
            get_data(conn=conn,old_data=old_data)
            my_close(conn=conn)
            print('运行完成/一次等待60秒')
            time.sleep(60)
        except:
            print('运行错误-等待2-3秒后从新运行')
            time.sleep(random.uniform(2,3))
