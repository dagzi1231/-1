import socket
import pinyin
import string
import sys
import threading
import time
import logging
import difflib
import sys
import csv
from tkinter import filedialog
import getopt
import argparse
import requests
import parsel
import json
import pandas as pd
import tkinter
import sqlite3
import tkinter.messagebox 

#多开一个线程作为后台进行数据更新
def update_data():
    search(update_city)
    save(update_city)
    pass
def start_update_thread():
    def update_data_with_timer():
        while True:
            update_data()
            time.sleep(7 * 24 * 60 * 60) # 每 7 天运行一次 update_data 函数

    update_thread = threading.Thread(target=update_data_with_timer, args=())
    update_thread.daemon = True
    update_thread.start()


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
    # init_db(dbpath)                  #初始化数据库
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
    sql = "select * from houseinfotable"
    datas = cur.execute(sql)
    # print(type(datas))
    # for data in datas:
    #     print(data[1])
    cur.close()
    con.close()

def getnum(dbpath):
    hisdict={}
    con = sqlite3.connect(dbpath)
    cur = con.cursor()
    sql = "select * from houseinfotable"
    datas = cur.execute(sql)
    print(type(datas))
    for data in datas:
        if data[1] not in hisdict:
            hisdict[data[1]]=1
        elif data[1] in hisdict:
            hisdict[data[1]]+=1
    cur.close()
    con.close()
    return hisdict

def save(city):
    global savemethod
    global ds
    global datas
    df = datas
    try:
        if savemethod==1:
            saveDataDB(ds,"hous.db")
            print('保存成功')
            # # print([self.ress,self.titles,self.addresses,self.totalprices,self.unitprices,self.introduces])
            output("hous.db")
        else :
            print('保存到数据库成功，可在当前目录查看')
            savefile = 'house'#filedialog.asksaveasfilename(filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*") ))
            df.to_excel(savefile + ".xlsx", index=False, sheet_name="Results")
            logging.info('保存数据成功')
    except Exception as e:
        tkinter.messagebox.showerror(title = '错误信息',message = str(e))
def getsqlitsource():
    con = sqlite3.connect("hous.db")
    cur = con.cursor()
    cnt=0
    sql = "select * from houseinfotable"
    datas = cur.execute(sql)
    
    for data in datas:
        cnt+=0
        senddata=[]
        for datax in data:
            senddata.append(datax)
        # print(senddata)
        strdata=json.dumps(senddata).encode()
        conn.send(strdata)
        time.sleep(0.2)

def search(city):
    global cnt
    global ds
    if city:
        res=fuzzy_matching(data1,city)
        if res!=-1:
            titles = []
            addresses = []
            introduces = []
            totalprices = []
            unitprices = []
            ress = []
            flagofs=0
            for page in range(1,50):
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
                    if cnt>maxnumbers:
                        datas.columns=['city','title','address','price','price_pre_squ','houseInfo']
                        logging.info('爬取信息成功')
                        if iftest==0:
                            conn.send(json.dumps('F1,H0').encode())
                            if flagofs==0:
                                conn.send(json.dumps('F1,H1').encode())
                        return datas
                    title = li.css('.title a::text').get()
                    id=str(cnt)
                    address = '-'.join(li.css('.positionInfo a::text').getall())
                    introduce = li.css('.houseInfo::text').get()
                    
                    totalprice = li.css('.priceInfo .totalPrice span::text').get()+'万'
                    unitprict = li.css('.unitPrice span::text').get()
                    Data=[id,res,title,address,totalprice,unitprict,introduce]
                    titles.append(title)
                    addresses.append(address)
                    introduces.append(introduce)
                    totalprices.append(totalprice)
                    unitprices.append(unitprict)
                    ress.append(res)
                    flagofs=1
                    ds.append([])
                    ds[cnt].append(res)
                    ds[cnt].append(title)
                    ds[cnt].append(address)
                    ds[cnt].append(totalprice)
                    ds[cnt].append(unitprict)
                    ds[cnt].append(introduce)
                    cnt+=1
                    datas=pd.DataFrame([ress,titles,addresses,totalprices,unitprices,introduces]).T
            # datas.columns=['city','title','address','price','price_pre_squ','houseInfo']
            # logging.info('爬取信息成功')
            # return datas  
        else:
            tkinter.messagebox.showerror('错误',"没有找到相应的城市！可重新启动程序在初始化菜单选择4进行补充！")
    else :
        tkinter.messagebox.showinfo(title = '错误信息',message = '请输入内容')
      
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

#测试必要的变量
flagofsearch=0   #是否开启模糊匹配标志位 默认关
file_name="C:\\Users\\guoxiaoke\\Desktop\\NEU\\计算机课程\\python\\test\\new\\城市数据.txt"
f = open(file_name,encoding='utf-8')
cnt=0   #计数获取数据条数
maxnumbers=60
data1=f.read()
ds = []
savemethod=1
datas= []
iftest = 1    #若为1则在测试中
if __name__ == '__main__':
    update_city='沈阳'
    start_update_thread()  #即后台程序开启每一周更新一次数据 默认更新城市沈阳
    iftest = 0     #是否处在测试的flag
    filename123="./logging.txt"
    city=''
    server = socket.socket()
    server.bind(('localhost',40000))
    print("waiting for clinet...")
    server.listen()
    conn, addr = server.accept()
    print(addr)
    while True:
        bdata=conn.recv(1024)
        try:
            data = json.loads(bdata)
        except:    #检测到客户端关闭后自动退出
            break
        if(type(data)==type([])):
            print(data[0])
        if(type(data)==type('str')):
            if data[0]=='S':     #相当于信息发送的包头 之前接触过单片机 串口通讯时一般设置包头包尾来检验信息 甚至为了防止信息传输错误还会有一些CRC检验之类的检验
                city=data[1:]
                search(city)
                save(city)

            elif data[0]=='D':
                break
            elif data[0]=='P':
                savemethod=int(data[1])
            elif data[0]=='G':
                tmpdic = getnum('hous.db')
                conn.send(json.dumps(tmpdic).encode())
            elif data[0]=='A':
                maxnumbers=int(data[1:])
            elif data[0]=='C':
                save(city)
            elif data[0]=='H':
                getsqlitsource()
                print('hi')
                conn.send(json.dumps('T').encode())
            elif data[0]=='O':
                init_db('hous.db')
            elif data[0]=='F':
                update_city=data[1:]
                if(fuzzy_matching(data1,update_city)==-1):
                    conn.send(json.dumps('P').encode())
                else:
                    conn.send(json.dumps('O').encode())


    server.close()
