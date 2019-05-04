import requests
import json
from lxml import etree
import datetime
import re
import pymysql
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
def my_insert(conn,data,table_name):
    try:
        keys_sql = ','.join(data.keys())
        values_sql = []
        for v in data.values():
            values_sql.append('"%s"' % v)
        a = ','.join(values_sql)
        sql = "INSERT INTO %s(%s) VALUES (%s)" % (table_name,keys_sql, a)
        print(sql)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        keys_sql = ','.join(data.keys())
        values_sql = []
        for v in data.values():
            values_sql.append("'%s'" % v)
        a = ','.join(values_sql)
        # print(len(data.values()))
        # print(len(data.keys()))
        sql = 'INSERT INTO %s(%s) VALUES (%s)' % (table_name, keys_sql, a)
        # print(sql)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
def get_videos(conn):
    url = 'https://live.kuaishou.com/graphql'
    post_data ={
	"operationName": "videoFeedsQuery",
	"variables": {
		"count": 100,
		"pcursor": "0"
	},
	"query": "fragment VideoMainInfo on VideoFeed {\n  photoId\n  caption\n  thumbnailUrl\n  poster\n  viewCount\n  likeCount\n  commentCount\n  timestamp\n  workType\n  type\n  useVideoPlayer\n  imgUrls\n  imgSizes\n  magicFace\n  musicName\n  location\n  liked\n  onlyFollowerCanComment\n  width\n  height\n  expTag\n  __typename\n}\n\nquery videoFeedsQuery($pcursor: String, $count: Int) {\n  videoFeeds(pcursor: $pcursor, count: $count) {\n    list {\n      user {\n        id\n        profile\n        name\n        __typename\n      }\n      ...VideoMainInfo\n      __typename\n    }\n    pcursor\n    __typename\n  }\n}\n"
    }
    headers= {
        'accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '699',
        'content-type': 'application/json',
        'Cookie': 'clientid=3; did=web_384d9fefd2e64e2313aaa2790227e1df; client_key=65890b29; didv=1556291904430; Hm_lvt_86a27b7db2c5c0ae37fee4a8a35033ee=1556291905; Hm_lpvt_86a27b7db2c5c0ae37fee4a8a35033ee=1556291905; kuaishou.live.bfb1s=ac5f27b3b62895859c4c1622f49856a4',
        'Host': 'live.kuaishou.com',
        'Origin': 'https://live.kuaishou.com',
        'Referer': 'https://live.kuaishou.com/v/hot/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
    }
    wb_data = requests.post(url=url,headers=headers,json=post_data,verify=False)
    wb_data.encoding ='utf-8'
    wb_data =json.loads(wb_data.text)
    count = 0
    for item in wb_data.get('data').get('videoFeeds').get('list'):
        out_data = item.get('user')
        print(count)
        get_user_info(conn=conn,data=out_data)
        get_user_vides(conn=conn,data=out_data,pcursor='')
        count+=1
        if count >=10:
            break


def parsingChar(type, data):
    fontscn_h57yip2q = {
        '\\uabcf': '4',
        '\\uaced': '3',
        '\\uaedd': '8',
        '\\uaede': '0',
        '\\uafcd': '6',
        '\\ubdaa': '5',
        '\\ubdcd': '1',
        '\\ubfad': '9',
        '\\uccda': '2',
        '\\ucfbe': '7',
    }
    fontscn_3jqwe90k = {
        '\\uaacb': '4',
        '\\uabcd': '3',
        '\\uacdd': '0',
        '\\uaefb': '8',
        '\\uafbc': '6',
        '\\ubbca': '1',
        '\\ubdca': '5',
        '\\ubfee': '9',
        '\\uccac': '2',
        '\\ucfba': '7',
    }
    fontscn_yuh4hy4p = {
        '\\uaabd': '5',
        '\\uaadd': '0',
        '\\uacde': '9',
        '\\uadaa': '2',
        '\\uadac': '1',
        '\\uadcb': '7',
        '\\uaeed': '8',
        '\\ubebb': '3',
        '\\ucbdc': '6',
        '\\ucccf': '4',
    }
    fontscn_qw2f1m1o = {################
        '\\uabcb': '4',
        '\\uaccd': '3',
        '\\uacda': '0',
        '\\uaeff': '8',
        '\\uafbb': '6',
        '\\ubdca': '1',
        '\\ubdcc': '5',
        '\\ubfef': '9',
        '\\uccaa': '2',
        '\\ucfba': '7',
    }
    fontscn_yx77i032 = {
        '\\uabce': '4',
        '\\uaccd': '6',
        '\\uaeda': '8',
        '\\uaefe': '0',
        '\\uafed': '3',
        '\\ubaaa': '5',
        '\\ubddd': '1',
        '\\ubfad': '2',
        '\\ubfae': '9',
        '\\uc44f': '7',
    }
    woff_dict = {'h57yip2q': fontscn_h57yip2q, '3jqwe90k': fontscn_3jqwe90k, 'yuh4hy4p': fontscn_yuh4hy4p,
                 'qw2f1m1o': fontscn_qw2f1m1o, 'yx77i032': fontscn_yx77i032}
    li = []
    new_data = (list(map(lambda x: x.encode('unicode_escape'), data)))
    for i in new_data:
        if len(str(i)) > 5:
            # print(type)
            num = woff_dict[type][str(i)[3:-1]]
            li.append(num)
        else:
            li.append(str(i)[2:-1])
    res = ''.join(li)
    # print(res)
    return res

def get_user_info(conn,data):

    url = 'https://live.kuaishou.com/profile/%s'%data.get('id')
    headers = {
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'clientid=3; did=web_384d9fefd2e64e2313aaa2790227e1df; client_key=65890b29; didv=1556291904430; Hm_lvt_86a27b7db2c5c0ae37fee4a8a35033ee=1556291905; Hm_lpvt_86a27b7db2c5c0ae37fee4a8a35033ee=1556291905; kuaishou.live.bfb1s=ac5f27b3b62895859c4c1622f49856a4; userId=211430228; userId=211430228; kuaishou.live.web_st=ChRrdWFpc2hvdS5saXZlLndlYi5zdBKgAYLys9tlwIX98I1XQpTUbcUaljgOlJCg6nYa_QNZxSkN4tm51HfqSvQYwJwtraFqGEXToU1YHMXnHUeBwFcHYI9jyapmG8rPbV9KdHGYVnxr1gxzieAfuVWDCRELLDgqOYE8NfxfnPifhELuM6BCV-SNZu1z74tIxMPhwODPkgMsAvMMX4CvJ9W7E8KWKVc10OoacoJfNkSdKosXxC44dBMaEtjNYCqMvUVZmp6WeyTUfct3aCIg9PmJNLhaJ1lD-AwB0ZA8ZxVzyrvqm-WNLrz6Mx6zeh4oBTAB; kuaishou.live.web_ph=378778f29e63780e10303b8f5760f796af67',
        'Host': 'live.kuaishou.com',
        'Referer': 'https://live.kuaishou.com/v/hot',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
    }
    wb_data = requests.get(url=url,headers=headers)
    et  = etree.HTML(wb_data.text)
    ks_id = ''.join(et.xpath('//*[@id="app"]/div/div[3]/div[1]/div[1]/div[2]/p[2]/span[1]/text()'))
    ks_id = re.sub('快手ID：|用户ID：','',ks_id)
    fans = parsingChar(type='qw2f1m1o',data=''.join(et.xpath('//*[@class="user-data-item fans"]/text()')))
    if 'w' in fans:
        fans = int(re.sub('[^\d]', '', fans)) * 10000
    like = parsingChar(type='qw2f1m1o',data=''.join(et.xpath('//*[@class="user-data-item follow"]/text()')))
    if 'w' in like:
        like = int(re.sub('[^\d]','',like))*10000
    works = parsingChar(type='qw2f1m1o',data=''.join(et.xpath('//*[@class="user-data-item work"]/text()')))
    if 'w' in works:
        works = int(re.sub('[^\d]','',works))*10000
    out_data = {
        'ks_id':ks_id,
        'fans':fans,
        'like_':like,
        'works':works,

    }
    print(out_data)
    my_insert(conn=conn, table_name='ks_user_info', data=out_data)

    # times = et.xpath('//*[@class="feed-list"]/li//div/div[2]/div/text()')
    # names = et.xpath('//*[@class="feed-list"]/li//div/div[2]/p[1]/text()')
    # play_counts = et.xpath('//*[@class="feed-list"]/li/div/div[2]/p[2]/span[1]/text()')
    # like_counts = et.xpath('//*[@class="feed-list"]/li/div/div[2]/p[2]/span[2]/text()')
    # comment_counts = et.xpath('//*[@class="feed-list"]/li/div/div[2]/p[2]/span[3]/text()')
    # for name,play_count,like_count,comment_count,time_ in zip(names,play_counts,like_counts,comment_counts,times):
    #     first_20_data = {
    #         'name':name.strip(),
    #         'play_count':parsingChar(type='qw2f1m1o',data=play_count.strip()),
    #         'like_count':parsingChar(type='qw2f1m1o',data=like_count.strip()),
    #         'comment_count':parsingChar(type='qw2f1m1o',data=comment_count.strip()),
    #         'time_':time_,
    #     }
    #     print(first_20_data)
    # print(out_data)
def get_user_vides(conn,data,pcursor):
    url = 'https://live.kuaishou.com/graphql'
    json_data = {
	"operationName": "publicFeedsQuery",
	"variables": {
		"principalId": data.get('id'),
		"pcursor": pcursor,
		"count": 24
	},
	"query": "query publicFeedsQuery($principalId: String, $pcursor: String, $count: Int) {\n  publicFeeds(principalId: $principalId, pcursor: $pcursor, count: $count) {\n    pcursor\n    live {\n      user {\n        id\n        kwaiId\n        eid\n        profile\n        name\n        living\n        __typename\n      }\n      watchingCount\n      src\n      title\n      gameId\n      gameName\n      categoryId\n      liveStreamId\n      playUrls {\n        quality\n        url\n        __typename\n      }\n      followed\n      type\n      living\n      redPack\n      liveGuess\n      anchorPointed\n      latestViewed\n      expTag\n      __typename\n    }\n    list {\n      photoId\n      caption\n      thumbnailUrl\n      poster\n      viewCount\n      likeCount\n      commentCount\n      timestamp\n      workType\n      type\n      useVideoPlayer\n      imgUrls\n      imgSizes\n      magicFace\n      musicName\n      location\n      liked\n      onlyFollowerCanComment\n      relativeHeight\n      width\n      height\n      user {\n        id\n        eid\n        name\n        profile\n        __typename\n      }\n      expTag\n      __typename\n    }\n    __typename\n  }\n}\n"
    }
    headers = {
        'Cookie': 'clientid=3; did=web_384d9fefd2e64e2313aaa2790227e1df; client_key=65890b29; didv=1556291904430; Hm_lvt_86a27b7db2c5c0ae37fee4a8a35033ee=1556291905; Hm_lpvt_86a27b7db2c5c0ae37fee4a8a35033ee=1556291905; kuaishou.live.bfb1s=ac5f27b3b62895859c4c1622f49856a4; userId=211430228; userId=211430228; kuaishou.live.web_st=ChRrdWFpc2hvdS5saXZlLndlYi5zdBKgARC97yIZwEZBhQhqs5IzILHcjlrZOhYCyMTAkCHsRRfunMTdzOtcmqgXyUJnF0_9HwpJ3aluYQVl7ttkpuEz-ZQn25GTZzQue6HvN9QQHQwcWnX4INVETbSd-7j5dgcjW63-CtfoMgCm5J2aDBKa_2ngMgf56s28KSpone6RzGXsLFu7OlalqUE-z0_XPSOX1aVYmaj2AYiSKYgvITS6hbEaEqtYXSf19kp4pfaTtPC7dufEBiIg6lv4IQZndMg5ijrGFvF81HRYnnE0OL3PKKCdkD8LFyMoBTAB; kuaishou.live.web_ph=fba53516d87d8a67878b4562b0b5c42ca1bf',
        'Host': 'live.kuaishou.com',
        'Origin': 'https://live.kuaishou.com',
        'Referer': 'https://live.kuaishou.com/profile/%s'%data.get('id'),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
    }
    wb_data=  requests.post(url=url,headers=headers,json=json_data,verify=False)
    # print(wb_data.text)
    wb_data.encoding ='utf-8'

    wb_data = json.loads(wb_data.text)
    for item in wb_data.get('data').get('publicFeeds').get('list'):
        # print(item)
        out_data = {
            'title':item.get('caption').strip().replace("\n",''),
            'play_count':item.get('viewCount'),
            'likeCount':item.get('likeCount'),
            'commentCount':item.get('commentCount'),
            # 'creat_time':(datetime.datetime.fromtimestamp(int(int()),
            'creat_time':datetime.datetime.fromtimestamp(int(int(item.get('timestamp'))/1000)).strftime('%Y-%m-%d %H:%M:%S'),
            'video_url':'https://live.kuaishou.com/u/'+data.get('id')+'/'+item.get('photoId')
        }
        print(out_data)
        my_insert(conn=conn,table_name='ks_user_video',data=out_data)
    pcursor = wb_data.get('data').get('publicFeeds').get('pcursor')
    print(pcursor)
    if pcursor !='no_more':
        print(pcursor)
        get_user_vides(conn=conn,data=data,pcursor=pcursor)
    else:
        pass
if __name__ == '__main__':
    conn = my_conn(host='127.0.0.1', user='root', passwd='zhang.123', port=3306, db='test')
    get_videos(conn=conn)
    my_close(conn=conn)