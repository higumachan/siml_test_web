import BeautifulSoup
from xml.etree.ElementTree import ElementTree


class DateScheme:
    def __init__(self, tag):
        self.ident = tag.find("identifier").attrib;
        self.date_scheme    = tag.find("Scheme").text;
        self.date_scheme_re = tag.find("Scheme_Re").text;

class TextScheme:
    def __init__(self, tag):
        self.ident = tag.find("identifier").attrib;

class NextPageScheme:
    def __init__(self, tag):
        self.argument = tag.find("Argument").text;

class SchemeReader:
    def __init__(self, file_name):
        f = open(file_name);
        """
        self.xml = f.read();
        self.parse();
        """
        self.root = ElementTree(file=f);
        self.parse();
        f.close();
    
    def parse(self):
        """
        bs = BeautifulSoup.BeautifulSoup(self.xml, "xml");
        print bs
        date_tag = bs.find("Date");
        print date_tag
        self.date = DateScheme(date_tag);
        text_tag = bs.find("Text");
        self.text = TextScheme(text_tag);
        """
        date_tag  = self.root.find("Date");
        self.date = DateScheme(date_tag);
        text_tag = self.root.find("Text");
        self.text = TextScheme(text_tag);
        nextpage_tag = self.root.find("NextPage");
        if (nextpage_tag):
            self.has_nextpage = True;
            self.nextpage = NextPageScheme(nextpage_tag);
        else:
            self.has_nextpage = False;

if __name__ == "__main__":
    SchemeReader("hatena_d.xml");
    
