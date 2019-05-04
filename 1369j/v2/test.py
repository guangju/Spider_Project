import requests
from lxml import etree
all_list =[]
url = 'https://www.1396j.com/xyft/kaijiang'
wb_data = requests.get(url=url)
et = etree.HTML(wb_data.text)
for i, time_ in zip(et.xpath('//*[@id="history"]//tr/td[2]/div'), et.xpath('//*[@id="history"]//tr/td[1]')):
    count = 1
    out_data = {}
    for number in i.xpath('string()').strip().split():
        out_data['number%s' % count] = number
        count += 1
        # print(out_data)
    out_data['time_'] = time_.xpath('string()')
    all_list.append(out_data)
all_list.reverse()
all_list.append(0)
for old_data, new_data in zip(all_list,all_list[1:-1]):
    print(old_data, new_data)
