
# coding: utf-8

# In[12]:

fields = [ "Photo/video identifier",    #0
"User NSID",                            #1
"User nickname",                        #2
"Date taken",                           #3
"Date uploaded", 
"Capture device", 
"Title", 
"Description", 
"User tags (comma-separated)", 
"Machine tags (comma-separated)", 
"Longitude", 
"Latitude", 
"Accuracy", 
"Photo/video page URL", 
"Photo/video download URL", 
"License name", 
"License URL", 
"Photo/video server identifier", 
"Photo/video farm identifier", 
"Photo/video secret", 
"Photo/video secret original", 
"Photo/video extension original", 
"Photos/video marker (0 = photo, 1 = video)" ]


# In[55]:

cities = set(["adana" , "adiyaman" , "afyonkarahisar" , "agri" , "aksaray" , "amasya" , "ankara" ,"antalya" , "ardahan" ,
 "artvin" , "aydi" , "balikesir" , "bartin" , "batman" , "bayburt" , "bilecik" ,  "bingol" , "bitlis" , "bolu" , "burdur" , "bursa" ,
 "canakkale" ,"cankiri" , "corum" , "denizli" , "diyarbakir" , "duzce" ,  "edirne" , "elazig" , "erzincan" , "erzurum" , 
 "eskisehir" , "gaziantep" , "giresun" ,"gumushane" ,"hakkari" , "hatay" ,"igdir" , "isparta" ,"istanbul" , "izmir" , 
 "kahramanmaras" , "karabuk" , "karaman" , "kars" , "kastamonu" , "kayseri" , "kirikkale" , "kirklareli" , "kirsehir" , 
 "kilis" , "kocaeli" , "konya" ,   "kutahya" , "malatya" , "manisa" , "mardin" , "mersin" , "mugla", "mus" , 
 "nevsehir" , "nigde" , "ordu" , "osmaniye" , "rize" , "sakarya" , "samsun" , "siirt" , "sinop" , "sivas", "sanliurfa" , 
 "sirnak" , "tekirdag" , "tokat" , "trabzon" , "tunceli" , "usak" , "van" , "yalova" , "yozgat" , "zonguldak"])


# In[23]:

import sys
sys.getdefaultencoding()
print u"ışık".upper()


# In[168]:

import urllib
from unicodedata import normalize

print urllib.quote("ğüşıöç ĞÜİŞÖÇ\nabc")

line = "%C4%9F%C3%BC%C5%9F%C4%B1%C3%B6%C3%A7%20%C4%9E%C3%9C%C4%B0%C5%9E%C3%96%C3%87%0Aabc"
def tr2ascii(line):
    line = line.replace(u"ı", "i")
    line = line.replace(u"+", " ")
    line = line.replace(u"\n", "")
    return normalize("NFD", line).encode('ascii','ignore')
line = urllib.unquote(line).decode("utf-8")
print(tr2ascii(line))


# In[50]:


filename ="test-dataset"
dataset = open(filename, "r")
for i,line in enumerate(dataset): 
      # print type(line)
      line = tr2ascii(line)
      arr = line.split("\t") 
      if (arr[22] == 1): continue    # if video bypass loop 
      # for col in [0,2,6,7,8,9,13,14,17,18,19,20,21]:
      for col in [6,7,8,9]:
         key = fields[col]
         val = arr[col]
      # tags = set(arr[8].split(","))
      # m_tags = set(arr[9].split(","))
         if val: print "%s:%s" % (key,val)


# In[59]:

import pyorient
client = pyorient.OrientDB("localhost", 2424)  # host, port

# open a connection (username and password)
client.connect("root", "odb48")


# select to use that database
client.db_open("harita-deneme", "root", "odb48")



# In[66]:

stats = "{ 'asked':0, 'correct':0, 'incorrect':0, 'passed':0, '@class': 'QuizStats', '@type': 'd' }"
new_tag = { 'name': 'XYZ', 'stats': stats}
rec_pos = client.command("INSERT INTO CityTag content { 'name': 'XYZ', 'stats': %s }" % stats)


# In[90]:

# stats = { '@QuizStats': { 'asked':0, 'correct':0, 'incorrect':0, 'passed':0 } }
# new_tag = { 'name': 'XYZ2', 'stats': stats}
# rec_pos = client.record_create(14, new_tag)
rec_pos[0].oRecordData['stats']


# In[79]:

print rec_pos[0]


# In[72]:

rid1 = rec_pos[0]._rid
resp = client.command("UPDATE %s PUT alias = '%s',1" % (rid1, "XYZ"))
resp


# In[172]:

client = pyorient.OrientDB("localhost", 2424)  # host, port
client.connect("root", "odb48")
client.db_open("harita-deneme", "root", "odb48")

try:
    stats = "{ 'asked':0, 'correct':0, 'incorrect':0, 'passed':0, '@class': 'QuizStats', '@type': 'd' }"
    filename ="test-dataset"
    filename ="yfcc100m_dataset-1"
    dataset = open(filename, "r")
    city_tag_rids = dict()
    user_rids = dict()
    for i,line in enumerate(dataset): 
          if i%5000 == 0: print "i=%d" % i
          line =  urllib.unquote(line).decode("utf-8")
          line2 = tr2ascii(line)
          arr = line2.split("\t") 
          if (arr[22] == 1): continue    # if video bypass loop 
          tags = arr[8].split(",") 
          r = [(i,tag) for (i,tag) in enumerate(tags) if tag in cities]
          if r:
             uid = arr[1]
             uname = arr[2].encode('string_escape')
             title = arr[6].encode('string_escape')
             descr = arr[6].encode('string_escape')
             page_url = arr[13]
             url = arr[14]       
             cmd = u"begin;"                     
             cmd += "let img = create vertex Image content { title:'%s', descr:'%s', stats:%s, url:'%s', page_url:'%s' };" % (title,descr,stats,url,page_url) 
             user_rid = user_rids.get(uid)
             if user_rid:
                 cmd += "create edge takenBy from $img to %s;" % user_rid
             else: 
                 cmd += "let user = create vertex User content { uid: '%s', uname:'%s', stats:%s };" % (uid,uname,stats)
                 cmd += "create edge takenBy from $img to $user;"
             tags_orig = line.split("\t")[8].split(",")       
             for (i,city_tag) in r:       
                alias = tags_orig[i]      
                # print "alias=%s" % alias
                city_rid = city_tag_rids.get(city_tag)
                if city_rid:
                    cmd += "create edge hasCity from $img to %s;" % city_rid
                    # update #13:0 put alias = "abcd", if(eval('alias containskey ("abcd")'), eval('alias.abcd + 1'), 1) RETURN AFTER @this
                    cmd += "update %s put alias = '%s', if(eval('alias containskey \"%s\"'), eval('alias.%s + 1'), 1);" % (city_rid, alias, alias, alias)
                else:
                    cmd += "let city = create vertex CityTag content { 'name':'%s', 'alias': {'%s':1}, stats:%s };" %  (city_tag, alias, stats)
                    cmd += "create edge hasCity from $img to $city;"
             # cmd += "let rids = select expand(out().include('@rid', '@class')) from $img;"   
             cmd += "commit retry 5;"     
             # cmd += "let img_rid = SELECT @rid FROM $img;"       
             cmd += "return $img;"       
             # print repr(cmd.encode("utf8"))
             # print cmd.encode("utf8")       
             result = client.batch(cmd.encode("utf8"))
             # print result[0]._rid 
             # query = "select expand(out().include('@rid', '@class')) from %s" % (result[0]._rid)
             query = "select @rid as rec_id, @class as rec_type FROM (select expand(out().include('@rid', '@class')) from %s)" % (result[0]._rid)
             # print query.encode('utf8')       
             recs = client.command(query)
             for rec in recs:
                rec_dict = rec.oRecordData
                if rec_dict['rec_type'] == "User":
                    user_rids[uid] = rec_dict['rec_id']
                elif rec_dict['rec_type'] == "CityTag":
                    city_tag_rids[city_tag] = rec_dict['rec_id']
                    
             # for (i,city_tag) in r:
             #   alias = tags_orig[i]
    # print user_rids
    print city_tag_rids
finally:
    client.db_close()


# In[164]:

recs[0].oRecordData['rec_id'].get_hash()
strg = 'abc"dssd"cs\n\ncd'
strg = tr2ascii(strg)
strg = strg.encode('unicode_escape')
strg

