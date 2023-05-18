import unittest
import sys
import tkinter
import os
from project3cilent import *
class TestWindow(unittest.TestCase):
    def test_init(self):
        self.client = window()
        self.assertIsNotNone(self.client.win)
        self.assertEqual(self.client.maxnumbers, 60)
        self.assertEqual(self.client.cnt, 0)
        self.assertEqual(self.client.citydict, {})
        self.assertEqual(self.client.searchflag, 0)
    def test_drawhistogram(self):
        # 测试程序能否正确地绘制柱状图
        self.client.drawhistogram()
        # 检查绘制的图片是否存在
        self.assertTrue(os.path.exists('histogram.png'))

    def tearDown(self):
        # 在测试用例执行后的清理工作，例如关闭窗口、清空数据库等
        self.client.win.destroy()
if __name__ == '__main__':
    unittest.main()