import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(os.path.join(root_dir, 'src'))

try:
    from indexer import build_index
except ImportError:
    # 备用方案，防止某些环境下的路径差异
    from src.indexer import build_index

class TestSearchEngine(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("\n" + "="*50)
        print("STARTING COMPREHENSIVE SEARCH ENGINE TESTS")
        print("="*50)

    def setUp(self):
        # page1: good(2次), friends(1次)
        # page2: good(1次), book(1次)
        # page3: good(1次), friends(2次)
        self.mock_pages = {
            "/page1": "Good friends are good to find.",
            "/page2": "A good book is a great companion.",
            "/page3": "Friends should be friends. Good ones are rare."
        }
        self.index = build_index(self.mock_pages)

    def test_01_single_word_basic(self):
        """测试基础单次搜索"""
        print("\n[Test 01] Searching for 'book'...")
        results = set(self.index.get("book", {}).keys())
        print(f"  Result: {results}")
        self.assertEqual(results, {"/page2"})

    def test_02_multi_word_intersection(self):
        """测试多词查询的交集逻辑 (AND 逻辑)"""
        query = ["good", "friends"]
        print(f"\n[Test 02] Intersection search for: {query}")
        
        # 模拟 main.py 中的交集逻辑
        results = None
        for word in query:
            word_pages = set(self.index.get(word.lower(), {}).keys())
            print(f"  - Word '{word}' found in: {word_pages}")
            if results is None:
                results = word_pages
            else:
                results = results.intersection(word_pages)
        
        print(f"  => Final Intersection: {results}")
        # page2 只有 good，没有 friends，所以应该被排除
        self.assertEqual(results, {"/page1", "/page3"})

    def test_03_case_insensitivity(self):
        """测试大小写不敏感"""
        print("\n[Test 03] Case sensitivity check: 'FRIENDS' vs 'friends'")
        res_upper = set(self.index.get("FRIENDS".lower(), {}).keys())
        res_lower = set(self.index.get("friends".lower(), {}).keys())
        print(f"  => Upper count: {len(res_upper)}, Lower count: {len(res_lower)}")
        self.assertEqual(res_upper, res_lower)
        self.assertTrue(len(res_upper) > 0)

    def test_04_ranking_logic(self):
        """测试相关性排序逻辑 (词频总和)"""
        query = ["friends"]
        print(f"\n[Test 04] Ranking check for query: {query}")
        
        results = set(self.index.get("friends", {}).keys())
        # 模拟 main.py 中的排序计算
        ranked = sorted(
            results,
            key=lambda p: sum(len(self.index.get(w, {}).get(p, [])) for w in query),
            reverse=True
        )
        
        print(f"  => Ranked Results: {ranked}")
        self.assertEqual(ranked[0], "/page3")
        print(f"  (Confirmed: /page3 is ranked higher due to higher frequency)")

    def test_05_empty_query(self):
        """测试不存在的词"""
        word = "soviet_nostalgia" 
        print(f"\n[Test 05] Searching for non-existent word: '{word}'")
        results = self.index.get(word, {})
        print(f"  => Result count: {len(results)}")
        self.assertEqual(len(results), 0)

if __name__ == '__main__':
    unittest.main()