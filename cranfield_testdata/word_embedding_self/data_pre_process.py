import json
import os
import numpy as np
import pos_methods as seg
import pickle as pc
class DataClean():
    def __init__(self,src_json):
        self.segmentor=seg.LtpNlp()
        f=open(src_json)
        self.data=json.load(f)
        self.sen_list=[]
        self.words_list=[]
        self.ids_list=[]
        self.word_ids={}
        self.id_words={}
        self.vocab_count={}
        self.total_words=0

    def rm_noise(self,noise=['，','。','！','（','）','【','】',':']):
        '''
        去除哪些噪音，可以在这里添加
        要去除标点符号，并将句子从此处分开 以免影响词表示:如逗号，句号如果保留，
        ("fox", "。") 这样的训练样本并不会给我们提供关于“fox”更多的语义信息，因为“。”在非常多单词的上下文中几乎都会出现，似乎并不是
        问号暂时保留，使其与一些疑问词表达相似，有什么用吗？不知道，先这样吧
        :return:
        '''
        def rm_tag(sen):
            for i in noise:
                sen=str(sen).replace(i,'')
            self.sen_list.append(sen)

        for row in self.data:
            title=row['article_title']
            content=row['article_content']
            rm_tag(title)
            rm_tag(content)
            qs=row['questions']
            for q in qs:
                rm_tag(q['question'])


    def segment(self,segment=True):
        '''
        使用ltp分词
        :return:
        '''
        for row in self.sen_list:
            if segment == True:
                sen = list(self.segmentor.ltpseg(row))
            else:
                sen=list(row)
            self.words_list.append(sen)
            for w in sen:
                if self.vocab_count.get(w, 0) == 0:
                    self.vocab_count[w] = 1
                else:
                    self.vocab_count[w] = self.vocab_count[w] + 1






    def rm_min_freq(self,min_freq=5):
        '''
        去除低频词
        :param min_freq:
        :return:
        '''
        vocab={}
        for k,v in self.vocab_count.items():
            if v > min_freq:
                vocab[k]=v
        self.vocab_count=vocab

    def word_map(self):
        self.word_ids={w:id for id,w in enumerate(self.vocab_count.keys())}
        self.id_words={id:w for id,w in enumerate(self.vocab_count.keys())}
        self.ids_list=[[self.word_ids[w]  for w in row if self.word_ids.get(w,-1)>-1 ] for row in self.words_list]
        self.total_words=np.sum(list(self.vocab_count.values()))
        print("unique words:{}".format(len(self.vocab_count)))
        print("total_words:{}".format(self.total_words))


    def freq_sample(self,threshold=0.8):
        '''
        高频词采样
        :param threshold:
        :return:
        '''
        t=1e-5
        vocab={}
        self.total_words=np.sum(list(self.vocab_count.values()))
        for k,v in self.vocab_count.items():
            freq=v/self.total_words
            prob=1-np.sqrt(t/freq)
            if prob<threshold:
                vocab[k]=v
        self.vocab_count=vocab



class DataBatch():
    def __init__(self, ids_list, batch_size,window_size=3):
        self.raw_data=ids_list
        self.batch_size=batch_size
        self.window_size=window_size

    def batches(self):
        '''
        是否应该只取full_batch,否则是否会报错.每个batchsize应相等
        :return:
        '''
        x=[]
        y=[]
        for row in self.raw_data:
           for i,w in enumerate(row):
               start=0
               end=0
               if i>self.window_size:
                   start=i-self.window_size
               if i+self.window_size<len(row):
                   end=i+self.window_size+1
               else:
                   end=len(row)
               y_tmp=row[start:i]+row[i+1:end]
               x.extend([row[i]]*(end-start-1))
               y.extend(y_tmp)
               if len(x)>=self.batch_size:

                   yield x[:self.batch_size+1],y[:self.batch_size+1]
                   x=x[self.batch_size:]
                   y=y[self.batch_size:]


def save_pickle():

    data_path=os.path.abspath(os.path.join(__file__,'../../data/lacie.json'))
    data_map=os.path.abspath(os.path.join(__file__,'../../data/lacie.pk'))
    dc=DataClean(src_json=data_path)
    dc.rm_noise()
    dc.segment(segment=True)
    dc.rm_min_freq()
    # dc.freq_sample()
    dc.word_map()
    f=open(data_map,mode='wb')
    pc.dump([dc.total_words,dc.words_list,dc.word_ids,dc.id_words,dc.ids_list],f)
    with open('words.txt',mode='w') as f:
        for w in dc.word_ids:
            f.write(w+'\n')
    f.close()




if __name__=="__main__":
    save_pickle()

