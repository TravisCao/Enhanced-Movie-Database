



import requests
from bs4 import BeautifulSoup
import json
import re
import codecs
import time
import random

headers = {
    'Cookie':'xxxxxxxx',
    'Host':'movie.douban.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
}

import requests
import time
import threading
import urllib3

# =================================================================================================

class CrawlThread(threading.Thread):
    def __init__(self,proxyip):
        super(CrawlThread, self).__init__()
        self.proxyip=proxyip

    def run(self):
        global count
        global lines
        start = time.time()
        #close warning 
        urllib3.disable_warnings()

        end = time.time()
        index = random.randint(2,434681) 
        while(end-start <= 20):
            while(    ('{}\n'.format(index) in lines)   or    ('{}'.format(index) in lines)    ):
                index = random.randint(2,434681)  
            with open('/Users/hm_cai/Desktop/CSC3170爬虫/celebrity_record.txt','a') as record:
                record.write('{}\n'.format(index))
                lines.append('{}\n'.format(index))

            current_url = 'https://movie.douban.com/celebrity/{}/'.format(1000000+index) 
            self.write_content(current_url, index)
            count += 1
            print(count, index)
            

            time.sleep(0.1)
            end = time.time()

    def get_html(self,url):
        print(url)
        try:
            r = requests.get(url, proxies={"http" : 'http://' + self.proxyip, "https" : 'https://' + self.proxyip}, verify=False, timeout=15, headers=headers)
        except Exception as e :
            print("fail request the website：%s" % e)
            return
        return r.text #return text


    def write_content(self, url, file_index):
        html = self.get_html(url)
        soup = BeautifulSoup(html,'lxml')
        html_award = self.get_html(url+'awards/')
        soup_award = BeautifulSoup(html_award,'lxml')

        actor_Chi_Eng_name = soup.find('h1')
        if actor_Chi_Eng_name is None:
            actor_Chi_Eng_name = 'Null'

        actor_info = soup.find('div',attrs={'class':'info'})
        if actor_info is None:
            actor_info = 'Null'

        best_five = soup.find('ul', attrs= {'class':'list-s'})
        if best_five is None:
            best_five = 'Null'

        awards = soup_award.find('div',attrs={'class':'article'})
        if awards is None:
            awards = 'Null'

        try:
            with open('//Users/hm_cai/Desktop/CSC3170爬虫/celebrity/dataset/{}.txt'.format(file_index), 'a') as f:
                f.write('姓名:{}\n'.format(actor_Chi_Eng_name.get_text()))
                f.write(actor_info.get_text().lstrip().rstrip())
                f.write('\n')
                f.write(best_five.get_text().lstrip().rstrip())
                f.write('\n\n\n\nAwards:\n')
                f.write(awards.get_text().lstrip().rstrip())
        except:
            pass




# lerage every obtained ip
class GetIpThread(threading.Thread):
    def __init__(self,fetchSecond):
        super(GetIpThread, self).__init__()
        self.fetchSecond=fetchSecond
    def run(self):
        global ips
        while True:
            res = requests.get(apiUrl).content.decode()
            ips = res.split('\n')
            print(len(ips))
            for proxyip in ips:
                if proxyip.strip():
                    CrawlThread(proxyip).start()
            print('====================== waiting ==========================')
            time.sleep(self.fetchSecond)



if __name__ == '__main__':
    
    init_url = 'https://movie.douban.com/celebrity/'
    with open('/Users/hm_cai/Desktop/CSC3170爬虫/celebrity_record.txt','r') as record_cele:
        lines = record_cele.readlines()
    print(lines)


    order = "8dd1370a60c54c2aa7ea7b6ee59e918b"
    apiUrl = "http://dynamic.goubanjia.com/dynamic/get/" + order + ".html"
    fetchSecond = 4
    GetIpThread(fetchSecond).start()













