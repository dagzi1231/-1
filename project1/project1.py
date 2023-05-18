import pinyin
import string
import sys
import time
import logging
import difflib
#输入name
import sys
import getopt
import argparse

def main(argv):

    try:
        opts, args = getopt.getopt(argv[1:], "-h-s:-m:", ["help", "search=", "menu="])
    except getopt.GetoptError as e:
        print(e.msg)
        print("输入--help或-h获取相关信息")
        sys.exit(2)


    opts, args = getopt.getopt(argv[1:], "-h-s:-m:", ["help", "search=", "menu="])

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('输入（-s 参数 或者 -m 参数）来在程序启动时选择是否启用模糊匹配，以下为例子：')
            print('  python project1.py -s 1    意为开启模糊匹配')
            print('  python project1.py -s 0    意为开启精确匹配（只输出最相似的值）')
            print("  python project1.py -m 1    意为开启菜单功能（默认关闭菜单功能）")
            print('  python project1.py -m 0    意为不开启菜单功能（默认开启模糊匹配）')
            sys.exit()
        elif opt in ("-s", "--search"):
            global flagof 
            flagof= int(arg)
        elif opt in ("-m", "--menu"):
            global flagg2 
            flagg2= int(arg)
    

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
    if flagof==1 :
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
        return texts_score[-1][0]
def get_pinyin_first_alpha(name):
    return "".join([i[0] for i in pinyin.get(name, " ").split(" ")])
flagof=1
flagg2=0
if len(sys.argv) < 2:
    sys.exit("请输入--help或-h获取更多帮助")
main(sys.argv)


file_name="./城市数据.txt"
filename123="./logging.txt"


if flagg2==1:
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
            flagof=0
            logging.info("取消了模糊匹配")
            print("模糊匹配已取消")
        elif(tmpp==3):
            flagof=1
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




s=input("输入城市名称:")

data=get_pinyin_first_alpha(s)
data=data.upper()
f = open(file_name,encoding='utf-8')

data1=f.read()
logging.info("数据文件打开完成！")

t = 60
print("*******************************搜索进度*******************************")
start = time.perf_counter()
for i in range(t + 1):
    finsh = "▓" * i
    need_do = "-" * (t - i)
    progress = (i / t) * 100
    dur = time.perf_counter() - start
    print("\r{:^3.0f}%[{}->{}]{:.2f}s".format(progress, finsh, need_do, dur), end="")
    time.sleep(0.05)
logging.info("进度条加载完毕！")

print()

res=fuzzy_matching(data1,s)
if res!=-1:
    logging.info("模糊匹配完成！")
    result=get_pinyin_first_alpha(res)
    logging.info("汉字拼音首字母获取成功！")
    result=result.upper()
    print("结果为：",end='')
    print(result)
else:
    print("没有找到相应的城市！可重新启动程序在初始化菜单选择4进行补充！")
logging.info("程序成功执行！")
#print(data)