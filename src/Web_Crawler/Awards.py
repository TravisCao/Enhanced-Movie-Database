import logging
import random
import string
import requests
import time
from collections import deque
from urllib import parse
import pandas as pd
import re
from bs4 import *
from retrying import retry


User_Agents = [ "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
]
class DoubanSpider(object):
    """豆瓣爬虫"""
    def __init__(self,form,Type,country,genres):
        # 基本的URL
        self.base_url = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&'
        self.full_url = self.base_url + '{query_params}'
        # 从User-Agents中选择一个User-Agent
        
        # 代理服务器
        self.proxyHost = "dyn.horocn.com"
        self.proxyPort = "50000"

        # 代理隧道验证信息
        self.proxyUser = "BUGT1663533146089384"
        self.proxyPass = "tsDrlKYJH7wM"

        self.proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": self.proxyHost,
            "port": self.proxyPort,
            "user": self.proxyUser,
            "pass": self.proxyPass,
        }

        self.proxies = {
            "http": self.proxyMeta,
            "https": self.proxyMeta,
        }
        # 可选参数 
        self.form_tag = form  # 影视形式
        self.type_tag = Type  # 类型
        self.countries_tag =  country # 地区
        self.genres_tag = genres #特色
        #默认参数
        self.sort = 'T'  # 排序方式,默认是T,表示热度
        self.range = 0, 10  # 评分范围
    @retry(stop_max_attempt_number=5)
    def geturl(self,url):
        self.headers = {'User-Agent':random.choice(User_Agents)}
        resp=requests.get(url,headers=self.headers,proxies=self.proxies)
        return resp
    def encode_query_data(self):
        """对输入信息进行编码处理"""
        
        if not (self.form_tag and self.type_tag and self.countries_tag and self.genres_tag):
            all_tags = ''
        else:
            all_tags = [self.form_tag, self.type_tag, self.countries_tag, self.genres_tag]
        query_param = {
            'sort': self.sort,
            'range': self.range,
            'tags': all_tags,
        }

        # string.printable:表示ASCII字符就不用编码了
        query_params = parse.urlencode(query_param, safe=string.printable)
        # 去除查询参数中无效的字符
        invalid_chars = ['(', ')', '[', ']', '+', '\'']
        for char in invalid_chars:
            if char in query_params:
                query_params = query_params.replace(char, '')
        # 把查询参数和base_url组合起来形成完整的url
        self.full_url = self.full_url.format(query_params=query_params) + '&start={start}'
        '''
        query_params = 'tags='+str(self.form_tag)+','+str(self.type_tag)+','+str(self.countries_tag)+','+\
            str(self.genres_tag)
        self.full_url = self.full_url.format(query_params=query_params) + '&start={start}'
        '''
    def find_award(self,subject):
        url = "https://movie.douban.com/subject/{}/awards/".format(subject)
        count = 0
        while True:
            try:
                r = self.geturl(url)
            except Exception as e:
                count += 1
                if count >= 5:
                    return [["","",""]]
                continue

            content = r.content
            if r.status_code == requests.codes.ok:
                soup = BeautifulSoup(content, 'html.parser')  # html.parser
                awards = []
                for box in soup.findAll('div', attrs={'class': 'awards'}):
                    name = box.div.h2.a.get_text()
                    for ul in box.findAll('ul'):
                        award = []
                        award.append(name)
                        n = ul.findAll('li')
                        award.append(n[0].get_text())
                        p = ''
                        for a in n[1].findAll('a'):
                            p +='/'
                            p += a.get_text()
                        award.append(p)
                        awards.append(award)
                return awards
            else:
                count+=1
                if count >= 5:
                    return [["","",""]]
                continue
    def download_movies(self, offset):
        """下载电影信息
        :param offset: 控制一次请求的影视数量
        :return resp:请求得到的响应体"""
        full_url = self.full_url.format(start=offset)
        resp = None
        count = 0
        while not resp or resp.status_code != 200 or not dict(resp.json()).get('data') or len(str(dict(resp.json()).get('data'))) < 20:
            count += 1
            if count >=6:
                return None
            try:
                #方法1.USER_AGENT配置,仿造浏览器访问 headers
                #方法2.伪造Cookie，解封豆瓣IP ,cookies = jar
                #jar = requests.cookies.RequestsCookieJar()
                #jar.set('bid', 'ehjk9OLdwha', domain='.douban.com', path='/')
                #jar.set('11', '25678', domain='.douban.com', path='/')
                #方法3.使用代理IP proxies
                resp = self.geturl(full_url)
                
            except Exception as e:
                logging.error(e)
        return resp

    def get_movies(self, resp):
        """获取电影信息
        :param resp: 响应体
        :return movies:爬取到的电影信息"""
        if resp:
            if resp.status_code == 200:
                # 获取响应文件中的电影数据
                movies = dict(resp.json()).get('data')
                if movies:
                    # 获取到电影了,
                    return movies
                else:
                    # 响应结果中没有电影了!
                    # print('已超出范围!')
                    return None
            else:
                #关机
                import os
                os.system("poweroff")
        else:
            # 没有获取到电影信息
            return None

    def save_movies(self, movies):
        """把请求到的电影保存到csv文件中
        :param movies:提取到的电影信息
        """
        #判断爬取的网页是否为空
        if len(str(movies)) < 20 : 
            return False
        #分词
        words = re.findall(pattern=r'\d\.\d|\w+(?:[ ，\-：·！。\？\(\)]?\w*)*',string=str(movies))
        #提取信息，生成字典
        items = []
        title_flag = False
        subject_flag = False
        title = None
        ID = None
        for word in words:
            if word == 'title':
                title_flag = True
            elif word == 'subject':
                subject_flag = True
            elif title_flag:
                title_flag = False
                title = word
            elif subject_flag:
                subject_flag = False
                ID = word
                award = self.find_award(word)
                if award == None:
                    continue
                for i in award:
                    item = {'ID':'','电影':'','奖项':'','类别':'','人物':''}
                    item['ID'] = ID
                    item['电影'] = title
                    item['奖项'] = i[0]
                    item['类别'] = i[1]
                    item['人物'] = i[2]
                    items.append(item)
                
        #保存字典
        frame = pd.DataFrame.from_dict(items)
        frame.to_csv('../movie_award.csv',index=0,header=0,mode='a')  #不保留索引，不保留标题，追加写入
        return True


def main():
    """豆瓣电影爬虫程序入口"""
    form_tags = ['电影','电视剧','综艺','动画','纪录片','短片']
    Type_tags = ['剧情','喜剧','动作','爱情','科幻','悬疑','惊悚','恐怖','犯罪','同性','音乐','歌舞','传记','历史',\
    '战争','西部','奇幻','冒险','灾难','武侠','情色'] 
    country_tags = ['中国大陆','美国','香港','台湾','日本','韩国','英国','法国','德国','意大利','西班牙','印度',\
    '泰国','俄罗斯','伊朗','加拿大','澳大利亚','爱尔兰','瑞典','巴西','丹麦']
    genres_tags = ['经典','青春','文艺','搞笑','励志','魔幻','感人','女性','黑帮']
    a = [{'ID':'ID','电影':'电影','奖项':'奖项','类别':'类别','人物':'获奖人'}]
    frame = pd.DataFrame.from_dict(a)
    frame.to_csv('../movie_award.csv',index=0,header=0,mode='a')
    
    for form in form_tags:
        if form != '电影':
            continue
        for Type in Type_tags:
            for country in country_tags[1:8]:
                for genres in genres_tags:
                    print(form,Type,country,genres)
                    # 1. 初始化工作,设置请求头等
                    spider = DoubanSpider(form=form,Type=Type,country=country,genres=genres)
                    # 2. 对信息进行编码处理,组合成有效的URL组合成有效的URL
                    spider.encode_query_data()
                    
                    offset = 0
                    flag = True
                    while flag:
                        # 3. 下载影视信息
                        reps = spider.download_movies(offset)
                        # 4.提取下载的信息
                        movies = spider.get_movies(reps)
                        # 5. 保存数据到csv文件
                        flag = spider.save_movies(movies)
                        print(offset,flag)
                        offset += 20
                        # 控制访问速度(访问太快会被封IP)
if __name__ == '__main__':
    main()
