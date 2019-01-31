import requests
from lxml import etree
from tkinter import *

# print("\n","Powered by Dong dong Xu")
# print("\n","      更多代码均放在   -->Github : https://github.com/Tcloser")
# print("\n")
# print("写在前面：本程序用于实时爬取最新调剂信息，关键词可以根据所爬内容适当修改，1.0版本主要进行测试信息及界面优化。")
# print("\n")
# print("                                            调剂信息最新发表内容如下所示：")
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
            #print(" *----------------------------------------------------------------------------------------------------*")
            #print("      "+quetitle,queprof,"http://www.chinakaoyan.com/"+queurl)#打印出来
            #text1.delete(0.0, END)
            text1.insert('insert',quetitle,queprof,"     http://www.chinakaoyan.com/"+queurl+"\n"+"\n")
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
            #print(" *----------------------------------------------------------------------------------------------------*")
            #print("      " + quetime,quelist, queporf, queurl)  # 打印出来
            text1.insert('insert', quetime+str(quelist)+queporf+queurl +"\n"+"\n")
            #text1.insert(quetime,quelist, queporf, queurl)
        return question_list,question_porf, question_url  # 将问题名称与地址输出至list，url保存

    @staticmethod
    def seach_keyword_chinakaoyan(question_list, question_url):
        number = 0
        sum_number = 0
        for i in question_list:
            if re.findall(search_profession, i) == [search_profession]:#匹配相同字段，对应链接顺序
                #print(i,"---请点击：","http://www.chinakaoyan.com"+question_url[number])
                text2.insert('insert',i+"---请去往："+"http://www.chinakaoyan.com"+str(question_url[number]) + "\n"+"\n")
                sum_number +=1
            number = number + 1
        if sum_number == 0:
            text2.insert('insert',"目前最新发布中没有搜索到相关内容。"+"\n")

    @staticmethod
    def seach_keyword_muchong(question_list, question_url):
        number = 0
        sum_number = 0
        for i in question_list:
            if re.findall(search_profession, i) == [search_profession]:#匹配相同字段，对应链接顺序
                #print(i,"---请点击：",question_url[number])
                text2.insert('insert',i+"---请去往："+str(question_url[number])+ "\n"+"\n")
                sum_number +=1
            number = number + 1
        if sum_number == 0:
            text2.insert('insert',"目前最新发布中没有搜索到相关内容。"+"\n")

def run_main():
    #while 1:#定时60s查询
        text1.delete(0.0, END)
        text2.delete(0.0, END)
        global search_profession
        search_profession = entry1.get()#获取输入专业
        muchong_index = 1
        (title_chinakaoyan,prof_chinakaoyan, url_chinakaoyan) = spider.start_request_chinakaoyan(web_site_chinakaoyan)# 查询 chinakaoyan.com一页
        #print("\n","小木虫网站信息如下：                      ","\n")
        while 1: #小木虫三页
            if muchong_index != 4:
                web_site_muchong = 'http://muchong.com/bbs/kaoyan.php?action=adjust&type=1&page=' + str(muchong_index)
                (list_muchong, porf_muchong,url_muchong) = spider.start_request_muchong(web_site_muchong)  # 查询 muchong
                muchong_index = muchong_index + 1
            else :
                break
        #print("\n")
        # muchong_index = 1  # 小木虫页面复位
        spider.seach_keyword_chinakaoyan(prof_chinakaoyan, url_chinakaoyan)#对chinakaoyan专业进行关键字查询
        spider.seach_keyword_chinakaoyan(title_chinakaoyan, url_chinakaoyan)#对chinakaoyan学校
        #print("\n")
        spider.seach_keyword_muchong(porf_muchong, url_muchong)#对小木虫学校专业信息进行关键字匹配
        spider.seach_keyword_muchong(list_muchong, url_muchong)#对小木虫学校信息进行关键字匹配
        #print("                                   ","1分钟后将对最新信息进行检索")

        #time.sleep(15)

spider = Spider()
#GUI
master = Tk()
master.title('考研调剂信息查询1.0   Powered by Dong dong Xu')
master.geometry('1200x650+100+50')#显示框大小与坐标
master.resizable(0, 0)
#标签
label1 = Label(master, text='请输入专业或学校简称：', font=('GB2312', 14))
label1.grid(row=0, column=0, sticky=E)#.grid将内容展示出来
label2 = Label(master, text='Github : https://github.com/Tcloser', font=('GB2312', 14))
label2.grid(row=2, column=1)#.grid将内容展示出来
#输入专业内容框1
entry1 = Entry(master, font=('GB2312', 14), width=30)
entry1.grid(row=0, column=1)
#搜索内容显示框
res = StringVar()
#搜索按钮
button1 = Button(master, text='搜索', font=('GB2312', 14), width=14, command=run_main)#******执行循环
button1.grid(row=0, column=2)
#退出按钮
button2 = Button(master, text='退出', font=('GB2312', 14), width=14, command=master.quit)
button2.grid(row=2, column=2)
#文本显示
text1 = Text(master, font=('GB2312', 12), width=150, height=25)
text1.grid(columnspan=3)
text2 = Text(master, font=('GB2312', 12), width=150, height=10, fg ="red")
text2.grid(columnspan=3)
#显示框
master.mainloop()








