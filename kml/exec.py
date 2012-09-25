from scheme import SchemeReader
from parser import Parser
from urls   import urls
import urllib2

scheme_reader = SchemeReader("hatena_d.xml");

f = open("nadeko.txt", "w");
for url in urls:
    parser = Parser(scheme_reader, url);
    print url
    print parser.text;
    print parser.date;
    print 
    f.write(url);
    f.write("\n");
    f.write(parser.text.encode("utf-8"));
    f.write("\n");
    f.write("\n");
    #f.write(parser.date.encode("utf-8"));

