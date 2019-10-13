import tensorflow as tf

import json
import demjson
import io
import codecs
import jieba
import jieba.analyse
import re
import random

json_file=open('train.json', 'a')

def store(data):

        dumps_str=json.dumps(data, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ': '))
       
        print(dumps_str)

        json_file.write(dumps_str)
  




   
filepath="/media/hadoop/娱乐/oppo_round1_train_20180929.txt"

oppo_file=open(filepath,"r")

domain={}
count=0
domain_sentence={}
chinese=set()

for line in oppo_file:
        #print(line)应用
        line_split=line.split("	")
        print(line_split[3]) 
       
        #print(line_split[2])
        if  line_split[3] not in domain:
               domain[line_split[3]]=count
               count=count+1

        if  line_split[3] not in domain_sentence:  

               domain_sentence[line_split[3]]=set([line_split[2]])

        else:
               #list_sentence=[]
               list_sentence=set()
               list_sentence=domain_sentence[line_split[3]]

               #if line_split[2]  not in list_sentence:

               list_sentence.add(line_split[2])

               domain_sentence[line_split[3]]=list_sentence
 


print(domain)
string_json=''

s_list=[]
flight_city=[]
for sentence in domain_sentence["航班"]:#可以作为槽内容
       seg_list = jieba.cut(sentence)
       sentence2=" ".join(seg_list)
     #print(sentence)
       word=sentence2.split(" ") 
       print(sentence)
       print(word[0])
       print(word[2])
       string_dic={}
       string_dic["domain"]="flight"
       string_dic["text"]=sentence.strip()
       string_dic["intent"]="QUERY"
       slot={}
       slot["endLoc_city"]=word[2].strip()
       slot["startLoc_city"]=word[0].strip()
       string_dic["slots"]=slot

 

       s_list.append(string_dic) 
       flight_city.append(word[2].strip())
       flight_city.append(word[0].strip())

cook=[]
for sentence in domain_sentence["菜谱"]:#可以作为槽内容
       #seg_list = jieba.cut(sentence)
       #sentence2=" ".join(seg_list)
       #word=sentence2.split(" ") 
       print(sentence)
       #print(word[0])
       word=sentence.replace("的做法","")
       print(word)
      # string_dic=string_dic+',{'+'domain:cookbook,text:'+sentence+',intent:QUERY,'+'slots: {dishName:'+word+'}}'
       string_dic={}
       string_dic["domain"]="cookbook"
       string_dic["text"]=sentence.strip()
       string_dic["intent"]="QUERY"
       slot={}
       slot["dishName"]=word.strip()
      # slot["startLoc_city"]=word[0].strip()
       string_dic["slots"]=slot

       s_list.append(string_dic)

       cook.append(word.strip())
       chinese.add(word.strip())

print(domain_sentence["健康"])  
for sentence in domain_sentence["健康"]:
        tags = jieba.analyse.extract_tags(sentence, topK=2)
        print(sentence)
        print(tags)
        word=''
       # string_dic=string_dic+',{'+'domain:health,text:'+sentence+',intent:QUERY,'+'slots: {keyword:'+word+'}}'
        string_dic={}
        string_dic["domain"]="health"
        string_dic["text"]=sentence.strip()
        string_dic["intent"]="QUERY"
        slot={}
    
        string_dic["slots"]=slot

      #  s_list.append(string_dic)
        
        seg=jieba.cut(sentence.strip())

        sentence_jieba=" ".join(seg)

        word_seq=sentence_jieba.split(" ")

        for word in word_seq:

              if len(word)>1:

                    chinese.add(word)

        
app_name=[]
for sentence in domain_sentence["应用"]:#可以作为槽内容
        print(sentence)
        word=sentence
        #string_dic=string_dic+',{'+'domain:app,text:'+sentence+',intent:LAUNCH,'+'slots: {keyword:'+word+'}}'
        string_dic={}
        string_dic["domain"]="app"
        string_dic["text"]=sentence.strip()
        string_dic["intent"]="LAUNCH"
        slot={}
        slot["name"]=word.strip()
      # slot["startLoc_city"]=word[0].strip()
        string_dic["slots"]=slot

       # s_list.append(string_dic)
        s=word.strip()
        if "(" in s:

            s=s[:s.index("(")]
        if "（" in s:
            s=s[:s.index("（")]

        app_name.append(s)

print(app_name)

#exit()


website=[]
for sentence in domain_sentence["网站"]:  #可以作为槽内容
        print(sentence)
        word=sentence
       # string_dic=string_dic+',{'+'domain:website,text:'+sentence+',intent:OPEN,'+'slots: {keyword:'+word+'}}'
        string_dic={}
        string_dic["domain"]="website"
        string_dic["text"]=sentence.strip()
        string_dic["intent"]="OPEN"
        slot={}
        slot["name"]=word.strip()
      # slot["startLoc_city"]=word[0].strip()
        string_dic["slots"]=slot

        s_list.append(string_dic)

        website.append(word.strip())
#exit()
video=[]
for sentence in domain_sentence["影视"]:
   if  len(sentence)<10:
        print(sentence)
        #word=sentence
        video.append(sentence.strip())
        #string_dic=string_dic+',{'+'domain:cinemas,text:'+sentence+',intent:QUERY,'+'slots: {keyword:'+word+'}}'

print("video length:",len(video))
#exit()
music=[]
for sentence in domain_sentence["音乐"]:
   if  len(sentence)<15 :
        print(sentence)
        if ("(") in sentence and sentence.index("(")>0 :
             s=sentence[0:sentence.index("(")]
             print(s)
             music.append(s.strip())             
        else:
             music.append(sentence.strip())

       # string_dic=string_dic+',{'+'domain:music,text:'+sentence+',intent:PLAY,'+'slots: {keyword:'+word+'}}'
#input()
for sentence in domain_sentence["网页"]:
        print(sentence)
        word=sentence
        #string_dic=string_dic+',{'+'domain:website,text:'+sentence+',intent:OPEN,'+'slots: {keyword:'+word+'}}'

     #   website.append(word.strip())

#input()


file_path="./train.json"
file_path_2="./人名词典.txt"
file_path_3="./全国地名大全.txt"
file_path_4="./机构名词典.txt"
file_path_5="./上海地名.txt"
file_path_6="./city.txt"

file_path_7="./xian3.txt"
file_path_8="./xian.txt"
file_path_9="./qu4.txt"

file_path_10="./stock_a.txt"

file_path_11="./tv.txt"
file_path_12="tv_game.txt"

file_path_13="./caipiao2.txt"
file_path_14="china_football.txt"

file_path_15="artist_male.txt"
file_path_16="song.txt"
file_path_17="./chinese.txt"

file_path_18="./影院.txt"
file_path_19="./movie.txt"

file_path_20="./football.txt"

file_path_21="./novel_category.txt"

file_path_22="./xiaosuo.txt"

file_path_23="./xiaosuo_author.txt"

file_path_24="./jiankang.txt"

file_path_25="./食材.txt"

file_path_26="./poetry_author.txt"

file_path_27="./名句.txt"

file_path_28="./radio.txt"
person_name=[]
address=[]
organization=[]
shanghai_address=[]

city=[]

area=[]
city_address=[]
xian_area=[]
tv_name=set()

theatre_name=set()

football_team=set()

novel_category=[]
novel_name=[]
novel_author=[]

disease=[]
ingredient=[]

poetry_author=[]
poetry_keyword=[]
poetry_author_name=[]

radio_code_name=[]

file_radio_name=open(file_path_28,"r")

for line in file_radio_name:

   if len(line)>3 and "频率" not in line:
       print(line)
       line_seq=line.split(" ")
       print(line_seq[-1].strip())
       print(line_seq[-2])

       radio_code_name.append((line_seq[-2],line_seq[-1].strip()))

print(radio_code_name)

#exit()





file_poetry_author=open(file_path_26,"r")

for line in file_poetry_author:
    if len(line.strip())>1:
        print(line)
        poetry_author.append(line.strip())

print(poetry_author)


file_keyword=open(file_path_27,"r")

for line in file_keyword:

        print(line)
        if "，"  in line:
             print(line)
             line_seq=line.split("，")
             print(line_seq[0])
             poetry_keyword.append(line_seq[0].strip())

        if "《"  in line:

             pattern = re.compile("(?<=《)[^》]+(?=》)")

             result=pattern.findall(line)
             poerty=""
             for r in result:

                  print(r)
                  poerty=r
             line=line[:line.index("《")]
             if len(line.strip())>1:
                  poetry_author_name.append((line,poerty))


print(poetry_keyword)
print(poetry_author_name)

#exit()

ingredient_file=open(file_path_25,"r")

for line in  ingredient_file:
      if len(line)>15:
            line_seq=line.split(" ")
            for seq in line_seq:
               # print(seq)
                if len(seq.strip())>1 and "更多"  not in seq:
                    length=len(seq)
                    seq=seq[:int(length/2)]
                    print(seq)
                    ingredient.append(seq)
#exit()


disease_author_file=open(file_path_24,"r")



for line in disease_author_file:
     if len(line.strip())>2:
         line=line.strip()
         line=line.replace("·","")
         print(line)
         disease.append(line)

print(disease)

for sentence in domain_sentence["健康"]:
     for illness in disease:
             if illness in sentence:

                     string_dic={}
                     string_dic["domain"]="health"
                     string_dic["text"]=sentence.strip()
                     string_dic["intent"]="QUERY"
                     slot={}
                     slot["keyword"]=illness
                     string_dic["slots"]=slot

                     s_list.append(string_dic)

                     print(sentence)
                     print(illness)
#exit()




novel_author_file=open(file_path_23,"r")

for line in novel_author_file:
    if len(line.strip())>1:

         print(line)
         novel_author.append(line.strip())

print(novel_author)

#exit()

novel_name_file=open(file_path_22,"r")
for line in  novel_name_file:
     if  "简介" not in line and "2" not in line and "3" not in line and "4" not in line and "5" not in line and "1" not in line and "6" not in line and "7" not in line and "8" not in line and "9" not in line:
        print(line)
        if len(line.strip())>1:
             novel_name.append(line.strip())

print(novel_name)

#exit()



novel_category_file=open(file_path_21,"r")

for line in novel_category_file:
     if len(line)>5:
           line=line.replace("。","")
           line_seq=line.split("，")
           for seq in line_seq:
                 seq=seq.replace("小说","")
                
                 novel_category.append(seq.strip())

print(novel_category)
#exit()


lottery=[]

lottery_file_name=open(file_path_13,"r")

for line in lottery_file_name:
    if len(line)>3:

      print(line)
      lottery.append(line.strip())

print(lottery)

#exit()




football_file_name=open(file_path_20,"r")

for line in  football_file_name:
       #print(line)
       if "足球俱乐部" in line:
          line=line[:line.index("足球")]
         # print(line)
          if len(line.strip())>2:
               football_team.add(line.strip())
       else:
          if len(line.strip())>2:
               football_team.add(line.strip())

print(football_team)
#exit()


move_file_name=open(file_path_19,"r")

pattern = re.compile('《[\u4e00-\u9fa5]+》')  

cinemas_movie=set()

for line in move_file_name:
       
       #print(line)
       result=pattern.findall(line)
      # print(result)
       if len(result)>=1:
           for r in result:
                print(r)
                r=r.replace("《","").replace("》","")
                cinemas_movie.add(r)
print(cinemas_movie)

#exit()


theatre_file_name=open(file_path_18,"r")

for line in theatre_file_name:
    if "影城" in line or '影院' in line :
      if  '公司' not in line and '名单' not in line and '名称' not in line:
       
        line_seq=line.split(" ")

        for seq in line_seq:

            if "影城" in seq or '影院' in seq:

                   seq=seq.replace('(','')
                   seq=seq.replace(')','') 

                   seq=seq.replace('-','')
                   if len(seq.strip())>3:         
                         print(seq)
                         theatre_name.add(seq.strip())

print(theatre_name)

#exit()

movie_category=['动作','冒险','喜剧','爱情','战争','恐怖','犯罪','悬疑','惊悚','武侠','科幻','音乐','动画','奇幻','家庭','剧情','伦理','记录','历史','青春','励志']



location_country=["朝鲜","韩国","日本","俄罗斯","美国","英国","意大利","伊朗","德国","越南","西班牙","葡萄牙","加拿大","冰岛","澳大利亚","泰国","法国","委内瑞拉","巴西","古巴"]

tv_file_name=open(file_path_11,"r")

for line in tv_file_name:

     line=line.strip()

     if len(line)>3 and '广告' not in line and '插播' not in line and '特殊' not in line  and '电视局' not in line  and '事业局' not in line   and '电视中心' not in line  and "制片厂" not in line and "卫星" not in line and "联播" not in line:
       if '服务中心' not in line  and '栏目'  not in line and '其它' not in line and "套播" not in line and "赞助" not in line and "新闻中心" not in line:
         if "·" in line and "节目" not in line and '标版' not in line and '套餐' not in line and '广播电视新闻' not in line and '集团' not in line and '七彩' not in line and '切播' not in line and '商业性'  not in line and "电视业务" not in line and '“' not in line:
           line=line.replace("12345简介 刊例 折扣 联系","")
           line=line.replace("特别广","")
           line=line.replace("精品","")
           if "频道"  in line:
               line=line[:line.index("频道")+2]
           if "（"  in line:
               line=line[:line.index("（")]

           if "《"  in line:
               line=line[:line.index("《")]

           if "、"  in line:
               line=line[:line.index("、")]
           if "电视剧"  in line:
               line=line[:line.index("电视剧")]

           if "剧场"  in line:
               line=line[:line.index("剧场")]

           if "特约播映"  in line:
               line=line[:line.index("特约播映")]

           if "金曲放送"  in line:
               line=line[:line.index("金曲放送")]

           if "江苏卫视"  in line:
               line=line[line.index("江苏卫视"):line.index("江苏卫视")+4]
           if line[-1]=="频":
               line=line+"道"

           line=line.replace("·","")
           line=line.strip()
           print(line)
           tv_name.add(line)


#exit()


file_chinese_name=open(file_path_17,"r")

for line in file_chinese_name:

     if len(line)>1:
           line_seq=[]
           line=line.replace("。","")
           line=line.replace("！","")
           line=line.replace("？","")
           line=line.strip()
          # print(line)
           if "、"  in line:
                line_seq=line[line.index("、")+1:].split("，")
               # print(line_seq)
           else:
                line_seq=line.split("，")
           for seq in line_seq:

                print(seq)
                chinese.add(seq)
                 




print(chinese)
#exit()

file_person_name=open(file_path_2,"r")

for  line  in file_person_name:

     line_seq=line.split(" ")
     person_name.append(line_seq[0].strip())


for name in   person_name:

     if "—" in name:


        person_name.remove(name)




file_address_name=open(file_path_3,"r")

for  line  in file_address_name:

     line_seq=line.split(" ")

     if "路" in line_seq and line_seq.count("路")==1:
           address.append(line_seq[0].strip())
     else:
           if "路"  not in line_seq:
                 address.append(line_seq[0].strip())

print(address)
#input()

file_organization_name=open(file_path_4,"r")

for  line  in file_organization_name:

     line_seq=line.split(" ")
     organization.append(line_seq[0].strip())

print(organization)

#input()

file_shanghai_name=open(file_path_5,"r")

for  line  in file_shanghai_name:

     line_seq=line.split(" ")

     if "路" in line_seq and line_seq.count("路")==1:

           shanghai_address.append(line_seq[0].strip())

     else:
           if "路"  not in line_seq:

                   shanghai_address.append(line_seq[0].strip())

print(shanghai_address)
#input()

file_city_name=open(file_path_6,"r")

for  line  in file_city_name:

  if len(line)>4 and "——" in line:

     line_seq=line.split("——")
     print(line_seq[-1])

     seq=line_seq[-1]
     city_seq=seq.split("、")

     for city in city_seq:
            print(city)

            city_address.append(city.strip())


print(city_address)
print("city")
#input()

file_xiancity_name=open(file_path_7,"r")

for  line  in file_xiancity_name:
        xian_seq=line.split("	")
        for xian in xian_seq:
           if ("县" in xian) and ("下辖" not in xian) and ("（" not in xian):
                
                xian_area.append(xian.strip())
file_xiancity_name=open(file_path_8,"r")

for  line  in file_xiancity_name:
        xian_seq=line.split(" 	")
        for xian in xian_seq:
           if ( len(xian.strip() )>=5) and ("TOP" not in xian)  and (":" not in xian) :
              if ("省") in xian:
                   area=xian[xian.index("省")+1:].strip()
                   xian_area.append(area)
              else:
                   if xian.index("市",4)>0:
                       area=xian[xian.index("市")+1:].strip()
                       #xian_area.append(area)
                       if len(area)>2:
                            xian_area.append(area)
                   else:
                       area=xian[2:].strip()
                       if len(area)>2:
                            xian_area.append(area)

file_qu_name=open(file_path_9,"r")

for  line  in file_qu_name:
        #print(line)
        qu_seq=line.split("	")
        #for xian in qu_seq:
        #print(qu_seq)
        if len(qu_seq)>1:
            print(qu_seq[1])
            for qu in qu_seq[1].split("、"):
                      xian_area.append(qu.strip())

file_stock_name=open(file_path_10,"r")


stock=[]
for line in file_stock_name:

    stock_seq=line.split(" 	")

    if len(stock_seq)>1 and len(stock_seq[1].strip())>1:
      
        print(stock_seq[1])
        stock.append(stock_seq[1].strip())


file_song_name=open(file_path_16,"r")


for line in file_song_name:

      if "-" in line and "." in line:

            song_seq=line.split("-")
            print(song_seq[0])
            index=(song_seq[0]).index(".")
            s=song_seq[0][index:]
            s=s.replace("。","")

            music.append(s.replace(" ",""))



file_artist_name=open(file_path_15,"r")

artist=[]
for line in file_artist_name:

    title=re.finditer(r'html">\S+</a',line) 

    for ti in title:

       t=str(ti.group())
       t=t.replace('html">',"")
       t=t.replace('</a',"")
       print(t)

       if len(t)>1:
           artist.append(t)
     

print(artist)
#input()
print(xian_area)
#input()

for m in music:
   if "\xa0" in m:
     

       #index=m.index("\xa0")
       music.remove(m)



count=50 
video_count=50
music_count=50
football_count=50
lottery_count=50

city_count=50
novel_count=50

app_count=50
radio_count=50

map_count=50
website_count=50
cook_count=50

datetime_date=['今天','明天','后天']
datetime_time=['下午','上午','中午','晚上']
tv_category=['电影','电视剧','纪录片']
riddle_category=["搞笑谜语","字谜","成语谜语","动物谜语","爱情谜语","灯谜","人名谜语","地名谜语","词语谜语","带格谜语","用语谜语","儿童谜语","物品谜语","植物谜语","诗词谜语","书报谜语","俗语谜语","药品谜语","音乐谜语","影视谜语","称谓谜语","趣味谜语"]

with open(file_path, 'r') as f:
        data_list = json.load(f)


        for data in data_list:
             domain_value = data['domain']
             intent_value = data['intent']

             text_value=data['text']

             slots = data['slots']

             print(slots)

             string_dic={}
             string_dic["domain"]=domain_value
             string_dic["text"]=text_value.strip()
             string_dic["intent"]=intent_value
             #slot={}

             string_dic["slots"]=slots

             s_list.append(string_dic)

            
             if domain_value=="telephone":
                 if type(slots) != dict :
                  # slots = {}
                   #string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {}}'


                   string_dic={}
                   string_dic["domain"]=domain_value
                   string_dic["text"]=text_value.strip()
                   string_dic["intent"]=intent_value
                   slot={}

                   string_dic["slots"]=slot

                   s_list.append(string_dic)


                 else:

                    if 'name'  in slots:
                       word=slots['name']
                       #string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {name:'+word+'}}'

                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                       slot={}
                       slot["name"]=word
                       string_dic["slots"]=slot

                       s_list.append(string_dic)

                       for n in range(count):

                             w=random.choice (person_name )
                             sentence=text_value.replace(word,w)
                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                           #  slot={}
                            # slot["name"]=w
                           #  

                             slot={}
                             for k in slots:

                                if k=='name':

                                      slot["name"]=w
                                else:
                                      slot[k]=slots[k]

                             string_dic["slots"]=slot

                             s_list.append(string_dic)



                    else:
                
                      # string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {}}'
                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                       slot={}

                       string_dic["slots"]=slot

                       s_list.append(string_dic)

             if domain_value=="map":
                 if type(slots) != dict :
                     #slots = {}
                    # string_dic=string_dic+',{'+'domain:map,text:'+text_value+',intent:'+intent_value+',slots: {}}'

                     string_dic={}
                     string_dic["domain"]=domain_value
                     string_dic["text"]=text_value.strip()
                     string_dic["intent"]=intent_value
                     #slot={}

                     string_dic["slots"]=slots

                     s_list.append(string_dic)

                 else:
                     #s="{"
                     #for key in slots:
                      #    s=s+key+':'+slots[key]+","

                     #s=s+"}"

                    # string_dic=string_dic+',{'+'domain:map,text:'+text_value+',intent:'+intent_value+',slots:'+s+'}'

                     string_dic={}
                     string_dic["domain"]=domain_value
                     string_dic["text"]=text_value.strip()
                     string_dic["intent"]=intent_value
                    # slot={}

                     string_dic["slots"]=slots

                     s_list.append(string_dic)
                     

                    # if len(slots)==1:

                     if "location_poi"   in slots:
                         word=slots['location_poi']

                         for n in range(map_count):

                             w=random.choice (address)


                             sentence=text_value.replace(word,w)


                             string_dic={}
                             string_dic["domain"]="map"
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value


                             slot={}
                             for k in slots:

                                if k=='location_poi':

                                      slot["location_poi"]=w
                                else:
                                      slot[k]=slots[k]

                             string_dic["slots"]=slot

                             s_list.append(string_dic)


                         for n in range(map_count):

                             w=random.choice (organization)


                             sentence=text_value.replace(word,w)

                             string_dic={}
                             string_dic["domain"]="map"
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value

                             slot={}
                             for k in slots:

                                if k=='location_poi':

                                      slot["location_poi"]=w
                                else:
                                      slot[k]=slots[k]

                             string_dic["slots"]=slot

                             s_list.append(string_dic)


                     if "location_city"   in slots:
                         word=slots['location_city']

                         for n in range(count):

                             w=random.choice (city_address)


                             sentence=text_value.replace(word,w)

                          #   string_dic=string_dic+',{'+'domain:map,text:'+sentence+',intent:'+intent_value+',slots: {location_city:'+w+'}}'

                             string_dic={}
                             string_dic["domain"]="map"
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value

                             slot={}

                             for k in slots:

                                if k=='location_city':

                                      slot["location_city"]=w
                                else:
                                      slot[k]=slots[k]

                             string_dic["slots"]=slot

                             s_list.append(string_dic)


                     if "endLoc_poi"   in slots and len(slots)==1:
                         word=slots['endLoc_poi']

                         for n in range(map_count):

                             w=random.choice (shanghai_address)


                             sentence=text_value.replace(word,w)

                             string_dic={}
                             string_dic["domain"]="map"
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value

                             slot={}

                             for k in slots:

                                if k=='endLoc_poi':

                                      slot["endLoc_poi"]=w
                                else:
                                      slot[k]=slots[k]

                             string_dic["slots"]=slot

                             s_list.append(string_dic)



                     if "location_area"   in slots:
                         word=slots['location_area']

                         for n in range(count):

                             w=random.choice (xian_area)


                             sentence=text_value.replace(word,w)

                             string_dic={}
                             string_dic["domain"]="map"
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value


                             slot={}

                             for k in slots:

                                if k=='location_area':

                                      slot["location_area"]=w
                                else:
                                      slot[k]=slots[k]

                             string_dic["slots"]=slot

                             s_list.append(string_dic)


                          #   s_list.append(string_dic)


             if domain_value=="website":
                 if type(slots) != dict :
                     #slots = {}
                    # string_dic=string_dic+',{'+'domain:map,text:'+text_value+',intent:'+intent_value+',slots: {}}'

                     string_dic={}
                     string_dic["domain"]=domain_value
                     string_dic["text"]=text_value.strip()
                     string_dic["intent"]=intent_value
                     #slot={}

                     string_dic["slots"]=slots

                     s_list.append(string_dic)

                 else:

                    if 'name'  in slots:
                       word=slots['name']
                       #string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {name:'+word+'}}'

                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                       slot={}
                       slot["name"]=word
                       string_dic["slots"]=slot

                       s_list.append(string_dic)

                       for n in range(website_count):

                             w=random.choice (website )
                             sentence=text_value.replace(word,w)
                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]="website"
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             slot["name"]=w
                             string_dic["slots"]=slot
                             s_list.append(string_dic)




             if domain_value=="cookbook":
                 if type(slots) != dict :


                     string_dic={}
                     string_dic["domain"]=domain_value
                     string_dic["text"]=text_value.strip()
                     string_dic["intent"]=intent_value
                     #slot={}

                     string_dic["slots"]=slots

                     s_list.append(string_dic)

                 else:

                    if 'dishName'  in slots and len(slots)==1:
                       word=slots['dishName']
                       #string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {name:'+word+'}}'

                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                      # slot={}
                      # slot["dishName"]=word
                       string_dic["slots"]=slots

                       s_list.append(string_dic)

                       for n in range(cook_count):

                             w=random.choice (cook )
                             sentence=text_value.replace(word,w)
                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             slot["dishName"]=w
                             string_dic["slots"]=slot
                             s_list.append(string_dic)

                    if 'ingredient'  in slots and len(slots)==1:
                       word=slots['ingredient']
                       #string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {name:'+word+'}}'

                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                      # slot={}
                      # slot["dishName"]=word
                       string_dic["slots"]=slots

                       s_list.append(string_dic)

                       for n in range(cook_count):

                             w=random.choice (ingredient )
                             sentence=text_value.replace(word,w)
                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             slot["dishName"]=w
                             string_dic["slots"]=slot
                             s_list.append(string_dic)

             if domain_value=="video":
                 if type(slots) != dict :
                     #slots = {}
                    # string_dic=string_dic+',{'+'domain:map,text:'+text_value+',intent:'+intent_value+',slots: {}}'

                     string_dic={}
                     string_dic["domain"]=domain_value
                     string_dic["text"]=text_value.strip()
                     string_dic["intent"]=intent_value
                     #slot={}

                     string_dic["slots"]=slots

                     s_list.append(string_dic)

                 else:

                    if 'name'  in slots and len(slots)==1:
                       word=slots['name']
                       #string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {name:'+word+'}}'

                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                       slot={}
                       slot["name"]=word
                       string_dic["slots"]=slot

                       s_list.append(string_dic)

                       for n in range(video_count):

                             w=random.choice (video )
                             sentence=text_value.replace(word,w)
                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             slot["name"]=w
                             string_dic["slots"]=slot
                             s_list.append(string_dic)


             if domain_value=="stock":
                 if type(slots) != dict :
                     #slots = {}
                    # string_dic=string_dic+',{'+'domain:map,text:'+text_value+',intent:'+intent_value+',slots: {}}'

                     string_dic={}
                     string_dic["domain"]=domain_value
                     string_dic["text"]=text_value.strip()
                     string_dic["intent"]=intent_value
                     #slot={}

                     string_dic["slots"]=slots

                     s_list.append(string_dic)

                 else:

                    if 'name'  in slots and len(slots)==1:
                       word=slots['name']
                       #string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {name:'+word+'}}'

                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                       slot={}
                       slot["name"]=word
                       string_dic["slots"]=slot

                       s_list.append(string_dic)

                       for n in range(count):

                             w=random.choice (stock )
                             sentence=text_value.replace(word,w)
                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             slot["name"]=w
                             string_dic["slots"]=slot
                             s_list.append(string_dic)


             if domain_value=="message":
                 if type(slots) != dict :


                     string_dic={}
                     string_dic["domain"]=domain_value
                     string_dic["text"]=text_value.strip()
                     string_dic["intent"]=intent_value
                     #slot={}

                     string_dic["slots"]=slots

                     s_list.append(string_dic)

                 else:

                    if 'name'  in slots  and len(slots)==1:
                       word=slots['name']
 
                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                       slot={}
                       slot["name"]=word
                       string_dic["slots"]=slot

                       s_list.append(string_dic)

                       for n in range(count):

                             w=random.choice (person_name )
                             sentence=text_value.replace(word,w)
                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             slot["name"]=w
                             string_dic["slots"]=slot
                             s_list.append(string_dic)

                    if 'name'  in slots  and len(slots)==2 and 'receiver'  in slots:
                       word=slots['name']
                       word2=slots['receiver']
                       #string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {name:'+word+'}}'

                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                       #slot={}
                       #slot["name"]=word
                       string_dic["slots"]=slots

                       s_list.append(string_dic)

                       for n in range(count):

                           #  w1=random.choice (person_name )
                            # w2=random.choice (person_name )
                          w1,w2=random.sample(person_name , 2)
                          if w1 not in text_value and w2 not in text_value:
                             sentence=text_value.replace(word,w1)

                             sentence=sentence.replace(word2,w2)

                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             slot["name"]=w1
                             slot["receiver"]=w2
                             string_dic["slots"]=slot
                             s_list.append(string_dic)




             if domain_value=="contacts":
                 if type(slots) != dict :
                     #slots = {}
                    # string_dic=string_dic+',{'+'domain:map,text:'+text_value+',intent:'+intent_value+',slots: {}}'

                     string_dic={}
                     string_dic["domain"]=domain_value
                     string_dic["text"]=text_value.strip()
                     string_dic["intent"]=intent_value
                     #slot={}

                     string_dic["slots"]=slots

                     s_list.append(string_dic)

                 else:

                    if 'name'  in slots  and len(slots)==1:
                       word=slots['name']
                       #string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {name:'+word+'}}'

                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                       slot={}
                       slot["name"]=word
                       string_dic["slots"]=slot

                       s_list.append(string_dic)

                       for n in range(count):

                             w=random.choice (person_name )
                             sentence=text_value.replace(word,w)
                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             slot["name"]=w
                             string_dic["slots"]=slot
                             s_list.append(string_dic)


             if domain_value=="email":
                 if type(slots) != dict :
                     #slots = {}
                    # string_dic=string_dic+',{'+'domain:map,text:'+text_value+',intent:'+intent_value+',slots: {}}'

                     string_dic={}
                     string_dic["domain"]=domain_value
                     string_dic["text"]=text_value.strip()
                     string_dic["intent"]=intent_value
                     #slot={}

                     string_dic["slots"]=slots

                     s_list.append(string_dic)

                 else:

                    if 'name'  in slots  and len(slots)==1:
                       word=slots['name']
                       #string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {name:'+word+'}}'

                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                       slot={}
                       slot["name"]=word
                       string_dic["slots"]=slot

                       s_list.append(string_dic)

                       for n in range(count):

                             w=random.choice (person_name )
                             sentence=text_value.replace(word,w)
                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             slot["name"]=w
                             string_dic["slots"]=slot
                             s_list.append(string_dic)


             if domain_value=="bus":
                 if type(slots) != dict :
                     #slots = {}
                    # string_dic=string_dic+',{'+'domain:map,text:'+text_value+',intent:'+intent_value+',slots: {}}'

                     string_dic={}
                     string_dic["domain"]=domain_value
                     string_dic["text"]=text_value.strip()
                     string_dic["intent"]=intent_value
                     #slot={}

                     string_dic["slots"]=slots

                     s_list.append(string_dic)

                 else:

                    if 'Dest'  in slots  and len(slots)==1:
                       word=slots['Dest']
                       #string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {name:'+word+'}}'

                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                      # slot={}
                       #slot["Dest"]=word
                       string_dic["slots"]=slots

                       s_list.append(string_dic)

                       for n in range(count):

                          w=random.choice (xian_area )
                          if w not in text_value:
                             sentence=text_value.replace(word,w)
                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             slot["Dest"]=w
                             string_dic["slots"]=slot
                             s_list.append(string_dic)

                    if 'Dest'  in slots  and 'Src' in slots:
                       word1=slots['Dest']
                       word2=slots['Src']
                       #string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {name:'+word+'}}'

                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                      # slot={}
                       #slot["Dest"]=word
                       string_dic["slots"]=slots

                       s_list.append(string_dic)

                       for n in range(count):

                           #  w=random.choice (xian_area )
                          #   sentence=text_value.replace(word,w)


                          w1,w2=random.sample(xian_area , 2)

                          if w1 not in text_value and w2 not in text_value:

                             sentence=text_value.replace(word1,w1)

                             sentence=sentence.replace(word2,w2)

                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             slot["Dest"]=w1
                             slot["Src"]=w2
                             string_dic["slots"]=slot
                             s_list.append(string_dic)

#############################################

             if domain_value=="flight":
                 if type(slots) != dict :
                     #slots = {}
                    # string_dic=string_dic+',{'+'domain:map,text:'+text_value+',intent:'+intent_value+',slots: {}}'

                     string_dic={}
                     string_dic["domain"]=domain_value
                     string_dic["text"]=text_value.strip()
                     string_dic["intent"]=intent_value
                     #slot={}

                     string_dic["slots"]=slots

                     s_list.append(string_dic)

                 else:

                    if 'endLoc_city'  in slots  and len(slots)==1:
                       word=slots['endLoc_city']
                       #string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {name:'+word+'}}'

                       string_dic={}
                       string_dic["domain"]="flight"
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                       #slot={}
                       #slot["endLoc_city"]=word
                       string_dic["slots"]=slots

                       s_list.append(string_dic)

                       for n in range(count):

                             w=random.choice (flight_city )
                             sentence=text_value.replace(word,w)
                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             slot["endLoc_city"]=w
                             string_dic["slots"]=slot
                             s_list.append(string_dic)

                    if 'endLoc_city'  in slots  and  "startLoc_city" in slots and  len(slots)==2:
                       word1=slots['endLoc_city']
                       word2=slots['startLoc_city']
                       #string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {name:'+word+'}}'

                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                      # slot={}
                       #slot["endLoc_city"]=word
                       string_dic["slots"]=slots

                       s_list.append(string_dic)

                       for n in range(count):

                          w1,w2=random.sample(flight_city  , 2)
                            
                          if w1 not in text_value and w2 not in text_value :

                             sentence=text_value.replace(word1,w1)

                             sentence=sentence.replace(word2,w2)

                             print("w1:",w1)

                             print("w2:",w2)
                             print("word1:",word1)
                             print("word2:",word2)

                             print(sentence)


                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             slot["endLoc_city"]=w1
                             slot["startLoc_city"]=w2
                             string_dic["slots"]=slot
                             s_list.append(string_dic)
                             print(slot)
                             #input()

             if domain_value=="music":
                 if type(slots) != dict :
                     #slots = {}
                    # string_dic=string_dic+',{'+'domain:map,text:'+text_value+',intent:'+intent_value+',slots: {}}'

                     string_dic={}
                     string_dic["domain"]=domain_value
                     string_dic["text"]=text_value.strip()
                     string_dic["intent"]=intent_value
                     #slot={}

                     string_dic["slots"]=slots

                     s_list.append(string_dic)

                 else:

                    if 'song'  in slots  and len(slots)==1:
                       word=slots['song']
                       #string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {name:'+word+'}}'

                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                       slot={}
                       slot["song"]=word
                       string_dic["slots"]=slot

                       s_list.append(string_dic)

                       for n in range(music_count):

                             w=random.choice (music )
                             sentence=text_value.replace(word,w)
                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             slot["song"]=w
                             string_dic["slots"]=slot
                             s_list.append(string_dic)



                    if 'artist'  in slots  and len(slots)==1:
                       word=slots['artist']
                       #string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {name:'+word+'}}'

                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                       slot={}
                       slot["artist"]=word
                       string_dic["slots"]=slot

                       s_list.append(string_dic)

                       for n in range(music_count):

                             w=random.choice (artist )
                             sentence=text_value.replace(word,w)
                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]="music"
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             slot["artist"]=w
                             string_dic["slots"]=slot
                             s_list.append(string_dic)

                    if 'artist'  in slots and  'song'  in slots  and len(slots)==2:
                       song_slots=slots['song']
                       artist_slots=slots['artist']

                       #string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {name:'+word+'}}'

                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                      # slot={}
                     #  slot["artist"]=word
                       string_dic["slots"]=slots

                       s_list.append(string_dic)

                       for n in range(music_count):

                             w1=random.choice (artist )

                             w2=random.choice (music)
                             sentence=text_value.replace(song_slots,w2)
                             sentence=sentence.replace(artist_slots,w1)

                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]="music"
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             slot["artist"]=w1
                             slot["song"]=w2
                             string_dic["slots"]=slot
                             s_list.append(string_dic)


             if domain_value=="translation":
                 if type(slots) != dict :
                     #slots = {}
                    # string_dic=string_dic+',{'+'domain:map,text:'+text_value+',intent:'+intent_value+',slots: {}}'

                     string_dic={}
                     string_dic["domain"]=domain_value
                     string_dic["text"]=text_value.strip()
                     string_dic["intent"]=intent_value
                     #slot={}

                     string_dic["slots"]=slots

                     s_list.append(string_dic)

                 else:

                    if 'content'  in slots  and len(slots)==1:

                       word=slots['content']
                 
                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                       #slot={}
                       #slot["artist"]=word
                       string_dic["slots"]=slots

                       s_list.append(string_dic)
                       chinese_list=list(chinese)
                       for n in range(count):

                             w=random.choice (chinese_list )
                             sentence=text_value.replace(word,w)
                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             slot["content"]=w
                             string_dic["slots"]=slot
                             s_list.append(string_dic)

                    if 'content'  in slots  and 'target' in slots:

                       word=slots['content']
                       word2=slots['target']
                 
                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                       #slot={}
                       #slot["artist"]=word
                       string_dic["slots"]=slots

                       s_list.append(string_dic)
                       chinese_list=list(chinese)

                       for n in range(count):

                          if w not in text_value:

                             w=random.choice (chinese_list )
                             sentence=text_value.replace(word,w)
                        

                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             slot["content"]=w
                             slot["target"]=word2
                             string_dic["slots"]=slot
                             s_list.append(string_dic)



             if domain_value=="weather":
                 if type(slots) != dict :
                     #slots = {}
                    # string_dic=string_dic+',{'+'domain:map,text:'+text_value+',intent:'+intent_value+',slots: {}}'

                     string_dic={}
                     string_dic["domain"]=domain_value
                     string_dic["text"]=text_value.strip()
                     string_dic["intent"]=intent_value
                     #slot={}

                     string_dic["slots"]=slots

                     s_list.append(string_dic)

                 else:

                    if 'location_city'  in slots  :

                       word=slots['location_city']
                       #string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {name:'+word+'}}'

                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                       slot={}
                       slot["location_city"]=word
                       string_dic["slots"]=slots

                       s_list.append(string_dic)

                       for n in range(count):

                             w=random.choice (city_address )
                             sentence=text_value.replace(word,w)
                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             for k in slots:

                                if k=='location_city':

                                      slot["location_city"]=w
                                else:
                                      slot[k]=slots[k]

                             string_dic["slots"]=slot
                             s_list.append(string_dic)




             if domain_value=="tvchannel":
                 if type(slots) != dict :
                     #slots = {}
                    # string_dic=string_dic+',{'+'domain:map,text:'+text_value+',intent:'+intent_value+',slots: {}}'

                     string_dic={}
                     string_dic["domain"]=domain_value
                     string_dic["text"]=text_value.strip()
                     string_dic["intent"]=intent_value
                     #slot={}

                     string_dic["slots"]=slots

                     s_list.append(string_dic)

                 else:

                    if 'name'  in slots  :

                       word=slots['name']
                       #string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {name:'+word+'}}'

                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                      # slot={}
                      # slot["location_city"]=word
                       string_dic["slots"]=slots

                       s_list.append(string_dic)

                       tv_name_list=list(tv_name)

                       for n in range(count):

                             w=random.choice (tv_name_list )
                             sentence=text_value.replace(word,w)
                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             for k in slots:

                                if k=='name':

                                      slot["name"]=w
                                else:
                                      slot[k]=slots[k]

                             string_dic["slots"]=slot
                             s_list.append(string_dic)
#epg

             if domain_value=="epg":
                 if type(slots) != dict :
                     #slots = {}
                    # string_dic=string_dic+',{'+'domain:map,text:'+text_value+',intent:'+intent_value+',slots: {}}'

                     string_dic={}
                     string_dic["domain"]=domain_value
                     string_dic["text"]=text_value.strip()
                     string_dic["intent"]=intent_value
                     #slot={}

                     string_dic["slots"]=slots

                     s_list.append(string_dic)

                 else:

                    if 'tvchannel'  in slots  :

                       word=slots['tvchannel']
                       #string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {name:'+word+'}}'

                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                      # slot={}
                      # slot["location_city"]=word
                       string_dic["slots"]=slots

                       s_list.append(string_dic)

                       tv_name_list=list(tv_name)

                       for n in range(count):

                             w=random.choice (tv_name_list )
                             sentence=text_value.replace(word,w)
                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             for k in slots:

                                if k=='tvchannel':

                                      slot["tvchannel"]=w
                                else:
                                      slot[k]=slots[k]

                             string_dic["slots"]=slot
                             s_list.append(string_dic)


             if domain_value=="train":
                 if type(slots) != dict :
                     #slots = {}
                    # string_dic=string_dic+',{'+'domain:map,text:'+text_value+',intent:'+intent_value+',slots: {}}'

                     string_dic={}
                     string_dic["domain"]=domain_value
                     string_dic["text"]=text_value.strip()
                     string_dic["intent"]=intent_value
                     #slot={}

                     string_dic["slots"]=slots

                     s_list.append(string_dic)

                 else:

                    if 'endLoc_city'  in slots  and 'startLoc_city' in slots and len(slots)==2:

                       word1=slots['endLoc_city']
                       word2=slots['startLoc_city']

                       #string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {name:'+word+'}}'

                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                      # slot={}
                      # slot["location_city"]=word
                       string_dic["slots"]=slots

                       s_list.append(string_dic)

                      # tv_name_list=list(tv_name)

                       for n in range(count):

                             #w=random.choice (xian_area )

                         w1,w2=random.sample(xian_area  , 2)

                         if (w1 not in word1) and (w1 not in word2) and (w2 not in word2) and (w2 not in word2) and (word1 not in w1) and (word1 not in w2)  and (word2 not in w1) and (word2 not in w2) and (w1!=w2):

                             sentence=text_value.replace(word1,w1).replace(word2,w2)

                           #if w2_area not in sentence:

                             #sentence=sentence

                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             for k in slots:

                                if k=='endLoc_city':

                                      slot["endLoc_city"]=w1
                                else:
                                      if k=='startLoc_city':

                                            slot["startLoc_city"]=w2
                                      else:

                                             slot[k]=slots[k]

                             string_dic["slots"]=slot
                             s_list.append(string_dic)


             if domain_value=="cinemas":
                 if type(slots) != dict :
                     #slots = {}
                    # string_dic=string_dic+',{'+'domain:map,text:'+text_value+',intent:'+intent_value+',slots: {}}'

                     string_dic={}
                     string_dic["domain"]=domain_value
                     string_dic["text"]=text_value.strip()
                     string_dic["intent"]=intent_value
                     #slot={}

                     string_dic["slots"]=slots

                     s_list.append(string_dic)

                 else:

                    if 'theatre'  in slots  :

                       word=slots['theatre']
                       #string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {name:'+word+'}}'

                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                      # slot={}
                      # slot["location_city"]=word
                       string_dic["slots"]=slots

                       s_list.append(string_dic)

                       theatre_name_list=list(theatre_name)

                       for n in range(count):

                             w=random.choice (theatre_name_list )
                             sentence=text_value.replace(word,w)
                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             for k in slots:

                                if k=='theatre':

                                      slot["theatre"]=w
                                else:
                                      slot[k]=slots[k]

                             string_dic["slots"]=slot
                             s_list.append(string_dic)


                    if 'name'  in slots  :

                       word=slots['name']
                       #string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {name:'+word+'}}'

                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                      # slot={}
                      # slot["location_city"]=word
                       string_dic["slots"]=slots

                       s_list.append(string_dic)

                       cinemas_movie_list=list(cinemas_movie)

                       for n in range(count):

                             w=random.choice (cinemas_movie_list )
                             sentence=text_value.replace(word,w)
                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             for k in slots:

                                if k=='name':

                                      slot["name"]=w
                                else:
                                      slot[k]=slots[k]

                             string_dic["slots"]=slot
                             s_list.append(string_dic)


                    if 'category'  in slots  :

                       word=slots['category']
                       #string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {name:'+word+'}}'

                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                      # slot={}
                      # slot["location_city"]=word
                       string_dic["slots"]=slots

                       s_list.append(string_dic)

                       #theatre_name_list=list(theatre_name)

                       for n in range(count):

                             w=random.choice (movie_category)
                             sentence=text_value.replace(word,w)
                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             for k in slots:

                                if k=='category':

                                      slot["category"]=w
                                else:
                                      slot[k]=slots[k]

                             string_dic["slots"]=slot
                             s_list.append(string_dic)


             if domain_value=="match":
                 if type(slots) != dict :
                     #slots = {}
                    # string_dic=string_dic+',{'+'domain:map,text:'+text_value+',intent:'+intent_value+',slots: {}}'

                     string_dic={}
                     string_dic["domain"]=domain_value
                     string_dic["text"]=text_value.strip()
                     string_dic["intent"]=intent_value
                     #slot={}

                     string_dic["slots"]=slots

                     s_list.append(string_dic)

                 else:

                    if 'name'  in slots  :

                       word=slots['name']
                       #string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {name:'+word+'}}'

                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                      # slot={}
                      # slot["location_city"]=word
                       string_dic["slots"]=slots

                       s_list.append(string_dic)

                       football_name_list=list(football_team)

                       for n in range(football_count):

                             w=random.choice (football_name_list )
                             sentence=text_value.replace(word,w)
                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             for k in slots:

                                if k=='name':

                                      slot["name"]=w
                                else:
                                      slot[k]=slots[k]

                             string_dic["slots"]=slot
                             s_list.append(string_dic)


             if domain_value=="lottery":
                 if type(slots) != dict :
                     #slots = {}
                    # string_dic=string_dic+',{'+'domain:map,text:'+text_value+',intent:'+intent_value+',slots: {}}'

                     string_dic={}
                     string_dic["domain"]=domain_value
                     string_dic["text"]=text_value.strip()
                     string_dic["intent"]=intent_value
                     #slot={}

                     string_dic["slots"]=slots

                     s_list.append(string_dic)

                 else:

                    if 'name'  in slots  :

                       word=slots['name']
                       #string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {name:'+word+'}}'

                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                      # slot={}
                      # slot["location_city"]=word
                       string_dic["slots"]=slots

                       s_list.append(string_dic)

                       lottery_name_list=list(lottery)

                       for n in range(lottery_count):

                             w=random.choice (lottery )
                             sentence=text_value.replace(word,w)
                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             for k in slots:

                                if k=='name':

                                      slot["name"]=w
                                else:
                                      slot[k]=slots[k]

                             string_dic["slots"]=slot
                             s_list.append(string_dic)


             if domain_value=="news":
                 if type(slots) != dict :
                     #slots = {}
                    # string_dic=string_dic+',{'+'domain:map,text:'+text_value+',intent:'+intent_value+',slots: {}}'

                     string_dic={}
                     string_dic["domain"]=domain_value
                     string_dic["text"]=text_value.strip()
                     string_dic["intent"]=intent_value
                     #slot={}

                     string_dic["slots"]=slots

                     s_list.append(string_dic)

                 else:

                    if 'location_city'  in slots and 'location_province' not in slots :

                       word=slots['location_city']
                       #string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {name:'+word+'}}'

                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                      # slot={}
                      # slot["location_city"]=word
                       string_dic["slots"]=slots

                       s_list.append(string_dic)

                       #lottery_name_list=list(lottery)

                       for n in range(city_count):

                             w=random.choice (city_address  )
                             sentence=text_value.replace(word,w)
                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             for k in slots:

                                if k=='location_city':

                                      slot["location_city"]=w
                                else:
                                      slot[k]=slots[k]

                             string_dic["slots"]=slot
                             s_list.append(string_dic)

#location_country


                    if 'location_country'  in slots and 'location_province' not in slots :

                       word=slots['location_country']
                       #string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {name:'+word+'}}'

                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                      # slot={}
                      # slot["location_city"]=word
                       string_dic["slots"]=slots

                       s_list.append(string_dic)

                       #lottery_name_list=list(lottery)

                       for n in range(city_count):

                             w=random.choice (location_country )
                             sentence=text_value.replace(word,w)
                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             for k in slots:

                                if k=='location_country':

                                      slot["location_country"]=w
                                else:
                                      slot[k]=slots[k]

                             string_dic["slots"]=slot
                             s_list.append(string_dic)





             if domain_value=="novel":
                 if type(slots) != dict :
                     #slots = {}
                    # string_dic=string_dic+',{'+'domain:map,text:'+text_value+',intent:'+intent_value+',slots: {}}'

                     string_dic={}
                     string_dic["domain"]=domain_value
                     string_dic["text"]=text_value.strip()
                     string_dic["intent"]=intent_value
                     #slot={}

                     string_dic["slots"]=slots

                     s_list.append(string_dic)

                 else:

                    if 'name'  in slots  :

                       word=slots['name']
                       #string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {name:'+word+'}}'

                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                      # slot={}
                      # slot["location_city"]=word
                       string_dic["slots"]=slots

                       s_list.append(string_dic)

                      # football_name_list=list(football_team)

                       for n in range(novel_count):

                             w=random.choice (novel_name )
                             sentence=text_value.replace(word,w)
                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             for k in slots:

                                if k=='name':

                                      slot["name"]=w
                                else:
                                      slot[k]=slots[k]

                             string_dic["slots"]=slot
                             s_list.append(string_dic)

                    if 'category'  in slots  :

                       word=slots['category']
                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                      # slot={}
                      # slot["location_city"]=word
                       string_dic["slots"]=slots

                       s_list.append(string_dic)

                       for n in range(novel_count):

                             w=random.choice (novel_category )
                             sentence=text_value.replace(word,w)
                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             for k in slots:

                                if k=='category':

                                      slot["category"]=w
                                else:
                                      slot[k]=slots[k]

                             string_dic["slots"]=slot
                             s_list.append(string_dic)


                    if 'author'  in slots  :

                       word=slots['author']
                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                      # slot={}
                      # slot["location_city"]=word
                       string_dic["slots"]=slots

                       s_list.append(string_dic)

                       for n in range(novel_count):

                             w=random.choice (novel_author )
                             sentence=text_value.replace(word,w)
                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             for k in slots:

                                if k=='author':

                                      slot["author"]=w
                                else:
                                      slot[k]=slots[k]

                             string_dic["slots"]=slot
                             s_list.append(string_dic)




             if domain_value=="health":
                 if type(slots) != dict :
                     #slots = {}
                    # string_dic=string_dic+',{'+'domain:map,text:'+text_value+',intent:'+intent_value+',slots: {}}'

                     string_dic={}
                     string_dic["domain"]=domain_value
                     string_dic["text"]=text_value.strip()
                     string_dic["intent"]=intent_value
                     #slot={}

                     string_dic["slots"]=slots

                     s_list.append(string_dic)

                 else:

                    if 'keyword'  in slots  :

                       word=slots['keyword']
                       #string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {name:'+word+'}}'

                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                      # slot={}
                      # slot["location_city"]=word
                       string_dic["slots"]=slots

                       s_list.append(string_dic)

                      # football_name_list=list(football_team)



             if domain_value=="app":
                 if type(slots) != dict :
                     #slots = {}
                    # string_dic=string_dic+',{'+'domain:map,text:'+text_value+',intent:'+intent_value+',slots: {}}'

                     string_dic={}
                     string_dic["domain"]=domain_value
                     string_dic["text"]=text_value.strip()
                     string_dic["intent"]=intent_value
                     #slot={}

                     string_dic["slots"]=slots

                     s_list.append(string_dic)

                 else:

                    if 'name'  in slots  :

                       word=slots['name']
                       #string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {name:'+word+'}}'

                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                      # slot={}
                      # slot["location_city"]=word
                       string_dic["slots"]=slots

                       s_list.append(string_dic)

                      # football_name_list=list(football_team)

                       for n in range(app_count):

                             w=random.choice (app_name )
                             sentence=text_value.replace(word,w)
                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             for k in slots:

                                if k=='name':

                                      slot["name"]=w
                                else:
                                      slot[k]=slots[k]

                             string_dic["slots"]=slot
                             s_list.append(string_dic)


             if domain_value=="poetry":
                 if type(slots) != dict :
                     #slots = {}
                    # string_dic=string_dic+',{'+'domain:map,text:'+text_value+',intent:'+intent_value+',slots: {}}'

                     string_dic={}
                     string_dic["domain"]=domain_value
                     string_dic["text"]=text_value.strip()
                     string_dic["intent"]=intent_value
                     #slot={}

                     string_dic["slots"]=slots

                     s_list.append(string_dic)

                 else:

                    if 'name'  in slots  :

                       word=slots['name']
                       #string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {name:'+word+'}}'

                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                      # slot={}
                      # slot["location_city"]=word
                       string_dic["slots"]=slots

                       s_list.append(string_dic)

                      # football_name_list=list(football_team)

                       for n in range(novel_count):
                        # if 
                         w=random.choice (poetry_author_name )
                         if w[1] not in text_value:
                             sentence=text_value.replace(word,w[1])
                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             for k in slots:

                                if k=='name':

                                      slot["name"]=w[1]
                                else:
                                      slot[k]=slots[k]

                             string_dic["slots"]=slot
                             s_list.append(string_dic)

                    if 'keyword'  in slots  :

                       word=slots['keyword']
                       #string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {name:'+word+'}}'

                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                      # slot={}
                      # slot["location_city"]=word
                       string_dic["slots"]=slots

                       s_list.append(string_dic)

                      # football_name_list=list(football_team)

                       for n in range(novel_count):

                             w=random.choice (poetry_keyword )
                             sentence=text_value.replace(word,w)
                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             for k in slots:

                                if k=='keyword':

                                      slot["keyword"]=w
                                else:
                                      slot[k]=slots[k]

                             string_dic["slots"]=slot
                             s_list.append(string_dic)

                    if 'name'  in slots and "author" in slots :

                       word=slots['name']
                       word2=slots['author']

                       #string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {name:'+word+'}}'

                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                      # slot={}
                      # slot["location_city"]=word
                       string_dic["slots"]=slots

                       s_list.append(string_dic)

                      # football_name_list=list(football_team)

                       for n in range(novel_count):

                          w=random.choice (poetry_author_name )

                          if (w[1] not in text_value) and (w[0] not in text_value):

                            sentence=text_value.replace(word,w[1])

                            if w[0] not in text_value:

                             sentence=sentence.replace(word2,w[0])
                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             for k in slots:

                                if k=='name':

                                      slot["name"]=w[1]
                                else:
                                   if k=="author":
                                      slot["author"]=w[0]

                                   else:

                                      slot[k]=slots[k]

                             string_dic["slots"]=slot
                             s_list.append(string_dic)



             if domain_value=="radio":
                 if type(slots) != dict :
                     #slots = {}
                    # string_dic=string_dic+',{'+'domain:map,text:'+text_value+',intent:'+intent_value+',slots: {}}'

                     string_dic={}
                     string_dic["domain"]=domain_value
                     string_dic["text"]=text_value.strip()
                     string_dic["intent"]=intent_value
                     #slot={}

                     string_dic["slots"]=slots

                     s_list.append(string_dic)

                 else:
                   if "location_province" not in slots:

                    if 'name'  in slots  and len(slots)==1:

                       word=slots['name']
                       #string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {name:'+word+'}}'

                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                      # slot={}
                      # slot["location_city"]=word
                       string_dic["slots"]=slots

                       s_list.append(string_dic)

                      # football_name_list=list(football_team)

                       for n in range(radio_count):

                             w=random.choice (radio_code_name )
                             sentence=text_value.replace(word,w[1])
                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             for k in slots:

                                if k=='name':

                                      slot["name"]=w[1]
                                else:
                                      slot[k]=slots[k]

                             string_dic["slots"]=slot
                             s_list.append(string_dic)

                    if 'name'  in slots  and "code" in slots:

                       word=slots['name']
                       word2=slots['code']
                       #string_dic=string_dic+',{'+'domain:telephone,text:'+text_value+',intent:'+intent_value+',slots: {name:'+word+'}}'

                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                      # slot={}
                      # slot["location_city"]=word
                       string_dic["slots"]=slots

                       s_list.append(string_dic)

                      # football_name_list=list(football_team)

                       for n in range(radio_count):

                             w=random.choice (radio_code_name )

                             sentence=text_value.replace(word,w[1])

                             sentence=sentence.replace(word2,w[0])
                            # string_dic=string_dic+',{'+'domain:telephone,text:'+sentence+',intent:'+intent_value+',slots: {name:'+w+'}}'
                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             for k in slots:

                                if k=='name':

                                      slot["name"]=w[1]
                                else:

              
                                   if k=='code':
                                      slot["code"]=w[0]

                                   else:

                                      slot[k]=slots[k]

                             string_dic["slots"]=slot
                             s_list.append(string_dic)



             if domain_value=="riddle":
                 if type(slots) != dict :
                     #slots = {}
                    # string_dic=string_dic+',{'+'domain:map,text:'+text_value+',intent:'+intent_value+',slots: {}}'

                     string_dic={}
                     string_dic["domain"]=domain_value
                     string_dic["text"]=text_value.strip()
                     string_dic["intent"]=intent_value
                     #slot={}

                     string_dic["slots"]=slots

                     s_list.append(string_dic)

                 else:

                    if 'category'  in slots  :

                       word=slots['category']

                       string_dic={}
                       string_dic["domain"]=domain_value
                       string_dic["text"]=text_value.strip()
                       string_dic["intent"]=intent_value
                      # slot={}
                      # slot["location_city"]=word
                       string_dic["slots"]=slots

                       s_list.append(string_dic)


                       for n in range(radio_count):

                             w=random.choice (riddle_category )
                             sentence=text_value.replace(word,w)

                             string_dic={}
                             string_dic["domain"]=domain_value
                             string_dic["text"]=sentence
                             string_dic["intent"]=intent_value
                             slot={}
                             for k in slots:

                                if k=='category':

                                      slot["category"]=w
                                else:
                                      slot[k]=slots[k]

                             string_dic["slots"]=slot
                             s_list.append(string_dic)



store( s_list)
