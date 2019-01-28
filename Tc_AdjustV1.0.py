import requests
import re
import time
from lxml import etree
search_profession = input("你要查找的专业或学校是：")
print("\n","Powered by Dong dong Xu")
print("\n","      更多代码均放在   -->Github : https://github.com/Tcloser")
print("\n")
print("写在前面：本程序用于实时爬取最新调剂信息，关键词可以根据所爬内容适当修改，1.0版本主要进行测试信息及界面优化。")
print("\n")
print("                                            调剂信息最新发表内容如下所示：")
# 中国考研网 http://www.chinakaoyan.com/tiaoji/schoollist/pagenum/1.shtml
chinakaoyan_index = 1
web_site_chinakaoyan   = 'http://www.chinakaoyan.com/tiaoji/schoollist/pagenum/'+str(chinakaoyan_index)+'.shtml'  #网址第一页 可用循环多次
school_sign_chinakaoyan = '<span class="school">(.*?)</span>'                             #标题特征
profession_sign_chinakaoyan = '<span class="name">(.*?)</span>'                          #专业特征
title_sign_chinakaoyan = 'target="_blank">(.*?)</a></span>'                               #发表标题
url_sign_chinakaoyan   = '<span class="title"><a href="(.*?)" ti'                        #链接特征

# 小木虫 http://muchong.com/bbs/kaoyan.php?&page=1
muchong_index = 1
title_sign_muchong = 'class="xmc_ft12">(.*?)</a>'                                        #标题特征
profession_sign_muchong = '//tbody[@class="forum_body_manage"]/tr/td[last()-2]/text()'   #xpath专业特征
url_sign_muchong   = 'lp20"><a href="(.*?)" tar'                                         #链接特征
time_sign_muchong =  '//tbody[@class="forum_body_manage"]/tr/td[last()]/text()'

class Spider(object):
    @staticmethod
    def start_request_chinakaoyan (websit1) :
        response = requests.get(websit1)
        res = response.text  # 将信息从前端代码拿出
        # 正则表达式
        question_school = re.findall(school_sign_chinakaoyan, res) #标题特征
        question_prof = re.findall(profession_sign_chinakaoyan, res)#专业特征
        question_url  = re.findall(url_sign_chinakaoyan, res)   #链接特征
        question_title = re.findall(title_sign_chinakaoyan, res)  # 标题特征
        del (question_school[0]) #chinakaoyan.com第一个信息删除
        del (question_prof[0])
        for quetitle, queprof, queurl  in zip(question_title, question_prof,question_url):  #列表显示标题与部分地址
            print(" *----------------------------------------------------------------------------------------------------*")
            print("      "+quetitle,queprof,"http://www.chinakaoyan.com/"+queurl)#打印出来
        return question_title,question_prof,question_url  #将问题名称与地址输出至list，url保存

    @staticmethod
    def start_request_muchong(websit2):
        response = requests.get(websit2)
        res = response.text  # 将信息从前端代码拿出
        html = etree.HTML(response.text)  # 将信息从前端代码拿出
        # 正则表达式
        question_list = re.findall(title_sign_muchong, res)  # 标题特征
        question_porf = html.xpath(profession_sign_muchong)  # 111111
        question_time = html.xpath(time_sign_muchong)
        question_url = re.findall(url_sign_muchong, res)  # 链接特征
        for quetime,quelist, queporf, queurl in zip(question_time,question_list, question_porf, question_url):  # 列表显示标题与部分地址
            print(
                " *----------------------------------------------------------------------------------------------------*")
            print("      " + quetime,quelist, queporf, queurl)  # 打印出来
        return question_list,question_porf, question_url  # 将问题名称与地址输出至list，url保存

    @staticmethod
    def seach_keyword_chinakaoyan(question_list, question_url):
        number = 0
        sum_number = 0
        for i in question_list:
            if re.findall(search_profession, i) == [search_profession]:#匹配相同字段，对应链接顺序
                print(i,"---请点击：","http://www.chinakaoyan.com"+question_url[number])
                sum_number +=1
            number = number + 1
        if sum_number == 0:
            print("                      目前最新发布中没有搜索到相关内容。")

    @staticmethod
    def seach_keyword_muchong(question_list, question_url):
        number = 0
        sum_number = 0
        for i in question_list:
            if re.findall(search_profession, i) == [search_profession]:#匹配相同字段，对应链接顺序
                print(i,"---请点击：",question_url[number])
                sum_number +=1
            number = number + 1
        if sum_number == 0:
            print("                      目前最新发布中没有搜索到相关内容。")

spider = Spider()
while 1:#定时60s查询
    (title_chinakaoyan,prof_chinakaoyan, url_chinakaoyan) = spider.start_request_chinakaoyan(web_site_chinakaoyan)# 查询 chinakaoyan.com一页
    #print('                                                      第', str(chinakaoyan_index),'页内容')
    print("\n","小木虫网站信息如下：                      ","\n")
    # spider.seach_keyword(list,url)
    while 1: #小木虫三页
        if muchong_index != 4:
            web_site_muchong = 'http://muchong.com/bbs/kaoyan.php?action=adjust&type=1&page=' + str(muchong_index)
            (list_muchong, porf_muchong,url_muchong) = spider.start_request_muchong(web_site_muchong)  # 查询 muchong
            muchong_index = muchong_index + 1
        else :
            break
    print("\n")
    spider.seach_keyword_chinakaoyan(prof_chinakaoyan, url_chinakaoyan)#对chinakaoyan专业进行关键字查询
    spider.seach_keyword_chinakaoyan(title_chinakaoyan, url_chinakaoyan)#对chinakaoyan学校
    print("\n")
    spider.seach_keyword_muchong(porf_muchong, url_muchong)#对小木虫学校专业信息进行关键字匹配
    spider.seach_keyword_muchong(list_muchong, url_muchong)#对小木虫学校信息进行关键字匹配
    print("                                   ","1分钟后将对最新信息进行检索")
    muchong_index = 1#小木虫页面复位
    time.sleep(60)







