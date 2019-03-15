from networktest import networktest
import sqlite3

tableinit = '''
CREATE TABLE IF NOT EXISTS datas (
  "name" TEXT NOT NULL,
  "tag" TEXT,
  "type" TEXT,
  PRIMARY KEY ("name"))'''
if __name__ == '__main__':
    sq = sqlite3.connect('./db.sqlite')
    c = sq.cursor()
    c.execute(tableinit)
    # curs = c.execute('SELECT count(*) FROM datas WHERE name = :name', {'name': 'hello'})
    # print(curs.fetchone()[0])
    sq.close()
    for i in range(0, 100):
        try:
            networktest()
        except Exception as e:
            print(e)
