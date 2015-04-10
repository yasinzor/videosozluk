import nltk
import json
import pysrt
import MySQLdb
import sys
import re
import time

def extract(filmName):
    db = MySQLdb.connect("127.0.0.1","dizing","ynr3","dizing" )
    cursor=db.cursor()
    # add film to the database

    sql = "INSERT INTO movie(title,path) VALUES (%s,%s)"
    cursor.execute(sql, (filmName, filmName) )
    mid = cursor.lastrowid

    # get current words
    cursor.execute("SELECT wid, original, pos FROM words")
    rows = cursor.fetchall()
    words = dict()
    for row in rows:
        words[(row[1],row[2])] = row[0]

    tag_re = re.compile('<.*?>')

    from nltk.stem import WordNetLemmatizer
    wnl = WordNetLemmatizer()

    from nltk.corpus import wordnet as wn
    from nltk.stem.snowball import EnglishStemmer
    snowball_stemmer = EnglishStemmer()

    from nltk.corpus import stopwords
    stop = stopwords.words('english')
    subs = pysrt.open('filmler/%s/%s.srt' % (filmName, filmName), encoding='iso-8859-1')



    ignore = -1
    j=0
    tags=[]
    end = 0
    f = open('tmp/extract_terms.log', 'wr')

    ignoreList = []
    new_sub = None
    new_subs = []
    for (i,sub) in enumerate(subs):
      #print "Processing : %s i:%d il:%s" % (sub.text, i, ignoreList)
      text = sub.text.strip()
      text = re.sub(tag_re, '', text)

      if ignoreList == []:
          new_sub = { 'start': sub.start, 'text': "" }
      if text[-1] not in ".!?":
        ignoreList.append(i+1)
        new_sub['text'] += " " + text
        new_sub["end"] = sub.end
      else:
        new_sub["end"] = sub.end
        new_sub["text"] += " " + text
        new_subs.append(new_sub)
      if i in ignoreList:
        ignoreList.pop(0)

    frame = 5 * 1000   # 5 seconds before and after
    # for (i,sub) in enumerate(new_subs[:80]):
    for (i,sub) in enumerate(new_subs):
      # start time of scene
      try:
          j = i - 1
          start1 = sub['start']
          if j < 0:
             start = start1 - pysrt.SubRipTime(milliseconds=frame/2)
          else:
              start2 = new_subs[j]['start']
              if start1 - start2 > frame:
                 start = start1 - pysrt.SubRipTime(milliseconds=frame/2)
              else:
                while (j >= 0 and start1 - start2 < frame):
                  start = start2
                  j -= 1
                  start2 = new_subs[j]['start']

          # end time of scene
          j = i + 1
          end1 = sub['end']
          if j >= len(new_subs) - 1:
              end = end1 + pysrt.SubRipTime(milliseconds=frame/2)
          else:
              end2 = new_subs[j]['end']
              if end2 - end1 > frame:
                end = end1 + pysrt.SubRipTime(milliseconds=frame/2)
              else:
                while (j < len(new_subs) and end2 -end1 < frame):
                  end = end2
                  j += 1
                  end2 = new_subs[j]['end']
      except IndexError as e:
          print "j=%s i=%d, sub=%s" % (j, i, sub)
          raise e
      scene = { 'sentence': sub['text'], 'start': start, 'end': end }
      #print "%s time: %s" % (sub['text'],str(end - start))

      text = sub['text'].strip().lower()
      text = nltk.word_tokenize(text)
      tags = nltk.pos_tag(text)
      #print tags


      our_tags = { "NN": wn.NOUN, "JJ":wn.ADJ, "VB":wn.VERB, "RB":wn.ADV }

      sql = "INSERT INTO scene(mid,sentence,start,stop) VALUES (%s,%s,%s,%s)"
      cursor.execute(sql, (mid, sub['text'], start, end) )
      sid = cursor.lastrowid
      print "scene: %s\n" % (scene)
      f.write(str(scene)+ "\n")
      scene_words = set()
      for j in set(tags):
        base_pos = j[1][:2]
        word = j[0]
        if((word not in stop) and (base_pos in our_tags.keys()) and "'" not in word and word not in scene_words):
            scene_words.add(word)
            if ((word, base_pos) in words):
                wid = words[(word, base_pos)]
            else:
                wn_pos = our_tags[base_pos]
                stem=wnl.lemmatize(word, wn_pos)
                sql = "INSERT INTO words(original, pos, stem1, stem2) VALUES (%s,%s,%s,%s)"
                cursor.execute(sql, (word, base_pos, stem, snowball_stemmer.stem(word)))
                wid = cursor.lastrowid
                words[(word, base_pos)] = wid
            sql = "INSERT INTO words_scenes(wid, sid) VALUES (%d,%d)" % (int(wid),int(sid))
            cursor.execute(sql)

    db.commit()
    db.close()

if __name__ == "__main__":
   # print sys.argv
   try:
     extract(sys.argv[1])
   except MySQLdb.Error, e:
     print e
     print "Error %d: %s" % (e.args[0], e.args[1])
     sys.exit(1)
