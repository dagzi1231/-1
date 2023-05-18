import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import pinyin
import pandas as pd
import time
import logging
import difflib
import random
import sys
from ttkbootstrap import Style
import csv
import getopt
import argparse
import requests
import sqlite3
import parsel
from lxml import etree
from tkinter import filedialog

def fuzzy_matching(texts, value):
    texts = texts.split(",")
    texts_score = {}
    logging.info("展开模糊搜索成功！\n")
    for i in texts:
        score = difflib.SequenceMatcher(None, i, value).quick_ratio()
        texts_score[i] = score
    texts_score = sorted(texts_score.items(), key=lambda x: x[1], reverse=False)
    logging.info("获取搜索匹配数据成功，且对数据进行排序！\n")
    po=1
    tmp12=0
    if flagofsearch==1 :
        b=[x[1] for x in texts_score]
        for i in range(100):
            if(b[-i]>0):
                print(i,end=':')
                print(texts_score[-i])
                tmp12=1
        logging.info("成功输出获取数据供给用户选择！(开启了模糊匹配选项)\n")
        if(tmp12==1):
            po=int(input("选择你所想输入的城市名称（1-N）:"))
            match_value = texts_score[-po][0]
            return match_value
        else:
            return -1    
    else :
        # print('\n*****************',texts_score[-1][1],'*****************\n')
        if texts_score[-1][1]==1 :
            return texts_score[-1][0]
        else :
            return -1

def get_pinyin_first_alpha(name):
    return "".join([i[0] for i in pinyin.get(name, " ").split(" ")])


class House:
    def __init__(self,master):
        self.columns={
        'ID':25,
        '城市':40,
        '广告标题':350,
        '地址':200,
        '总价格':50,
        '每平方的价格':100,
        '主要信息':450
        }
        self.tree=ttk.Treeview(master,height=18,show='headings')
        self.tree['columns'] = list(self.columns)
        for column in self.columns:  # 批量设置列属性
            self.tree.heading(column, text=column)  # #设置列标题
            self.tree.column(column, width=self.columns[column], anchor='center')  
        
        self.maxpage=50 #最大搜索页数 一页一般有三十个数据 这里默认最多50页 gui无法更改
        self.maxnumbers=30 #最大搜索数据条数 一般设置30
        
        self.savecheckbt=tk.Checkbutton(master,text='存储数据到excle文件',command=self.funchooseexcle)
        self.savecheckbt2=tk.Checkbutton(master,text='存储数据到数据库',command=self.funchoosedatab)
        self.savecheckbt.select()
        self.savemethod=1  #保存方式 有excle和database两种

        self.savecheckbt.grid(row=3,column=4)
        self.savecheckbt2.grid(row=3,column=4,sticky='e')
        self.progressbar=ttk.Progressbar(master,length=600)
        self.progressbar.grid(row=3,column=1,columnspan=5,pady=10,sticky='w')
        self.l2=tk.Label(master,text='搜索进度:',font=('微软雅黑',12))
        self.l2.grid(row=3,column=0)

        self.l3=tk.Label(master,text='加载进度:',font=('微软雅黑',12))
        self.l3.grid(row=2,column=0)

        self.progressbar2=ttk.Progressbar(master,length=200)
        self.progressbar2.grid(row=2,column=1,columnspan=2,pady=1)
        self.progressbar2['maximum']=self.maxnumbers

        self.progressbar['maximum']=100
        # self.canvas=tk.Canvas(master,width=600,height=15,bg='black')
        # self.canvas.grid(row=3,column=0,columnspan=3,pady=10)
        self.titles = []
        self.addresses = []
        self.introduces = []
        self.totalprices = []
        self.unitprices = []
        self.ress = []

        self.ds=[]

        self.tree.grid(row=1,column=0,columnspan=6) 
       
        
        self.b1 = tk.Label(master,text='请输入省会城市的名称:',font=('微软雅黑',12))
        self.b1.grid(row=0,column=3)

        self.e =tk.Entry(master,show=None,width=100)
        self.e.grid(row=0,column=4) 

        v=tk.StringVar(value='30')
        self.e2 =tk.Entry(master,show=None,width=10,textvariable=v)
        self.e2.grid(row=0,column=1,sticky='w')

        self.bt3=tk.Button(text='设置最大搜索数量:',command=self.setmaxnumbers)
        self.bt3.grid(row=0,column=0,sticky='e')


        # self.bt1=tk.Button(master,text='搜索',width=8,height=1,command=lambda:[self.progress(),self.search()])
        self.bt1=tk.Button(master,text='查询',width=8,height=1,command=lambda:[self.showprogress(),self.search()])

        self.bt1.grid(row=0,column=5)  
        self.btnDelete1=tkinter.Button(master,text='删除所选数据',font=('微软雅黑',12),command=self.deleteclick,width=10,height=1)
        self.btnDelete1.grid(row=2,column=3)  #
        self.btnDelete2=tkinter.Button(master,text='删除所有数据',font=('微软雅黑',12),command=self.deletealldata,width=10,height=1)
        self.btnDelete2.grid(row=2,column=4)
        self.button4 = tk.Button(master,text='保存所有数据',font=('微软雅黑',12),command=self.save,width=10,height=1)
        self.button4.grid(row=2,column=5)
    def setmaxnumbers(self):
        self.maxnumbers=int(self.e2.get())
        tkinter.messagebox.showinfo('提示','最大搜索数据数量设置成功')
        print('ok')
    
    def funchooseexcle(self):
        self.savemethod=1
        self.savecheckbt.select()
        self.savecheckbt2.deselect()
    def funchoosedatab(self):
        self.savemethod=0
        self.savecheckbt.deselect()
        self.savecheckbt2.select()


    def deleteclick(self):
        if not self.tree.selection():
            tkinter.messagebox.showerror('抱歉','你还没有选择，无法删除数据')
            return
        for item in self.tree.selection():
            self.tree.delete(item)

    def showprogress(self):
        for i in range(100):
            self.progressbar['value']=i+1
            window.update()
            time.sleep(0.005)
    

    def deletealldata(self):
        global cnt
        def delButton(tree):
            x=tree.get_children()
            for item in x:
                # print(item)
                tree.delete(item)
            logging.info('删除所有数据成功')
        delButton(self.tree)
        self.titles = []
        self.addresses = []
        self.introduces = []
        self.totalprices = []
        self.unitprices = []
        self.ress = []
        self.ds=[[]]
        cnt=0
    

    def search(self):
        global city
        global cnt
        self.progressbar2['maximum']=self.maxnumbers
        self.progressbar['value']=0
        flag1=0
        city =self.e.get()
        if city:

            
            res=fuzzy_matching(data1,city)
            if res!=-1:
                for page in range(1,100):
                    global datas
                    logging.info("模糊匹配完成！")
                    resultcity=get_pinyin_first_alpha(res)
                    logging.info("汉字拼音首字母获取成功！")
                    url='https://'+resultcity+f'.lianjia.com/ershoufang/pg{page}/'
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.42'}
                    reponse = requests.get(url=url,headers=headers)
                    html_data = reponse.text
                    #print(html_data)
                    selector = parsel.Selector(html_data)
                    lis = selector.css('.clear.LOGCLICKDATA')
                    #print(lis)
                    for li in lis:
                        if cnt > self.maxnumbers:
                            if flag1==0:
                                tkinter.messagebox.showinfo("提示",'已达到最大搜索数据上限，请在左上角进行添加以便搜索更多数据\n设置完成记得点击按钮确认')

                            datas.columns=['city','title','address','price','price_pre_squ','houseInfo']
                            logging.info('爬取信息成功')
                            return datas

                        title = li.css('.title a::text').get()
                        
                        self.progressbar2['value']=cnt
                        id=str(cnt)
                        address = '-'.join(li.css('.positionInfo a::text').getall())
                        introduce = li.css('.houseInfo::text').get()
                        totalprice = li.css('.priceInfo .totalPrice span::text').get()+'万'
                        unitprict = li.css('.unitPrice span::text').get()
                        Data=[id,res,title,address,totalprice,unitprict,introduce]
                        self.titles.append(title)
                        self.addresses.append(address)
                        self.introduces.append(introduce)
                        self.totalprices.append(totalprice)
                        self.unitprices.append(unitprict)
                        self.ress.append(res)
                        
                        self.ds.append([])
                        self.ds[cnt].append(res)
                        self.ds[cnt].append(title)
                        self.ds[cnt].append(address)
                        self.ds[cnt].append(totalprice)
                        self.ds[cnt].append(unitprict)
                        self.ds[cnt].append(introduce)
                        flag1=1
                        cnt+=1
                        
                        datas=pd.DataFrame([self.ress,self.titles,self.addresses,self.totalprices,self.unitprices,self.introduces]).T
                        self.tree.insert('', cnt,text='', values=Data)
                        if cnt%random.randrange(1,10)==0:
                            window.update()
                # datas.columns=['city','title','address','price','price_pre_squ','houseInfo']
                # logging.info('爬取信息成功')
                # return datas 
            else:
                tkinter.messagebox.showerror('输入错误',"没有找到相应的城市！可重新启动程序在初始化菜单选择4进行补充！")
        else :
            tkinter.messagebox.showinfo('错误信息','请输入内容')
    def save(self):
        self.df = pd.DataFrame([self.ress,self.titles,self.addresses,self.totalprices,self.unitprices,self.introduces]).T
        try:
            if self.savemethod==0:
                saveDataDB(self.ds,"house.db")
                tkinter.messagebox.showinfo('提示','保存数据成功\n可在py文件当前目录进行查看')
                # print([self.ress,self.titles,self.addresses,self.totalprices,self.unitprices,self.introduces])
                # output("house.db")
            else :
                savefile = filedialog.asksaveasfilename(filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*") ))
                self.df.to_excel(savefile + ".xlsx", index=False, sheet_name="Results")
                logging.info('保存数据成功')
        except Exception as e:
            print(self.ds)
            tkinter.messagebox.showerror(title = '错误信息',message = str(e))


def init_db(dbpath):
    initsql = "drop table if exists houseinfotable" 

    createsql = '''
        create table if not exists houseinfotable
        (
            id integer primary key autoincrement ,
            city varchar ,
            title varchar ,
            address varchar ,
            price varchar ,
            price_pre_squ varchar,
            houseInfo varchar
        )
    '''                          

    conn = sqlite3.connect(dbpath)   #打开或创建 连接数据库文件
    cursor = conn.cursor()           #获取游标
    cursor.execute(initsql)          # 执行SQL语句
    cursor.execute(createsql)        #执行SQL语句
    conn.commit()                    #提交数据库操作
    conn.close()

def saveDataDB(datalist,dbpath):
    init_db(dbpath)                  #初始化数据库
    conn = sqlite3.connect(dbpath)   #连接数据库文件
    cur = conn.cursor()              #获取游标

    for data in datalist:
        cur.execute("insert into houseinfotable(city,title,address,price,price_pre_squ,houseInfo)values(?, ?, ?, ?, ?, ?)",( data[0], data[1], data[2], data[3] ,data[4], data[5]))     #执行SQL语句

    conn.commit()      #提交数据库操作
    cur.close()
    conn.close()       #关闭数据库连接

def output(dbpath):
    con = sqlite3.connect(dbpath)
    cur = con.cursor()
    sql = "select * from studentTable"
    datas = cur.execute(sql)
    for data in datas:
        print(data)
    cur.close()
    con.close()





flagofsearch=0  #两个flag
file_name="./城市数据.txt"
filename123="./logging.txt"
logging.basicConfig(filename=filename123,level=logging.INFO,format="%(asctime)s-%(levelname)s:%(message)s")
print("****************************初始化菜单****************************")
print("1:重新输入城市数据文件路径")
print("2:取消模糊匹配支持（输入城市名称后仅输出认为最大匹配度的城市）")
print("3:启用模糊匹配")
print("4：追加补充城市名称")
print("5：退出菜单")
print("*****************************************************************")
tmpp=tmpp=int(input("输入1-5选择所要执行的"))
while tmpp!=4 :
    if(tmpp==1):
        file_name=input("请输入新的文件路径")
        logging.info("重新选取了数据文件路径")
    elif(tmpp==2):
        flagofsearch=0
        logging.info("取消了模糊匹配")
        print("模糊匹配已取消")
    elif(tmpp==3):
        flagofsearch=0
        logging.info("开启了模糊匹配")
        print("模糊匹配已开启")
    elif(tmpp==4)  :
        cityname=input("请输入城市名称:")
        f1= open(file_name,'a',encoding='utf-8')
        f1.write(','+cityname)
        f1.close()
    elif(tmpp==5):
        logging.info("初始化结束！")
        print("初始化结束！")
        break
    else :
        print("输入错误！请重新输入！")
    tmpp=int(input("输入1-5选择所要执行的"))

f = open(file_name,encoding='utf-8')
data1=f.read()

t = 20
print("*******************************加载城市数据*******************************")
start = time.perf_counter()
for i in range(t + 1):
    finsh = "▓" * i
    need_do = "-" * (t - i)
    progress = (i / t) * 100
    dur = time.perf_counter() - start
    print("\r{:^3.0f}%[{}->{}]{:.2f}s".format(progress, finsh, need_do, dur), end="")
    time.sleep(0.05)
logging.info("进度条加载完毕！")

window=tk.Tk()
# style = Style(theme='pulse')
# window=style.master
city=''
cnt=0

window.title('省会二手房信息搜索')
window.geometry('1305x530')

window.tk.call("source", "azure.tcl")
window.tk.call("set_theme", "light")

window.maxsize(1320,535)
window.minsize(1305,530)
a=House(window)
window.mainloop()


