import pandas as pd
import re
import tkinter as tk
import numpy as np
from tkinter import ttk
import tkinter.messagebox
from numpy import nan as NaN
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.svm import LinearSVR
import difflib
import joblib
def fuzzy_matching(texts, value):  
    texts = texts.split(",")
    texts_score = {}
    for i in texts:
        score = difflib.SequenceMatcher(None, i, value).quick_ratio()
        texts_score[i] = score
    texts_score = sorted(texts_score.items(), key=lambda x: x[1], reverse=False)
    po=1
    match_value =[]
    tmp12=0
    b=[x[1] for x in texts_score]
    for i in range(1,6):
        print(i,end=':')
        print(texts_score[-i])
        tmp12=1  
        match_value.append(int(texts_score[-i][0][texts_score[-i][0].index('{')+1:texts_score[-i][0].index('}')]))
    return match_value

#函数部分
def predictprice():
    global typeofmodel
    newdata=[]
    try:
        square = int(text1.get())
        year = int(text2.get())
    except:
        tkinter.messagebox.showinfo('提示','请输入正确且完整数据后再进行预测')
        return

    if year>2022 or year<1990 :
        tkinter.messagebox.showinfo('提示','请输入正确的建造年份(1990-2021)')
        return 
    if l1.current()<2 or l2.current()<2 or l3.current()<2 or l4.current()<2 or l5.current()<2:
        tkinter.messagebox.showinfo('提示','请设置完房屋信息后再进行预测')
        return 
    print(var4.get())
    newdata.append(featuredict[var4.get()])
    newdata.append(square)
    newdata.append(decorationdict[var3.get()])
    newdata.append(floordict[var2.get()])
    newdata.append(year)
    newdata.append(typedict[var1.get()])
    newdata.append(addressdict[var5.get()])
    newdata=[newdata]

    predict2 = model2.predict(newdata)
    predict1 = model.predict(newdata)
    predict3 = model3.predict(newdata)
    predict4 = model4.predict(newdata)
    print(predict1,predict2,predict3,predict4)
    if typeofmodel == 1:  
        tkinter.messagebox.showinfo('预测值','预测房屋价格为'+str(predict1).strip('[]')+'万元')
    elif typeofmodel == 2:
        tkinter.messagebox.showinfo('预测值','预测房屋价格为'+str(predict2).strip('[]')+'万元')
    elif typeofmodel == 3:
        tkinter.messagebox.showinfo('预测值','预测房屋价格为'+str(predict3).strip('[]')+'万元') 
    elif typeofmodel == 4:
        tkinter.messagebox.showinfo('预测值','预测房屋价格为'+str(predict4).strip('[]')+'万元')   
def fun1():
    global typeofmodel
    typeofmodel=1
    checkbt.select()
    checkbt2.deselect()
    checkbt3.deselect()
    checkbt4.deselect()
def fun2():
    global typeofmodel
    typeofmodel=2
    checkbt2.select()
    checkbt.deselect()
    checkbt3.deselect()
    checkbt4.deselect()
def fun3():
    global typeofmodel
    typeofmodel=3
    checkbt3.select()
    checkbt.deselect()
    checkbt2.deselect()
    checkbt4.deselect()
def fun4():
    global typeofmodel
    typeofmodel=4
    checkbt4.select()
    checkbt2.deselect()
    checkbt3.deselect()
    checkbt.deselect()

def searchfuzzy():
    global text
    try:
        square = int(text1.get())
        year = int(text2.get())
    except:
        tkinter.messagebox.showinfo('提示','请输入正确且完整数据后再进行预测')
        return

    if year>2022 or year<1990 :
        tkinter.messagebox.showinfo('提示','请输入正确的建造年份(1990-2021)')
        return 
    if l1.current()<2 or l2.current()<2 or l3.current()<2 or l4.current()<2 or l5.current()<2:
        tkinter.messagebox.showinfo('提示','请设置完房屋信息后再进行预测')
        return 
    def delButton(tree):
        x=tree.get_children()
        for item in x:
            # print(item)
            tree.delete(item)
    delButton(tree)
    val = var4.get()+'|'+text2.get()+'平米'+'|'+var3.get()+'|'+var2.get()+'|'+text1.get()+'年建'+'|'+var1.get()+'|'+var5.get()
    result = fuzzy_matching(text,val)
    count = 1
    for i in result:
        print(house[i])
        Data=[count,house[i][0],house[i][1],house[i][2],house[i][3],house[i][4],house[i][5]]
        tree.insert('', count,text='', values=Data)    
        count+=1
#函数部分结束

#初始化必要数据部分
typedict={}
floordict={}
decorationdict={}
featuredict={}
typecount = 1
floorcount = 1
decorationcount = 1
featurecount = 1
text = ''   #匹配数据库
house = []

df = pd.read_excel("./housedata.xlsx",engine='openpyxl')
info = df[5]
address = df[2]
price = df[3]
info = [x for x in info]    #读取数据
#地址数据初始化
addressdict = {}
addresscount = 1
address = [x for x in address]
address = [x[x.index('-')+1:] for x in address]
for i in address:
    if i not in addressdict:
        addressdict[i] = addresscount
        addresscount+=1
# 相似度匹配的初始化数据
p=df[5]
p = [x.split('|') for x in p]
for i, items in enumerate(p): 
    del(p[i][2])
    p[i] = [item.strip() for item in items]  #清楚空格
    p[i]="|".join(p[i])

for i, items in enumerate(p): 
    p[i] = items+'|'+address[i] +'{'+ str(i) +'}'
  
for i in p:
    text = text+ i.replace(" ",'') + ','
ww1=df[0]
ww2=df[1]
ww3=df[2]
ww4=df[3]
ww5=df[4]
ww6=df[5]
for i in range(len(p)):
    house.append([ww1[i],ww2[i],ww3[i],ww4[i],ww5[i],ww6[i]])
# 初始化结束



price = [x for x in price]
info  = [x.split('|') for x in info]
for i, items in enumerate(info):               #处理数据为数值型 下列代码全是
    info[i] = [item.strip() for item in items]  #清楚空格
    if len(info[i])==6:
        info[i].insert(5,'2015年建')                    #补全数据
    if len(info[i])==8:
        del(info[i][-1])  
    if info[i][0] not in featuredict:    #几室几厅 处理特征
        featuredict[info[i][0]] = featurecount
        info[i][0]=featuredict[info[i][0]] 
        featurecount += 1 
    elif info[i][0] in featuredict:
        info[i][0] = featuredict[info[i][0]]

    info[i][1] = info[i][1].strip('平方米')         #1为房屋的面积
    info[i][5] = re.sub('[年建]','',info[i][5])
    
    if info[i][6] not in typedict:  #房屋类型没有出现
        typedict[info[i][6]] = typecount #添加新房屋类型进字典
        info[i][6]=typedict[info[i][6]]
        typecount += 1   #计数器加1
    elif info[i][6] in typedict:
        info[i][6] = typedict[info[i][6]]  #已有的直接转换数值型

    tmp=info[i][4][0]
    if tmp != '高' and tmp != '中' and tmp != '低':
        floor = int(info[i][4][:-1])
        if floor < 10:
            info[i][4]='低'
        elif floor <20:
            info[i][4]='中'
        else:
            info[i][4]='高'
    else:
        info[i][4] = info[i][4][0]
    if info[i][4] not in floordict: #楼层高低
        floordict[info[i][4]] = floorcount
        info[i][4]=floordict[info[i][4]]
        floorcount += 1 
    elif info[i][4] in floordict:
        info[i][4] = floordict[info[i][4]]

    if info[i][3] not in decorationdict: #装饰
        decorationdict[info[i][3]] = decorationcount
        info[i][3]=decorationdict[info[i][3]]
        decorationcount += 1         
    elif info[i][3] in decorationdict:
        info[i][3] = decorationdict[info[i][3]]
    del(info[i][2])    #房屋朝向删除 一个种类多且对房价影响较小的因素
    info[i].append(addressdict[address[i]])
    #数据预处理结束


X = info
y = price
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = LinearRegression()   #线性回归
model.fit(X_train, y_train)
filename = 'model1.pkl'
joblib.dump(model, filename)
model2 = LinearSVR()         #SVR回归
model2.fit(X_train, y_train)
filename = 'model2.pkl'
joblib.dump(model, filename)
model3 = DecisionTreeRegressor(max_depth=6,min_samples_leaf=2) #决策树回归
model3.fit(X_train, y_train)
filename = 'model3.pkl'
joblib.dump(model, filename)
model4 = MLPRegressor(hidden_layer_sizes=(10,), max_iter=5000) #神经网络模型
model4.fit(X_train, y_train)
filename = 'model4.pkl'
joblib.dump(model, filename)
#界面设计：
window = tk.Tk()
#选择属性
window.tk.call("source", "azure.tcl")
window.tk.call("set_theme", "light")
#房屋属性选择设置
var1 = tkinter.StringVar()
l1=ttk.Combobox(window,height=7,textvariable=var1)
l1['value'] = ('请选择楼房类型','------------------','板楼','板塔结合','塔楼')
l1.current(0)

var2 = tkinter.StringVar()
l2=ttk.Combobox(window,height=7,textvariable=var2)
l2['value'] = ('请选择楼层高低','------------------','高','中','低')
l2.current(0)

var3 = tkinter.StringVar()
l3=ttk.Combobox(window,height=7,textvariable=var3)
l3['value'] = ('请选择装修类型','------------------','其他','精装','毛坯','简装')
l3.current(0)

var4 = tkinter.StringVar()
l4=ttk.Combobox(window,height=7,textvariable=var4)
l4['value'] = ('请选择户型','------------------','1室0厅','1室1厅','1室2厅','2室1厅','2室2厅','3室1厅','3室2厅','3室3厅','4室1厅','4室2厅','4室3厅','4室4厅','5室2厅','5室3厅','6室1厅','6室2厅','6室3厅')
l4.current(0)

var5 = tkinter.StringVar()
l5 = ttk.Combobox(window,height=7,textvariable=var5)
l5['value'] = ('请选择区域','------------------','西三台子', '于洪广场', '奥体', '新市府', '长白', '棋盘山', '道义', '经济技术开发区', '会展中心', '四台子', '塔湾', '长青', '东湖', '于洪新城', '北陵', '白塔', '蒲河新城', '启工街', '三台子', '八王寺', '八一', '工人村', '北行', '兴工街', '东北大马路', '望花', '黎明', '北站北', '丁香湖', '泉园', '保工北', '铁西广场', '二十一世纪', '陵西', '张士', '艳粉', '营城子', '重工街', '东五里河', '正良', '市府', '北二路', '霁虹', '滑翔', '南市场', '新立堡', '三好街', '荷兰村', '新南站', '保工南', '云峰', '长客', '方家栏', '南湖', '陵东', '金廊', '北一路', '上园', '东中街', '二台子', '和平湾', '首府新区', '33号 -于洪广场', '新华广场', '南塔', '陶瓷城', '造化', '金融中心', '理工大学')
l5.current(0)

l1.grid(row=1,column=0,pady=15,padx=15)
l2.grid(row=1,column=1,pady=15,padx=15)
l3.grid(row=1,column=3,pady=15,padx=15)
l4.grid(row=1,column=4,pady=15,padx=15)
l5.grid(row=3,column=0,pady=15,padx=15)
#输入面积和日期控件以及文本控件
text1 = tk.Entry(window,show=None,width=30)
text2 = tk.Entry(window,show=None,width=30)
label1 = tk.Label(window,text='请输入房屋面积(平方米):',font='宋体')
label2 = tk.Label(window,text='请输入房屋的建造日期:',font='宋体')

label1.grid(row=2,column=0)
text1.grid(row=2,column=1)
label2.grid(row=2,column=3)
text2.grid(row=2,column=4)

label3 = tk.Label(window,text='沈阳二手房价格预测:',font='宋体',)
label3.grid(row=0,column=0)
#按钮预测房屋
bt1 = tk.Button(window,text='预测房价',width=10,height=1,command=predictprice,font='宋体',background='pink',foreground='blue')
bt1.grid(row=3,column=3)
#按钮匹配相似房屋
bt2 = tk.Button(window,text='匹配相似房屋',command=searchfuzzy,font='宋体',background='pink',foreground='red')
bt2.grid(row=3,column=4)
#两个不同模型的切换
label4 = tk.Label(window,text='选择模型:',font='宋体')
checkbt=tk.Checkbutton(window,text='SVR回归',command=fun1,font='宋体')
checkbt2=tk.Checkbutton(window,text='多元线性回归（最小二乘法）',command=fun2,font='宋体')
checkbt3=tk.Checkbutton(window,text='神经网络回归',command=fun3,font='宋体')
checkbt4=tk.Checkbutton(window,text='决策树回归',command=fun4,font='宋体')
checkbt.select()
typeofmodel=1  #模型有四种 linear，svr模型，神经网络模型，决策树模型
checkbt.grid(row=0,column=3,sticky='e')
checkbt2.grid(row=0,column=4)
checkbt3.grid(row=0,column=3,sticky='w')
checkbt4.grid(row=0,column=2,sticky='e')
label4.grid(row=0,column=1)
#树形控件对相似房屋进行展示
columns={
'ID':25,
'城市':40,
'广告标题':350,
'地址':200,
'总价/万元':50,
'每平方价格':100,
'主要信息':450
}
tree=ttk.Treeview(window,height=18,show='headings')
tree['columns'] = list(columns)
for column in columns:  # 批量设置列属性
    tree.heading(column, text=column)  # #设置列标题
    tree.column(column, width=columns[column], anchor='center')  
tree.grid(rows=5,columnspan=5,column=0)

window.mainloop()