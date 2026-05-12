import unittest
from src.indexer import build_index

class TestIndexer(unittest.TestCase):
    def setUp(self):
        self.sample_pages = {
            "/page1": "Good friends are happy.",
            "/page2": "Better to be a good person."
        }
        self.index = build_index(self.sample_pages)

    def test_case_insensitivity(self):
        # 测试 'Good' 和 'good' 是否被视为同一个词 [cite: 19]
        self.assertIn("good", self.index)
        self.assertIn("/page1", self.index["good"])
        self.assertIn("/page2", self.index["good"])

    def test_word_positions(self):
        # 测试是否记录了单词位置
        # "good" 在 page1 是第0个词
        self.assertEqual(self.index["good"]["/page1"], [0])

    def test_multi_word_logic(self):
        # 模拟 main.py 中的 find 逻辑：查找包含 "good" 和 "friends" 的页面
        query = ["good", "friends"]
        results = set(self.index.get(query[0], {}).keys())
        for word in query[1:]:
            results = results.intersection(set(self.index.get(word, {}).keys()))
        
        self.assertIn("/page1", results)
        self.assertNotIn("/page2", results)

if __name__ == '__main__':
    unittest.main()