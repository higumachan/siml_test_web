import sys
from scheme import SchemeReader
from parser import Parser
from urls   import urls

url = sys.argv[1];
scheme_file = sys.argv[2];

scheme_reader = SchemeReader(scheme_file);

parser = Parser(scheme_reader, url);

print url
print parser.text
print parser.date
print 

