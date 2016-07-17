from bs4 import BeautifulSoup
import urllib.request as urllib

movies = []
root = "http://nadi-kon.tumblr.com"
extension = '/tagged/film/page/1'

while(True):
    page = urllib.urlopen(root+extension).read()
    soup = BeautifulSoup(page,"html.parser")
    entries = soup.find(id="entries")
    for post in entries.find_all(id="post"):
        caption = post.find("blockquote")
        if caption is None:
            continue
        for line in caption.find_all("p"):
            caption = line.text.strip()
            if "dir." in caption:
                left_p = caption.rfind("(")
                right_p = caption.rfind(")")
                dir = caption.index("dir.")+len("dir.")
                movie = caption[0:left_p].split()
                year = caption[left_p+1:right_p].split()[0]
                director = caption[dir:].split()
                text = " ".join(movie)+" ("+year+") dir. "+" ".join(director)
                if text not in movies:
                    movies.append(text)
    nav = entries.find(id="pagination")
    links = nav.find_all("a", string="next", href=True)
    if len(links) is 0:
        break
    else:
        extension = links[0]["href"]
print("\n".join(sorted(movies)))
with open("output.txt", "w", encoding="utf-8") as outfile:
    outfile.write("\n".join(sorted(movies)))