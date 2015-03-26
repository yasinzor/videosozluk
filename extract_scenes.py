import nltk
import json
import pysrt
import MySQLdb
import sys
import re
import time

def main(filmName):
    db = MySQLdb.connect("127.0.0.1","dizing","ynr3","dizing" )
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
          if j == len(new_subs):
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

      text = sub['text'].strip()
      text = nltk.word_tokenize(text)
      tags = nltk.pos_tag(text)
      #print tags

      cursor=db.cursor()
      our_tags = { "NN": wn.NOUN, "JJ":wn.ADJ, "VB":wn.VERB, "RB":wn.ADV }
      for j in tags:
        base_pos = j[1][:2]
        if((j[0] not in stop) and (base_pos in our_tags.keys())):
            wn_pos = our_tags[base_pos]
            stem=wnl.lemmatize(j[0], wn_pos)

            scene = { 'sentence': sub['text'], 'start': start, 'end': end, 'word':stem }
            print "scene: %s\n" % (scene)
            f.write(str(scene)+ "\n")
            print str(base_pos)+"\n"

            sql = "INSERT INTO scene(sentence, start, stop, word) VALUES (%s,%s,%s,%s)"
            sql1 = "INSERT INTO analyzed(original, pos, stem1, stem2) VALUES (%s,%s,%s,%s)"
            print sql
            print sql1
            try:
              cursor.execute(sql, (sub['text'], str(start), str(end), str(stem)) )
              cursor.execute(sql1, (j[0], str(base_pos), str(stem), str(snowball_stemmer.stem(j[0]))))
              db.commit()
              # time.sleep(0.2)
            except MySQLdb.Error, e:
                print e
                print "Error %d: %s" % (e.args[0], e.args[1])
                sys.exit(1)
                # db.rollback()

    db.close()

if __name__ == "__main__":
   # print sys.argv
   main(sys.argv[1])
