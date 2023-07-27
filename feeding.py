import feedparser
import requests
import sqlite3

con = sqlite3.connect("feeding.db")

cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS feeds(Id integer primary key autoincrement, title, url, topic, status DEFAULT(NULL), update_time DEFAULT (CURRENT_TIMESTAMP), UNIQUE(title, url))")

con.commit()

for line in open('youtube_source.tsv'):
  topic, URL = line.strip().split("\t")
  con = sqlite3.connect("feeding.db")
  cur = con.cursor()
  raw = []
  try:
    #print(URL)
    r = requests.get(URL)
    #print(r.status_code)
    d = feedparser.parse(r.text)

    for entry in d.entries:
      url = entry.link
      title = entry.title
      raw.append( (title, url, topic))
    cur.executemany("INSERT OR IGNORE INTO feeds(title, url, topic) VALUES(?, ?, ?)", raw)
    #print(raw)
    con.commit()
  except Exception as e:
        print(e)

con.commit()

data = []
for row in cur.execute("SELECT * FROM feeds where status is NULL ORDER BY topic"):
  print(row)
  id,title,url,topic,status, update_time = row
  data.append([id])
  #call webhook and then update the status

#update status to avoid duplicate updating

cur.executemany("UPDATE feeds set status = '1' where id = ? ", data)
con.commit()
con.close()

