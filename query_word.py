import MySQLdb
from nltk.stem.snowball import EnglishStemmer

def query(word):
    db = MySQLdb.connect("127.0.0.1","dizing","ynr3","dizing" )
    cursor=db.cursor()
    snowball_stemmer = EnglishStemmer()
    stem2 = snowball_stemmer.stem(word)
    cursor.execute("SELECT * FROM words WHERE original=%s OR stem1=%s OR stem2=%s", (word,word,stem2))
    rows = cursor.fetchall()
    words1 = dict()
    words2 = dict()
    for row in rows:
        if row[1] == word or row[3]==word:
            words1[word] = row[0]
        else:
            words2[word] = row[0]
    scenes1 = []
    scenes2 = []
    for (i,words_dict) in [(1,words1), (2,words2)]:
        wids = words_dict.values()
        for wid in wids:
            sql = "SELECT s.sentence, s.start, s.stop, s.ready, m.title FROM scene AS s, words_scenes AS ws, movie as m " + \
                           "WHERE ws.wid=%d AND ws.sid=s.sid AND s.mid = m.mid" % int(wid)
            # print sql
            cursor.execute(sql)
            rows = cursor.fetchall()
            if (i==1): scenes1 += rows
            else: scenes2 += rows
    print scenes1
    print scenes2
    return scenes1 + scenes2
    db.close()

"""
def f(k):
    import json
    l = []
    print(subs[k].start.ordinal / 1000.0)
    print(subs[k+5].end.ordinal / 1000.0)
    start0 = subs[k].start.ordinal / 1000.0
    for i in range(k,k+6):
      start = subs[i].start.ordinal / 1000.0
      end = subs[i].end.ordinal / 1000.0
      text = subs[i].text
      l.append({'start': start - start0, 'end': end - start0, 'text': text})
    return json.dumps(l)
"""
