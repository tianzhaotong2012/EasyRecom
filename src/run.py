# encoding=utf-8
import jieba
import string
import os
import re
import sys
import shutil
import commands
import time
#import pandas as pd
#import numpy as np
from json import *
#reload(sys)
#sys.setdefaultencoding('utf-8')

import log
import platform
def isWindowsSystem():
    return 'Windows' in platform.system()
def isLinuxSystem():
    return 'Linux' in platform.system()
#取两个字符串的交集部分
def get_intersect(a_list,b_list):
    ret_list = list((set(a_list).union(set(b_list))) ^ (set(a_list) ^ set(b_list)))
    return len(ret_list)


#sys.argv=["",r"F:\cixiangliang\zhwiki",r"D:\pro\waimai\rank\rank_log\bin\cf\output\recommend",r"F:\ML\input\user",r"F:\ML\input\post\post"]

#input_dir=sys.argv[1]
DIR_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

INPUT_USER_DIR = os.path.join(DIR_ROOT,'input','user')
INPUT_POST_DIR = os.path.join(DIR_ROOT,'input','post','post_online')
GENERATE_POSTVEC_DIR = os.path.join(DIR_ROOT,'input','post','post_vec')
TMP_ROOT_DIR = os.path.join(DIR_ROOT,'input','tmp','')
TMP_USER_DIR = os.path.join(DIR_ROOT,'input','tmp','user','')
TMP_USERCOMPARE_DIR = os.path.join(DIR_ROOT,'input','tmp','user_compare','')
OUTPUT_RECOMMENDUSER_DIR = os.path.join(DIR_ROOT,'output','recommend','user','')

WORD2VEC_DIR = os.path.join(DIR_ROOT,'cixiangliang','zhwiki')
WORD2VEC_NAME = "zhwiki_2017_03.sg_50d.word2vec"
OPEN_GREP = isLinuxSystem()

def find_cixiangliang( str ):
    global WORD2VEC_DIR
    global WORD2VEC_NAME
    global OPEN_GREP
    similar_word='未找到相似的词向量'
    similar_vec=["a","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0",
                 "0.0","0.0","0.0",
                 "0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0",
                 "0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0","0.0"]
    if OPEN_GREP==True:
        cmd_str = 'grep ' + str + ' -m1 '+ os.path.join(WORD2VEC_DIR,WORD2VEC_NAME)
        (status, output) = commands.getstatusoutput(cmd_str)
        if status == 0:
            findList = output.split(" ")
            if len(findList) == 52:
                del(findList[len(findList)-1])
                similar_vec = findList
        del similar_vec[0]
        print similar_vec
        print len(similar_vec)
    	time.sleep(0.0001)
    	return map(eval, similar_vec)
    for line in open(os.path.join(WORD2VEC_DIR,WORD2VEC_NAME)):
        item = line.strip()
        item_list = item.split(" ")
        k=item_list[0].decode("utf-8")
        #print k
        #print str
        if get_intersect(list(k.decode("utf-8")),list(str.decode("utf-8")))==len(list(str.decode("utf-8"))):
            if len(k)<similar_word:
                similar_word=k
                similar_vec=item_list
            #print k
            #print list(k)
            #print str
            #print list(str)
            #print item_list
    #print similar_word
    del similar_vec[0]
    print similar_vec
    print len(similar_vec)
    return map(float, similar_vec)
#        exit(0)

def get_sentence_vec(temp):
    #temp = "千万别乱学，否则很容易成为别人眼中的笑料"
    temp = temp.decode("utf8")
    string = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"), temp)
    seg_list = jieba.cut(string, cut_all=False)
    vec_list = []
    for item in seg_list:
        #print item
        vec = find_cixiangliang(item)
        vec_list.append(vec)
    print vec_list
    l = vec_list
    a = list(map(lambda *l: sum(l), *l))
    #print a
    return a

#dic1["1"]=get_sentence_vec(dic1["1"])
#dic1["2"]=get_sentence_vec(dic1["2"])

def cos(vector1,vector2):
    dot_product = 0.0;
    normA = 0.0;
    normB = 0.0;
    for a,b in zip(vector1,vector2):
        dot_product += a*b
        normA += a**2
        normB += b**2
    if normA == 0.0 or normB==0.0:
        return 0.0
    else:
        return dot_product / ((normA*normB)**0.5)

def generatePostVec():
    global INPUT_POST_DIR
    global GENERATE_POSTVEC_DIR
    isExists = os.path.exists(GENERATE_POSTVEC_DIR)
    if isExists:
        os.remove(GENERATE_POSTVEC_DIR)
    for line in open(INPUT_POST_DIR):
        item = line.strip()
        item_list = item.split("\t")
        if len(item_list) != 2:
            continue
        post_id=item_list[0].decode("utf-8")
        post_title=item_list[1].decode("utf-8")
        post_vec=get_sentence_vec(post_title)
        #print post_title
        #print post_vec
        f=file(GENERATE_POSTVEC_DIR, 'a ')
        f.write(post_id+"\t"+JSONEncoder().encode(post_vec)+'\n')
        f.close()

#generatePostVec()

def generateUserReadVec():
    global INPUT_USER_DIR
    global TMP_USER_DIR
    user_id_list = os.listdir(INPUT_USER_DIR)
    for user_id in user_id_list:
        for line in open(os.path.join(INPUT_USER_DIR,user_id)):
            item = line.strip()
            item_list = item.split(" ")
            post_id = item_list[0].decode("utf-8")
            post_title = item_list[1].decode("utf-8")
            post_vec = get_sentence_vec(post_title)
            #print post_title
            #print post_vec
            isExists = os.path.exists(TMP_USER_DIR)
            if not isExists:
                os.makedirs(TMP_USER_DIR)
            path=TMP_USER_DIR + user_id
            isExists = os.path.exists(path)
            if not isExists:
                f = file(TMP_USER_DIR + user_id, 'w')
                f.write("")
                f.close()
            f = file(TMP_USER_DIR + user_id, 'a')
            f.write(post_id + "\t" + JSONEncoder().encode(post_vec) + '\n')
            f.close()

#generateUserReadVec(sys.argv[3])

def compare():
    global TMP_USER_DIR
    global GENERATE_POSTVEC_DIR
    global TMP_USERCOMPARE_DIR
    user_id_list = os.listdir(TMP_USER_DIR)
    for user_id in user_id_list:
        for line in open(TMP_USER_DIR + user_id):
            item = line.strip()
            item_list = item.split("\t")
            post_id = item_list[0].decode("utf-8")
            post_vec = JSONDecoder().decode(item_list[1].decode("utf-8"))
            for iline in open(GENERATE_POSTVEC_DIR):
                ilineItem=iline.strip()
                ilineItemList=ilineItem.split("\t")
                ilinePostId=ilineItemList[0].decode("utf-8")
                ilinePostVec=JSONDecoder().decode(ilineItemList[1].decode("utf-8"))
                dis=cos(post_vec,ilinePostVec)
                if dis == 1.0:
                    dis=0.0
                path=TMP_USERCOMPARE_DIR + os.path.join(user_id,'')
                isExists = os.path.exists(path)
                if not isExists:
                    os.makedirs(path)
                f = file(path+post_id, 'a')
                f.write(ilinePostId+"\t"+str(dis)+'\n')
                f.close()

#compare()

def sort_cos():
    global TMP_USER_DIR
    global TMP_USERCOMPARE_DIR
    user_id_list = os.listdir(TMP_USER_DIR)
    for user_id in user_id_list:
        post_id_list = os.listdir(TMP_USERCOMPARE_DIR + os.path.join(user_id,''))
        for post_id in post_id_list:
            list = []
            for iline in open(TMP_USERCOMPARE_DIR + os.path.join(user_id,'')+post_id):
                ilineItem = iline.strip()
                ilineItemList = ilineItem.split("\t")
                list.append(ilineItemList)
            sortList = sorted(list, key=lambda x: x[1], reverse=True)
            f = file(TMP_USERCOMPARE_DIR + os.path.join(user_id,'')+post_id, 'w')
            f.close()
            f = file(TMP_USERCOMPARE_DIR + os.path.join(user_id,'')+post_id, 'a')
            for line in sortList:
                f.write(str(line[0]) + "\t" + str(line[1]) + "\n")
            f.close()



#sort_cos()

def top_cos():
    global TMP_USER_DIR
    global TMP_USERCOMPARE_DIR
    global OUTPUT_RECOMMENDUSER_DIR
    isExists = os.path.exists(OUTPUT_RECOMMENDUSER_DIR)
    if not isExists:
        os.makedirs(OUTPUT_RECOMMENDUSER_DIR)
    user_id_list = os.listdir(TMP_USER_DIR)
    for user_id in user_id_list:
        list =[]
        post_id_list = os.listdir(TMP_USERCOMPARE_DIR + os.path.join(user_id,''))
        for post_id in post_id_list:
            i=0
            for iline in open(TMP_USERCOMPARE_DIR + os.path.join(user_id,'') + post_id):
                if i>3:
                    break
                ilineItem = iline.strip()
                ilineItemList = ilineItem.split("\t")
                list.append(ilineItemList)
                i=i+1
        f = file(OUTPUT_RECOMMENDUSER_DIR + user_id, 'w')
        f.close()
        f = file(OUTPUT_RECOMMENDUSER_DIR + user_id, 'a')
        for line in list:
            f.write(str(line[0]) + "\t" + str(line[1]) + "\n")
        f.close()

#top_cos()

def cleanTmpAndRes():
    global TMP_ROOT_DIR
    global OUTPUT_RECOMMENDUSER_DIR
    isExists = os.path.exists(OUTPUT_RECOMMENDUSER_DIR)
    if isExists:
        shutil.rmtree(OUTPUT_RECOMMENDUSER_DIR)
    isExists = os.path.exists(TMP_ROOT_DIR)
    if isExists:
        shutil.rmtree(TMP_ROOT_DIR)

#cleanTmpAndRes()



def main():
    log.write("-------------------  easyRecommendFramework  START  --------------------------")
    cleanTmpAndRes()
    log.write("-------------------  generatePostVec  START         --------------------------")
    generatePostVec()
    log.write("-------------------  generatePostVec  END           --------------------------")
    log.write("-------------------  generateUserVec  START         --------------------------")
    generateUserReadVec()
    log.write("-------------------  generateUserVec  END           --------------------------")
    log.write("-------------------  COMPARE          START         --------------------------")
    compare()
    log.write("-------------------  COMPARE          END           --------------------------")
    log.write("-------------------  SORT             START         --------------------------")
    sort_cos()
    log.write("-------------------  SORT             END           --------------------------")
    log.write("-------------------  GET TOP          START         --------------------------")
    top_cos()
    log.write("-------------------  easyRecommendFramework   END   --------------------------")

main()

