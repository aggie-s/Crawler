import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

url = "http://www.mileycyrus.com/"

urls = [url]
visited = [url]

while len(urls) > 0:
    try:
        htmltext = urllib.request.urlopen(urls[0])
    except:
        print(urls[0])
    soup = BeautifulSoup(htmltext, "html.parser")

    urls.pop(0)
    print(len(urls))

    for tag in soup.findAll('a', href=True):
        tag['href'] = urllib.parse.urljoin(url, tag['href'])
        if url in tag['href'] and tag['href'] not in visited:
            urls.append(tag['href'])
            visited.append(tag['href'])

    print(visited)
