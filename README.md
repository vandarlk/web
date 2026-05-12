#  Features
Robust Crawler: Implements a polite crawling strategy with a 6-second delay and comprehensive error handling.

Inverted Index: Efficient data structure for fast word retrieval and positional lookups.

Advanced Search: Supports multi-word queries with Boolean Intersection (AND) logic.

Relevance Ranking: Search results are automatically ranked by total word frequency.

Professional Testing: A detailed unit test suite covering core search and ranking algorithms.

 Installation
Clone the repository:

Bash
git clone https://github.com/vandarlk/web.git
cd web
Install dependencies:

Bash
pip install requests beautifulsoup4
 Usage
Run the main shell to interact with the search engine:

Bash
python src/main.py
Supported Commands:
build: Start crawling and build the index (respects the 6s politeness window).

load: Load the existing index from data/index.json.

print <word>: Display index data for a specific word.

find <query>: Search for pages containing all query words, ranked by relevance.

exit: Close the application.

 Testing
To run the automated test suite and see the detailed logic verification:

Bash
python tests/test_search.py
 Project Structure
src/: Core source code (crawler, indexer, main shell).

tests/: Unit tests for search and ranking logic.

data/: Directory for the generated index.json.