import os
import pandas as pd
from src.com.zelkova.toutiao.cranfield_testdata import pos_methods as  pm,ttdata
res = ttdata.fetch_corpus()
# res=["上海现在在下大暴雨"]
HOME_DIR=os.path.abspath(os.path.join(__file__,'../../../../../../'))

def static_pos(pos_func, data, save_path,remain=[]):
    map = dict()
    for row in data:
        s = str(row[0]).replace(' ', '')
        if s:
            for w, p in pos_func(s):
                if map.get(p, []) == []:
                    map[p] = [w]
                else:
                    if w not in map[p]:
                        map[p].append(w)
    save_txt(map, save_path)
def jieba_gen(func,save_path,remain_pos):
    nlp=pm.JiebaNlp()
    func(nlp.jieba_pos, res, save_path,remain=remain_pos)

def thu_gen(func,save_path,remain_pos):
    nlp=pm.ThulacNlp()
    func(nlp.pos, res, save_path,remain=remain_pos)

def stanford_gen(func,save_path,remain_pos):
    nlp=pm.StanfordNlp()
    func(nlp.stanford_pos, res, save_path,remain=remain_pos)

def ltp_gen(func,save_path,remain_pos):
    nlp=pm.LtpNlp()
    func(nlp.ltppos, res, save_path,remain=remain_pos)
    nlp.release()

def ictclas_gen(func,save_path,remain_pos):
    nlp=pm.ICTCLAS()
    func(nlp.pos,res,save_path,remain=remain_pos)
    nlp.close()

def fool_gen(func,save_path,remain_pos):
    nlp=pm.Fool()
    func(nlp.pos,res,save_path,remain=remain_pos)

def save_txt(map:dict, path):
    with open(path,mode='w') as f:
        for k,v in map.items():
            if k and v:
                f.write(k+':\n')
                for i in range(0,len(v),10):
                    if i+10<len(v):
                        f.write(' '.join(v[i:i+10])+'\n')
                    else:
                        f.write(' '.join(v[i:])+'\n')
    f.close()

def title_pos(pos_func, data, save_path,remain=[]):
    words_pos=[]
    for row in data:
        ns = []
        if row[0]:
            for w,p in pos_func(row[0]):
                if p in remain:
                    ns.append(w)
        words_pos.append(ns)
    save_csv(data,words_pos,save_path)
def save_csv(data,words,path):
    df=pd.DataFrame()
    for t,w in zip(data,words):
        df=df.append({'title':t[0],'pos_word':w},ignore_index=True)
    df.to_csv(path_or_buf=path,index=False)


jieba_remain_pos=['n','nr','nz','l','i','eng']
ltp_remain_pos=['n','nh','nz','j','ws','i']
stanford_remain_pos=['NN','NR']
thulac_remain_pos=['n','nz','np','i','id']
ictclas_remain_pos=['noun']
fool_remain_pos=['nz','ns','n','nr','nx','nl']
# jieba_gen(title_pos,'jieba_title.csv',jieba_remain_pos)
# ltp_gen(title_pos,'ltp_title.csv',ltp_remain_pos)
# stanford_gen(title_pos,'stanford_title.csv',stanford_remain_pos)
# thu_gen(title_pos,'thulac_title.csv',thulac_remain_pos)
# ictclas_gen(static_pos,'ictclas.txt',[])
# ictclas_gen(title_pos,'ictclas.csv',ictclas_remain_pos)
# fool_gen(static_pos,'fool.txt',[])
fool_gen(title_pos,'fool.csv',fool_remain_pos)