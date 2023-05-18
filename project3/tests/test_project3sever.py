import unittest
import sys
import os
from project3sever import save
from project3sever import fuzzy_matching
from project3sever import get_pinyin_first_alpha
class TestUpdateData(unittest.TestCase):
    def setUp(self):
        # 在测试开始前，初始化虚拟的数据库
        self.db = {}
    def test_fuzzy_matching(self):
        city='沈阳'
        f = open("./城市数据.txt",encoding='utf-8')  #
        data1=f.read()                             
        testcity=fuzzy_matching(data1,city)         #测试模糊匹配程序是否运行成功
        self.assertEqual(testcity,'沈阳')            #利用断言测试沈阳
        self.assertEqual(fuzzy_matching(data1,"不存在的城市"),-1) #利用断言测试输入的城市不存在时的结果
    def test_get_pinyin_first_alpha(self):
        tmp='北京'
        self.assertEqual(get_pinyin_first_alpha(tmp),'bj') #测试获取拼音首字母是否正确，北京为bj
    def test_save(self):
        # 测试程序能否正确地保存搜索结果到指定的文件中
        city = '北京'
        save(city)
        # 检查保存的文件是否存在当前路径下
        self.assertTrue(os.path.exists('hous.db'))
if __name__ == '__main__':
    unittest.main()