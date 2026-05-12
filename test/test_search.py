import unittest
import sys
import os

# 获取当前脚本的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 找到 web 根目录
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
# 强行把根目录和 src 目录塞进 Python 的搜索列表
sys.path.append(root_dir)
sys.path.append(os.path.join(root_dir, 'src'))

# 这样无论你在哪个路径下跑，都能找到模块
try:
    from indexer import build_index
except ImportError:
    from src.indexer import build_index

class TestSearchLogic(unittest.TestCase):
    def setUp(self):
        # 准备模拟数据
        self.mock_pages = {
            "/page1": "Good friends are hard to find.",
            "/page2": "A good book is a great companion."
        }
        self.index = build_index(self.mock_pages)

    def test_single_word_find(self):
        word = "friends"
        # 逻辑：从索引中获取包含该词的页面集合
        results = set(self.index.get(word.lower(), {}).keys())
        self.assertIn("/page1", results)
        self.assertNotIn("/page2", results)

    def test_multi_word_find_intersection(self):
        # 测试多词查询（good friends）
        query = ["good", "friends"]
        results = None
        for word in query:
            word_pages = set(self.index.get(word.lower(), {}).keys())
            if results is None:
                results = word_pages
            else:
                results = results.intersection(word_pages)
        
        self.assertIn("/page1", results)
        self.assertNotIn("/page2", results)

if __name__ == '__main__':
    unittest.main()