#!/usr/bin/env python3

import sqlite3


class Controller:

    def __init__(self, db_path='./words.db'):
        self.words = {}
        self.db_path = db_path
    
    def save(self, data, append=False):
        '''data: type dictionary, like : {'გამარჯობა' : 10}'''
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        if not append:
            c.execute('CREATE TABLE words (word text, occurrence real)')
        for n in data:
            print(n)
            c.execute("INSERT INTO words VALUES ('"+n+"',0)")
            #c.execute("INSERT INTO words VALUES ('"+n+"',"+str(data[n])+")")
        conn.commit()
        conn.close()

    def load(self, dbfilter=""):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT * FROM words" + dbfilter)
        dbwords = c.fetchall()
        words = {}
        for w in dbwords:
            words[w[0]] = w[1]
        return words

    def delete(self, word):
        pass
    

if __name__ == "__main__":
    pass
    
    
    
