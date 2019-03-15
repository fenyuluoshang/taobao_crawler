from networktest import networktest
import sqlite3

tableinit = '''
CREATE TABLE IF NOT EXISTS "data" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "name" TEXT,
  "tag" TEXT,
  "type" TEXT
);'''
if __name__ == '__main__':
    sq = sqlite3.connect('./db.sqlite')
    c = sq.cursor()
    c.execute(tableinit)
    sq.close()
    for i in range(0, 100):
        try:
            networktest()
        except Exception as e:
            print(e)
