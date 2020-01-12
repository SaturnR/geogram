#!/usr/bin/env python3

from robobrowser import RoboBrowser
import sqlite3


#&w2=ბ&w3=ო
#&w1=ა

url = "http://www.nplg.gov.ge/saskolo/index.php?a=list&d=42&p={}&w1={}"

class collector:

    def __init__(self, browser = RoboBrowser(history=True)):
        self.words = {}
        self.pages = None
        self.browser = browser
        self.alphabet = "ა", "ბ", "გ", "დ", "ე", "ვ", "ზ", "თ",\
            "ი", "კ", "ლ", "მ", "ნ", "ო", "პ", "ჟ", "რ", "ს",\
            "ტ", "უ", "ფ", "ქ", "ღ", "ყ", "შ", "ჩ", "ც", "ძ",\
            "წ", "ჭ", "ხ", "ჯ", "ჰ";
        self.url = "http://www.nplg.gov.ge/saskolo/index.php?a=list&d=42&p={}&w1={}"
        
    def parsewords(self, word):
        if word.find("და არა"):
            word = word.split("და არა")[0]
        for sp in (",", " ", ".", ")", "(", "[", "]", "/", "\\" ):
            if len(word.split(sp)) > 1:
                for w in word.split(sp):
                    self.parsewords(w)
                return self.words
            
        word = word.strip().strip(".").strip(",").strip(":").strip(";").strip("!")
        if word in self.words:
            self.words[word] += 1
        else:
            self.words[word] = 1
            
        return self.words
    
    def save(self, data, path='./words.db', append=False):
        '''data: type dictionary, like : {'გამარჯობა' : 10}'''
        conn = sqlite3.connect(path)
        c = conn.cursor()
        if not append:
            c.execute('CREATE TABLE words (word text, occurrence real)')
        for n in data:
            print(n)
            c.execute("INSERT INTO words VALUES ('"+n+"',"+str(data[n])+")")
        conn.commit()
        conn.close()

    def load_dictionary(self, path='./words.db', dbfilter=""):
        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute("SELECT * FROM words" + dbfilter)
        dbwords = c.fetchall()
        words = {}
        for w in dbwords:
            words[w[0]] = w[1]
        return words

    def parsepage(self, url=url):
        for a in self.alphabet:
            self.browser.open(url.format(1, a))
            navpages = self.browser.find(class_="navpages")
            self.pages = int(navpages.find_all('a')[-2].text)
            print(a, self.pages)
            for p in range(1, self.pages+1):
                self.browser.open(url.format(p, a))
                word_forms = self.browser.find_all(class_="termpreview")
                
                for word_tag in word_forms:
                    self.parsewords(word_tag.text)
                    
                def_forms = self.browser.find_all(class_="defnpreview")
                
                for word_tag in def_forms:
                    wrds = word_tag.text.split(";")
                    if len(wrds) < 1:
                        self.parsewords(word_tag.text)
                    for w in wrds:
                        wd = w.strip()
                        if "=" in wd:
                            wd = wd.split('=')[0]
                        self.parsewords(wd)
        return self.words

if __name__ == "__main__":
    collect = collector()
    words = collect.parsepage()
    collect.save(words)
    
    
    
