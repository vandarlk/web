import sys
import os

# 确保 Python 解释器能找到 src 目录下的模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from crawler import crawl
    from indexer import build_index, save_index, load_index
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

def main():
    index = {}
    print("--- Search Tool Shell ---")
    print("Available commands: build, load, print <word>, find <query>, exit")
    
    while True:
        try:
            line = input("> ").strip()
            if not line:
                continue
            
            parts = line.split()
            cmd = parts[0].lower()

            if cmd == "build":
                print("Starting process... This will respect the 6s politeness window.")
                data = crawl()
                if not data:
                    print("Crawl failed or returned no data.")
                    continue
                index = build_index(data)
                
                # 防御性编程：确保保存目录存在 
                if not os.path.exists('data'):
                    os.makedirs('data')
                save_index(index, "data/index.json")
                print(f"Success: Index built with {len(index)} words.")

            elif cmd == "load":
                path = "data/index.json"
                if os.path.exists(path):
                    index = load_index(path)
                    print("Index loaded successfully.")
                else:
                    print(f"Error: {path} not found. Please run 'build' first.")

            elif cmd == "print":
                if len(parts) < 2:
                    print("Usage: print <word>")
                    continue
                word = parts[1].lower()
                # 检查单词是否存在于索引中 [cite: 33]
                print(index.get(word, "Word not found."))

            elif cmd == "find":
                if len(parts) < 2:
                    print("Usage: find <query>")
                    continue
                
                query_words = [w.lower() for w in parts[1:]]
                results = None
                
                for w in query_words:
                    pages = set(index.get(w, {}).keys())
                    if results is None:
                        results = pages
                    else:
                        # 执行交集操作，确保所有词都在页面中 [cite: 38, 40]
                        results = results.intersection(pages)
                
                if results:
                    print(f"Found in {len(results)} pages:")
                    for p in results:
                        print(f" - {p}")
                else:
                    print("No matches found for the given query.")

            elif cmd == "exit":
                print("Exiting...")
                break
            else:
                print(f"Unknown command: '{cmd}'.")

        except EOFError: # 处理 Ctrl+D
            break
        except Exception as e:
            # 防御性编程：捕获所有未知异常，防止 Shell 崩溃 
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()