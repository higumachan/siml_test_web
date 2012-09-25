#coding: utf-8

from scheme import SchemeReader
from parser import Parser
from urls   import urls
from urlparse import urlparse
import urllib

country_domains = [
    "co",
    "com",
    "jp",
    "tu",
    "nadeko",
];

domain_to_schemefile = {
    "blogspot": "kml/Scheme.xml", 
    "ismedia":  "kml/Wedge.xml", 
}

class SiteData:
    def __init__(self, parser):
        self.title  = parser.title;
        self.text   = parser.text;
        self.date   = parser.date;
        self.images = parser.images;

def scraping(urls):
    result = [];
    for url in urls:
        print url
        domain = urlparse(url)[1];
        toplevel_domain = get_toplevel_domain(domain);
        print toplevel_domain
        scheme_reader = SchemeReader(domain_to_schemefile[toplevel_domain]);
        parser = Parser(scheme_reader, url);
        result.append(SiteData(parser));
    return result;

def get_toplevel_domain(domain):
    l = domain.split(".");
    l.reverse();
    for name in l:
        if not (name in country_domains):
            return name;
    return None;

if __name__ == "__main__":
    urls = ["http://wedge.ismedia.jp/articles/-/2080"];
    print  scraping(urls, "Wedge.xml")[0].text;
