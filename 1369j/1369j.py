import requests
from lxml import etree
url = 'https://www.1396j.com/xyft/kaijiang'
wb_data = requests.get(url=url)
et = etree.HTML(wb_data.text)
all_list = []

# for i,time_ in zip(et.xpath('//*[@id="history"]//tr/td[2]/div'),et.xpath('//*[@id="history"]//tr/td[1]')):
#     print(i.xpath('string()').strip().split(),time_.xpath('string()'))
#
count = 0

# for v in range(0,1):
#     for i,i1 in zip(range(len(all_list)-1,0,-1),range(len(all_list)-2,-1,-1)):
#         if count>=5:
#             print('报警%s'%count,all_list[i],all_list[i1])
#         print(all_list[i],all_list[i1])
#         if all_list[i][v] not in all_list[i1][0:5]:
#             print('匹配不到+1')
#             count+=1
#         else:
#             count=0
