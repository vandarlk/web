import unittest
from src.indexer import build_index

class TestSearchLogic(unittest.TestCase):
    def setUp(self):
        # 准备模拟数据：page1 包含两个词，page2 只包含一个词
        self.mock_pages = {
            "/page1": "Good friends are hard to find.",
            "/page2": "A good book is a great companion."
        }
        self.index = build_index(self.mock_pages)

    def test_single_word_find(self):
        # 测试单个单词查询
        word = "friends"
        results = set(self.index.get(word.lower(), {}).keys())
        self.assertIn("/page1", results)
        self.assertNotIn("/page2", results) [cite: 37]

    def test_multi_word_find_intersection(self):
        # 测试多词查询（find good friends）
        # 逻辑：获取每个词的页面集合，然后取交集
        query = ["good", "friends"]
        
        # 获取第一个词的页面
        results = set(self.index.get(query[0].lower(), {}).keys())
        # 与后续词的页面取交集
        for word in query[1:]:
            word_pages = set(self.index.get(word.lower(), {}).keys())
            results = results.intersection(word_pages)
        
        # 预期：只有 page1 同时包含这两个词
        self.assertIn("/page1", results)
        self.assertNotIn("/page2", results) [cite: 38, 40]

    def test_case_insensitive_search(self):
        # 测试大小写不敏感查询 [cite: 19]
        query_word = "GOOD"
        results = self.index.get(query_word.lower(), {})
        self.assertTrue(len(results) > 0)
        self.assertIn("/page1", results)

if __name__ == '__main__':
    unittest.main()