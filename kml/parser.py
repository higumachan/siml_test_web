
#coding:utf-8

import BeautifulSoup
import datetime
import re
import urllib2
from urlparse import urlparse, urlunparse
from PIL import Image

MINIMUM_WIDTH  = 100;
MINIMUM_HEIGHT = 100;

class Parser:
    def __init__(self, scheme, url):
        self.parse(scheme, url);
    
    def parse(self, scheme, url):
        print url
        html = url_open(url);
        bs = BeautifulSoup.BeautifulSoup(html);
        self.title   = self.parse_title(bs);
        self.text    = self.parse_text(scheme.text, bs);
        self.date    = self.parse_date(scheme.date, bs);
        self.images  = self.parse_image(scheme.text, url, bs);
        if (scheme.has_nextpage):
            pages = _get_pages(scheme.nextpage, bs);
            for page in pages:
                print page
                html = url_open(_get_page_url(url, page, scheme));
                bs = BeautifulSoup.BeautifulSoup(html);
                self.text   += self.parse_text(scheme.text, bs);
                self.images += self.parse_image(scheme.text, url, bs);
                page += 1;
    
    def parse_title(self, bs):
        title = bs.find("title");
        if title is not None:
            return title.text;
        return None;

    def parse_text(self, scheme, bs):

        attrs = {};
        if (scheme.ident.has_key("id")):
            id = scheme.ident["id"];
            attrs["id"] = re.compile(id);

        if (scheme.ident.has_key("class")):
            cl = scheme.ident["class"];
            attrs["class"] = re.compile(cl);

        #id_search = re.compile(id);
        #cl_search = re.compile(cl);

        result = bs.find(attrs=attrs).text;

        return result;

    def parse_image(self, scheme, url, bs):
        attrs = {};
        if (scheme.ident.has_key("id")):
            id = scheme.ident["id"];
            attrs["id"] = re.compile(id);

        if (scheme.ident.has_key("class")):
            cl = scheme.ident["class"];
            attrs["class"] = re.compile(cl);

        main_contents = bs.find(attrs=attrs);
        images = [image_tag["src"] for image_tag in main_contents.findAll("img") if image_tag.has_key("src")]
        for i in range(len(images)):
            if (not images[i].startswith("http")):
                parsed_url     = list(urlparse(url));
                parsed_url[2]  = images[i];
                images[i]       = urlunparse(parsed_url);
                print images[i]
        print images
        return self._image_filter(images);
        
    
    def parse_date(self, scheme, bs):
        attrs = {};
        if (scheme.ident.has_key("id")):
            id = scheme.ident["id"];
            attrs["id"] = re.compile(id);
        if (scheme.ident.has_key("class")):
            cl = scheme.ident["class"];
            attrs["class"] = re.compile(cl);

        date_str = bs.find(attrs=attrs).text;
        #date_str = date_str[:len(scheme.date_scheme) + 1];
        m = re.search(scheme.date_scheme_re, date_str);
        if m:
            date_str = m.group(0);
        else:
            return None
        result = datetime.datetime.strptime(date_str.encode("utf-8"), scheme.date_scheme.encode("utf-8"));

        return (result);

    def _image_filter(self, images):
        result = [];
        for image in images:
            extension = image.split(".")[-1];
            data = url_open(image).read();
            f = open("temp.%s" % extension, "wb");
            f.write(data);
            f.close();
            im = Image.open("temp.%s" % extension);
            (w, h) = im.size;
            print w, h
            if (w >= MINIMUM_WIDTH and h >= MINIMUM_HEIGHT):
                result.append(image);
        return result;

def _get_page_url(url, page, scheme):
    return (url.split("?")[0] + "?%s=%d" % (scheme.nextpage.argument, page));

def _get_pages(scheme, bs):
    result = set([]);
    print scheme.argument + r"=([0-9]*)"
    pattern = re.compile(scheme.argument + r"=([0-9]*)")
    attrs = {};
    attrs["href"] = pattern;
    page_tags = bs.findAll(attrs=attrs);
    print page_tags
    for page_tag in page_tags:
        print page_tag["href"]
        url = page_tag["href"];
        find_index = url.find(scheme.argument + "=" )
        result.add(int(url[find_index + len(scheme.argument + "="):]));

    print result
    return list(result)   

def url_open(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    return opener.open(url);

