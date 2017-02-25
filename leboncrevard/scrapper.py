import hashlib
import re
from urllib.parse import urlparse, urlsplit, parse_qsl

import requests
from bs4 import BeautifulSoup


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
        ads = soup.find('section', {"class": "tabsContent block-white dontSwitch"})
        if ads == None:
            print("No ads!")
            return None
        for li in ads.find_all('li'):
            a = li.find('a')
            title = a['title']
            link = "http:" + a['href']
            datestr = ""
            try:
                ass = a.find('aside', {"class": "item_absolute"})
                p = ass.find('p');
                for child in p.children:
                    if (len(child.string) > 1):
                        datestr += child.string
                        datestr += " "
                datestr = re.sub('[\n+]', '', datestr).strip()
            except:
                print("Could not get date.")
            try:
                price = a.find('h3', {"class": "item_price"}).string.strip()
            except:
                price = ""
            try:
                ps = a.find_all('p', {"class": "item_supp"})
            except:
                print("No price")
                ps = []
            placement = ""
            for p in ps:
                if p and p.string:
                    if p.string.count("\n") > 4: # This is the only way I found to differentiate these fields...
                        placement = re.sub('[\s+]', '', p.string)
                        break
            try:
                ad_req = requests.get(link)
                if (ad_req.status_code != 200):
                    print("Request failed, status code is {:d}", ad_req.status_code)
                    return
                ad_soup = BeautifulSoup(ad_req.content, "lxml")
                try:
                    description = ad_soup.find('div', {"class": "line properties_description"})
                    m = hashlib.md5()
                    m.update(description.text.encode('utf-8'))
                    content_hash = m.hexdigest()
                except:
                    print("No description!")
                    content_hash = ""
            except:
                content_hash = ""
            ad = LbcAd(title, link, datestr, price, placement, content_hash)
            ad_list.append(ad)
        return ad_list
