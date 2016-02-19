import requests, pprint, re, html, hashlib
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlsplit, parse_qsl

class LbcAd:
    def __init__(self, title, link, date, price, placement, content_hash):
        self.title = title
        self.link = link
        self.date = date
        self.price = price
        self.placement = placement
        self.content_hash = content_hash

    def get_text(self):
        return self.title + "\n" + self.link + "\n" + self.date + "\n" + self.price + "\n" + self.placement + "\n\n"

    def get_hash(self):
        return self.content_hash

    def get_link(self):
        return self.link

    def print_ad(self):
        print("Title: " + self.title)
        print("Link: " + self.link)
        print("Date: " + self.date)
        print("Price: " + self.price)
        print("Placement: " + self.placement)
        print("Hash: " + self.content_hash)

class LbcScrapper:
    def __init__(self, url):
        self.url = url
        parsed = urlparse(url)
        self.location = parsed.scheme + "://" + parsed.netloc + parsed.path
        self.params = dict(parse_qsl(urlsplit(url).query))

    def test_connectivity(self):
        req = requests.get(self.location)
        if (req.status_code != 200):
            return False
        return True

    def scrap(self):
        ad_list = []
        req = requests.get(self.location, params=self.params)
        if (req.status_code != 200):
            print("Request failed, status code is {:d}", req.status_code)
            return None
        soup = BeautifulSoup(req.content, "lxml")
        ads = soup.find('div', {"class": "list-lbc"})
        if ads == None:
            print("No ads!")
            return None
        for a in ads.find_all('a'):
            try:
                a['class']
            except KeyError:
                title = a['title']
                link = "http:" + a['href']
                datestr = ""
                try:
                    date = a.find('div', {"class": "date"})
                    for child in date.children:
                        if (len(child.string) > 1):
                            datestr += child.string
                            datestr += " "
                    datestr = re.sub('[\n+]', '', datestr).strip()
                except:
                    datestr = ""
                try:
                    price = a.find('div', {"class": "price"}).string.strip()
                except:
                    price = ""
                try:
                    placement = re.sub('[\s+]', '', a.find('div', {"class": "placement"}).string)
                except:
                    placement = ""
                try:
                    ad_req = requests.get(link)
                    if (ad_req.status_code != 200):
                        print("Request failed, status code is {:d}", ad_req.status_code)
                        return
                    ad_soup = BeautifulSoup(ad_req.content, "lxml")
                    description = ad_soup.find('div', {"class": "content"})
                    m = hashlib.md5()
                    m.update(description.text.encode('utf-8'))
                    content_hash = m.hexdigest()
                except:
                    content_hash = ""
                ad = LbcAd(title, link, datestr, price, placement, content_hash)
                ad_list.append(ad)
        return ad_list
