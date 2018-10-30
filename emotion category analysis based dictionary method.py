# coding: utf-8
# This is the code I wrote for analyzing emotion of Weibo blogs based dictionary method. So the corpus is Chinese and some NLP modules adopted are special for Chinese.

import os
import time
import datetime
import numpy as np
import pandas as pd
import jieba
import sys

reload(sys)
sys.setdefaultencoding('utf8')
df = pd.read_excel("emotionWords.xlsx", 'Sheet1', index_col=None, na_values=['NA'])

def open_dict(Dict):
    path = '%s.txt' % Dict
    dictionary = open(path, 'r')
    dict = []
    for word in dictionary:
        word = word.strip()
        dict.append(word)
    return dict

def judgeodd(num):
    if (num % 2) == 0:
        return 'even'
    else:
        return 'odd'

grouped=df.groupby(df['emotiontype'])
emotionDic={}

#Constructing emotion dictionary 
for i in grouped:
    key=i[0].strip()
    emotionword=[]
    for j in i[1]['word']:
        emotionword.append(j)
    emotionDic[key]=emotionword

deny_word = open_dict(Dict = 'privative')
#Constructing degree words 
degree_word = open_dict(Dict = 'degree')
print(degree_word)
mostdict = degree_word[degree_word.index('extreme')+1 : degree_word.index('very')]#Weight 4, that is, multiplied by 4 before emotion words. 
verydict = degree_word[degree_word.index('very')+1 : degree_word.index('more')]#Weight3
moredict = degree_word[degree_word.index('more')+1 : degree_word.index('ish')]#Weight2
ishdict = degree_word[degree_word.index('ish')+1 : degree_word.index('last')]#Weight0.5

def sentiment_score_list(line):
    result=[]
    seg_sentence=str(line).split('。')
    for sen in seg_sentence:
        segtmp = jieba.lcut(sen, cut_all=False)
        currentIndex=0#Scan the current location 
        emotionWordIndex=0#Current emotion word position 
        emotionwordScore=0
        count=0
        count2=0
        count3=0#Final emotional score 
        hasEmotion=False
        for word in segtmp:
            emotion={'NB':0,'NC':0,'ND':0,'NE':0,'NG':0,'NH':0,'NI':0,'NJ':0,'NK':0,'NL':0,'NN':0,'PA':0,'PB':0,'PC':0,'PD':0,'PE':0,'PF':0,'PG':0,'PH':0,'PK':0}
            for key in emotionDic:
                count=emotion.get(key)
                if word in emotionDic.get(key):# Determine whether words are emotional words. 
                    hasEmotion=True
                    count+=1
                    c = 0
                    for w in segtmp[emotionWordIndex:currentIndex]: # Scanning degree words before emotional words
                        if w in mostdict:
                            count *= 4.0
                        elif w in verydict:
                            count *= 3.0
                        elif w in moredict:
                            count *= 2.0
                        elif w in ishdict:
                            count *= 0.5
                        elif w in deny_word:
                            c += 1
                    if judgeodd(c) == 'odd':  # Scanning negative words before emotional words 
                        count *= -1.0
                        count2 += count
                        count = 0
                        count3 = count + count2 + count3
                        count2 = 0
                    else:
                        count3 = count + count2 + count3
                        count = 0
                    emotion[key]=count3
                    emotionWordIndex=currentIndex+1
            if word=='！' or word=='!':##Determin whether there is an exclamation mark in the sentence. 
                if hasEmotion==True:
                    for key in emotion:
                        if emotion[key]!=0:
                            emotion[key]+=2
            currentIndex += 1
            result.append(emotion)
    return result

def sentiment_score(line):
    senti_score_list=sentiment_score_list(line)
    emotion={'NB':[],'NC':[],'ND':[],'NE':[],'NG':[],'NH':[],'NI':[],'NJ':[],'NK':[],'NL':[],'NN':[],'PA':[],'PB':[],'PC':[],'PD':[],'PE':[],'PF':[],'PG':[],'PH':[],'PK':[]}
    sorce={'NB':[],'NC':[],'ND':[],'NE':[],'NG':[],'NH':[],'NI':[],'NJ':[],'NK':[],'NL':[],'NN':[],'PA':[],'PB':[],'PC':[],'PD':[],'PE':[],'PF':[],'PG':[],'PH':[],'PK':[]}
    emotionResult=[]
    for review in senti_score_list:
        wordEmotion = review
        for key in wordEmotion:
            emotion[key].append(wordEmotion[key])
    
    maxTotal=0
    realTotal=0
    emotionstd=0
    emotionFlag=''
    for key in emotion:
        keyList=emotion[key]
        total=np.sum(keyList)
        avg=np.mean(keyList)
        std=np.std(keyList)
        sorce[key].append([total,avg,std])
        if maxTotal < abs(total):
            emotionFlag=key
            realTotal=total
            maxTotal=abs(total)
            emotionstd=std
        elif maxTotal==abs(total):
            if emotionstd > std:
                emotionFlag=key
                realTotal=total
                maxTotal=abs(total)
                emotionstd=std
    emotionResult.append([emotionFlag,realTotal])
    return emotionResult

dataPath = '/Users/lyndon/PycharmProjects/emotionScore/data'
dataFiles = os.listdir(dataPath)
for dataFile in dataFiles:
    t1 = datetime.datetime.now()
    #read into document
    df = pd.read_excel(dataPath + '/' + dataFile, 'Sheet1' , index_col=None, na_values=['NA'])
    # df.shape
    df['emotion']=df.content.apply(sentiment_score)
    df.to_excel('./categoryResult/' + dataFile.split('.')[0] + '_category.xlsx', sheet_name='Sheet1')
    # print('done')
    t2 = datetime.datetime.now()
    print('Done. Cost:', t2-t1)
    time.sleep(30)

    
    
### Edited by:

Yuru LI
the Communication University of China
Laboratory of Data Mining and Social Computing
