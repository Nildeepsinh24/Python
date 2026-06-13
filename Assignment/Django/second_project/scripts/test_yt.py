from youtubesearchpython import VideosSearch
import sys

sys.stdout.reconfigure(encoding='utf-8')

def test_search(query):
    print(f"Searching for: {query}")
    videosSearch = VideosSearch(query, limit = 5)
    results = videosSearch.result()['result']
    for idx, r in enumerate(results):
        print(f"Result {idx+1}: {r['title']} - {r['link']}")

test_search("Breaking Bad Season 1 official trailer")
test_search("Squid Game Season 2 official trailer")
test_search("The Office Season 5 official trailer")
