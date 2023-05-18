import socket
import json
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import pinyin
import string
import sys
import time
import logging
import sys
import csv
import getopt
import matplotlib
import argparse
import requests
import parsel
import random
import matplotlib
from PIL import Image
from PIL import ImageTk
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"]=["SimHei"] #设置字体
plt.rcParams["axes.unicode_minus"]=False #该语句解决图像中的“-”负号的乱码问题

class window:
    def __init__(self):
        self.win = tk.Tk()
        self.win.title('省会二手房信息搜索')
        self.win.geometry('1255x580')
        self.maxnumbers=60   #最大搜索数量
        self.max=20   #最大接受数据量
        self.cnt=0
        self.citydict={}
        self.win.tk.call("source", "azure.tcl") #美化界面
        self.win.tk.call("set_theme", "light")
        self.searchflag=0

        self.tree=ttk.Treeview(self.win,height=18,show='headings')
        columns={
            'ID':15,
            'city':40,
            'title':350,
            'address':200,
            'price':40,
            'price_pre_squ':100,
            'houseInfo':450
            }
        self.tree['columns'] = list(columns)
        for column in columns:  # 批量设置列属性
            self.tree.heading(column, text=column)  # #设置列标题
            self.tree.column(column, width=columns[column], anchor='center')  
        self.tree.grid(row=1,column=0,columnspan=6) 
        #  存储方式选择
        self.savecheckbt=tk.Checkbutton(self.win,text='存储数据到excle文件',command=self.funchooseexcle)
        self.savecheckbt2=tk.Checkbutton(self.win,text='存储数据到数据库',command=self.funchoosedatab)
        self.savecheckbt.select()
        self.savemethod=1  #保存方式 有excle和database两种
        self.savecheckbt.grid(row=3,column=4)
        self.savecheckbt2.grid(row=3,column=4,sticky='e')
        self.button4 = tk.Button(self.win,text='保存所有数据',font=('微软雅黑',12),command=self.save,width=10,height=1)
        self.button4.grid(row=2,column=5)
        #
        #  进度条
        self.progressbar=ttk.Progressbar(self.win,length=600)
        self.progressbar.grid(row=3,column=1,columnspan=5,pady=10,sticky='w')
        self.l2=tk.Label(self.win,text='搜索进度:',font=('微软雅黑',12))
        self.l2.grid(row=3,column=0)
        # self.l3=tk.Label(self.win,text='加载进度:',font=('微软雅黑',12))
        # self.l3.grid(row=2,column=0)
        #
        #  输入省会名称  搜索按钮
        b1 = tk.Label(self.win,text='请输入省会城市的名称:')
        b1.grid(row=0,column=3,padx=20)
        self.e =tk.Entry(self.win,show=None,width=70)
        self.e.grid(row=0,column=4,padx=20,sticky='e')
        bt1=tk.Button(self.win,text='查询',width=8,height=1,command=lambda:[self.showprogress(),self.search()])
        bt1.grid(row=0,column=5,padx=20)
        #
        #  设置搜索数量
        self.bt3=tk.Button(text='设置最大搜索数量:',command=self.setmaxnumbers)
        self.bt3.grid(row=0,column=0)
        v=tk.StringVar(value='60')
        self.e2 =tk.Entry(self.win,show=None,width=10,textvariable=v)
        self.e2.grid(row=0,column=1,sticky='w')
        #
        self.btnDelete1=tkinter.Button(self.win,text='删除所选数据',font=('微软雅黑',12),command=self.deleteclick,width=10,height=1)
        self.btnDelete1.grid(row=2,column=3)  #
        self.btnDelete2=tkinter.Button(self.win,text='删除所有数据',font=('微软雅黑',12),command=self.deletealldata,width=10,height=1)
        self.btnDelete2.grid(row=2,column=4)


        #获取服务端信息功能
        # bt2=tk.Button(self.win,text='收集城市二手房数量',command=self.getinfo)
        # bt2.grid(row=4,column=0)
        bt3=tk.Button(self.win,text='画出柱状图',command=self.drawhistogram)
        bt3.grid(row=4,column=1)
        btnDelete2=tkinter.Button(self.win,text='关闭服务端',command=self.shutdownserver,width=10,height=1)
        btnDelete2.grid(row=4,column=2)
        btngettree = tkinter.Button(self.win,text='获取当前数据库信息',command=self.gettree,height=1)
        btngettree.grid(row=4,column=3)
        v=tk.StringVar(value='20')
        self.e4 =tk.Entry(self.win,show=None,width=10,textvariable=v)
        self.e4.grid(row=4,column=4,sticky='w')

        bt4 = tk.Button(self.win,text='初始化数据库',command=self.initdatabase)
        bt4.grid(row=4,column=4)
        #自动更新城市
        bt5=tk.Button(self.win,text='设置自动更新城市',command=self.setupdatecity)
        bt5.grid(row=4,column=4,sticky='e')
        v=tk.StringVar(value='沈阳')
        self.e3 =tk.Entry(self.win,show=None,width=10,textvariable=v)
        self.e3.grid(row=4,column=5,sticky='w')
        #
        self.win.mainloop()

    def setupdatecity(self):
        if self.e3.get()=='':
            tkinter.messagebox.showinfo('请输入城市名称')
            pass
        cilent.send(json.dumps('F'+self.e3.get()).encode())
        tmp=cilent.recv(1024)
        if(json.loads(tmp)=='P'):
            tkinter.messagebox.showinfo('errpr','请输入正确的城市名称')
        elif(json.loads(tmp)=='O'):
            tkinter.messagebox.showinfo('info','设置成功')

    def __del__(self):
        cilent.send(json.dumps('D').encode())
        print('hello')

    def shutdownserver(self):
        tmp='D'
        btmp=json.dumps(tmp).encode()
        cilent.send(btmp)
    def initdatabase(self):
        cilent.send(json.dumps('O').encode())
    def save(self):
        tmp = 'C'
        cilent.send(json.dumps(tmp).encode())
    def gettree(self):
        cilent.send(json.dumps('H').encode())
        self.max=(int)(self.e4.get())
        while self.cnt<self.max:
            try:
                data = json.loads(cilent.recv(1024))
            except:
                print("recive error")
                pass
            if(data=='T'):
                print('whilesuccess')
                break
            else :
                self.cnt=self.cnt+1
                self.tree.insert('',int(data[0]),text='', values=data)
                if self.cnt%random.randrange(1,10)==0:
                    self.win.update()
        print('success')


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
        self.cnt=0

    def deleteclick(self):
        if not self.tree.selection():
            tkinter.messagebox.showerror('抱歉','你还没有选择，无法删除数据')
            return
        for item in self.tree.selection():
            self.tree.delete(item)
            self.cnt=self.cnt-1
    

    def setmaxnumbers(self):
        lastmaxn=self.maxnumbers
        self.maxnumbers=int(self.e2.get())
        if(lastmaxn<self.maxnumbers):
            self.searchflag=0
        tkinter.messagebox.showinfo('提示','最大搜索数据数量设置成功')
        cilent.send(json.dumps('A'+str(self.maxnumbers)).encode())
        print('ok')
    
    def search(self):
        if self.searchflag==1:
            tkinter.messagebox.showinfo('提示','请设置更高的搜索数量')
            return
        tmp='S'+self.e.get()
        btmp=json.dumps(tmp).encode()
        cilent.send(btmp)
        self.searchflag=1
        data1 =cilent.recv(1024)
        data2 =json.loads(data1).split(',')
        if data2[0][0] == 'F' and data2[0][1]=='1' and data2[1][0]=='H' and data2[1][1]=='0':
            tkinter.messagebox.showinfo('提示','爬取成功')
            self.progressbar['value']=0
        elif data2[0][0] == 'F' and data2[0][1]=='1' and data2[1][0]=='H' and data2[1][1]=='1':
            tkinter.messagebox.showinfo('提示','请增加最大搜索数据数')



    def showprogress(self):
        for i in range(100):
            self.progressbar['value']=i+1
            self.win.update()
            time.sleep(0.005)

    def getinfo(self):
        cilent.send(json.dumps('G').encode())
        try:
            self.citydict = json.loads(cilent.recv(4096).strip())
        except json.decoder.JSONDecodeError as e:
    # 解码时发生错误，打印错误日志或做其它处理
            print("JSONDecodeError:", e)
        print(self.citydict)
    def drawhistogram(self):
        self.getinfo()
        plt.bar(self.citydict.keys(),self.citydict.values())
        plt.savefig('histogram.png')
        plt.show()
    def funchooseexcle(self):
        self.savemethod=1
        self.savecheckbt.select()
        self.savecheckbt2.deselect()
    def funchoosedatab(self):
        self.savemethod=0
        self.savecheckbt.deselect()
        self.savecheckbt2.select()

if __name__=='__main__':
    cnt=0   #记录数据个数
    city=''
    cilent = socket.socket()
    cilent.connect(('localhost',50000))
    gui = window()

    del gui