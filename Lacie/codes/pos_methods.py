#coding=utf-8
import os
import json,requests
import jieba.posseg as pos
from stanfordcorenlp import StanfordCoreNLP
import pyltp
import thulac
import pynlpir
import fool

# 中科院，snownlp，fudannlp
class JiebaNlp():
    def __init__(self):
        pass

    def jieba_pos(self,sen):
        return pos.cut(sen, HMM=True)

class StanfordNlp():
    '''
    # https://blog.csdn.net/guolindonggld/article/details/72795022
    '''
    def __init__(self):

        self.nlp = StanfordCoreNLP(r'/home/lnn/Documents/postag/stanford-corenlp-full-2016-10-31/', lang='zh')
    def stanford_pos(self,sen):
        return self.nlp.pos_tag(sen)

class LtpNlp():
    '''
    #http://ltp.readthedocs.io/zh_CN/latest/install.html
    #https://github.com/HIT-SCIR/pyltp
    #http://pyltp.readthedocs.io/zh_CN/latest/api.html#id10
    '''
    def __init__(self):
        # model_path = '/home/lnn/Documents/postag/ltp_data_v3.4.0/'
        model_path = '/home/nana/Documents/ltp_data_v3.4.0/'
        self.seg = pyltp.Segmentor()
        self.seg.load(model_path + 'cws.model')
        self.pos = pyltp.Postagger()
        self.pos.load(model_path + 'pos.model')

    def ltpseg(self,sen):
        words=self.seg.segment(sen)
        return words

    def ltppos(self, sen):
        words=self.ltpseg(sen)
        pos_words=self.pos.postag(words)
        return [(i,j) for i,j in zip(words,pos_words)]
    def release(self):
        self.seg.release()
        self.pos.release()

class ThulacNlp():
    '''
    http://thulac.thunlp.org/
    '''
    def __init__(self):
        self.thu=thulac.thulac()
    def pos(self,sen):
        words=self.thu.cut(sen)
        pos_words=[]
        for row in words:
            pos_words.append((row[0],row[1]))
        return pos_words

class ICTCLAS():
    def __init__(self):
        pynlpir.open()

    def pos(self,sen):
        return pynlpir.segment(sen)
    def close(self):
        pynlpir.close()

class Fool():
    def __init__(self):
        pass
    def pos(self,sen):
        res=fool.pos_cut(sen)
        return res[0]

