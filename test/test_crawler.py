import unittest
from unittest.mock import patch, MagicMock
from src.crawler import crawl

class TestCrawler(unittest.TestCase):
    @patch('requests.get')
    def test_crawl_basic(self, mock_get):
        # 模拟网页返回
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><body><p>Test Quote</p></body></html>'
        mock_get.return_value = mock_response
        
        # 为了快速测试，我们假设只爬一页（不模拟 next 按钮）
        with patch('time.sleep', return_value=None): # 跳过6秒等待以加快测试
            result = crawl()
            self.assertIn("/", result)
            self.assertIn("Test Quote", result["/"])

if __name__ == '__main__':
    unittest.main()