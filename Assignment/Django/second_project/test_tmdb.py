import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0'
}

r = requests.get('https://www.themoviedb.org/search?query=The+Dark+Knight', headers=headers)
# Find the first movie URL
match = re.search(r'href="(/movie/\d+[^"]*)"', r.text)
if match:
    movie_url = "https://www.themoviedb.org" + match.group(1) + "/cast"
    r2 = requests.get(movie_url, headers=headers)
    cast = re.findall(r'<p><a href="/person/\d+-[^"]*">([^<]+)</a></p>', r2.text)
    print(cast[:15])
else:
    print("Not found")
