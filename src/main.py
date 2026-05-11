import sys
import os

# 强制将当前文件所在的目录 (src) 加入到 Python 的搜索路径中
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# 现在导入就不会报错了
try:
    from crawler import crawl
    from indexer import build_index, save_index, load_index
except ImportError as e:
    print(f"导入错误: {e}")
    print(f"当前搜索路径: {sys.path}")
    sys.exit(1)

def main():
    index = {}
    print("--- Search Tool Shell ---")
    print("Commands: build, load, print <word>, find <query>, exit")
    
    while True:
        try:
            line = input("> ").strip()
            if not line: continue
            parts = line.split()
            cmd = parts[0].lower()

            if cmd == "build":
                print("Starting crawl... (Each page takes 6s, please wait)")
                data = crawl()
                index = build_index(data)
                # 确保 data 文件夹存在
                if not os.path.exists('data'):
                    os.makedirs('data')
                save_index(index, "data/index.json")
                print(f"Success! Index built with {len(index)} words.")

            elif cmd == "load":
                if os.path.exists("data/index.json"):
                    index = load_index("data/index.json")
                    print("Index loaded successfully.")
                else:
                    print("Error: data/index.json not found. Run 'build' first.")

            elif cmd == "print" and len(parts) > 1:
                word = parts[1].lower()
                print(index.get(word, "Word not found in index."))

            elif cmd == "find" and len(parts) > 1:
                query_words = [w.lower() for w in parts[1:]]
                results = None
                for w in query_words:
                    pages = set(index.get(w, {}).keys())
                    if results is None:
                        results = pages
                    else:
                        results = results.intersection(pages)
                
                if results:
                    print(f"Found in {len(results)} pages:")
                    for p in results: print(f" - {p}")
                else:
                    print("No pages match your query.")

            elif cmd == "exit":
                break
            else:
                print("Unknown command or missing arguments.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()