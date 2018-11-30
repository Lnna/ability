

import json
import os
import numpy as np
from gensim.models import Word2Vec
import pickle as pc

from codes import pos_methods as seg

from keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence
from sklearn.manifold import TSNE

import matplotlib.pyplot as plt
home_dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'../'))

class CleanData():
    def __init__(self, segment=True, content_maxlen=1000,title_maxlen=50,question_maxlen=50, word_dim=100,answer_maxlen=50):
        '''

        :param segment:
        :param content_maxlen: 文本序列的最大长度，需要根据统计来修正
        '''
        if segment==True:
            self.segmentor=seg.LtpNlp()
        self.content_maxlen=content_maxlen
        self.title_maxlen=title_maxlen
        self.question_maxlen=question_maxlen
        self.dim=word_dim
        self.answer_maxlen=answer_maxlen


    def raw_text(self,src_json):
        f = open(src_json)
        data = json.load(f)
        self.contents=[]
        self.questions=[]
        self.titles=[]
        self.answer=[]
        self.ids=[]
        self.qids=[]
        self.answer_start=[]
        self.answer_end=[]
        self.create=[]
        for exm in data:
            id=exm['article_id']
            title=str(exm['article_title']).replace(" ","")
            article=str(exm['article_content']).replace(" ","")
            questions=exm['questions']
            for q in questions:
                if dict(q).get('answer','')!='':
                    qs=str(q['question']).replace(" ","")
                    self.answer.append(str(q['answer']).replace(" ",""))
                    self.titles.append(title)
                    self.questions.append(qs)
                    self.contents.append(article)
                    self.ids.append(id)
                    self.qids.append(q['questions_id'])
                else:
                    print(q['questions_id'])

        if self.segmentor:
            self.seg_question=[]
            self.seg_title=[]
            self.seg_content=[]
            self.seg_answer=[]
            for q,t,c,a in zip(self.questions,self.titles,self.contents,self.answer):
                self.seg_question.append(list(self.segmentor.ltpseg(q)))
                self.seg_title.append(list(self.segmentor.ltpseg(t)))
                self.seg_content.append(list(self.segmentor.ltpseg(c)))
                self.seg_answer.append(list(self.segmentor.ltpseg(a)))

        self.token=Tokenizer()
        self.token.fit_on_texts(self.seg_content+self.seg_question+self.seg_title+self.seg_answer)


        self.contents_sequences=sequence.pad_sequences(self.token.texts_to_sequences(self.seg_content),maxlen=self.content_maxlen)
        self.questions_sequences=sequence.pad_sequences(self.token.texts_to_sequences(self.seg_question),maxlen=self.question_maxlen)
        self.titles_sequences=sequence.pad_sequences(self.token.texts_to_sequences(self.seg_title),maxlen=self.title_maxlen)
        # self.answer_sequences=self.token.texts_to_sequences(self.seg_answer)

    def answer_y(self):
        self.answer_start=[]
        self.answer_end=[]
        for i in range(len(self.questions)):
            start = -1
            end = -1
            if self.contents[i].find(self.answer[i])>=0:
                l=len(self.seg_answer[i])

                for j in range(len(self.seg_content[i])-l):
                    if self.seg_content[i][j:j+l]==self.seg_answer[i]:
                        start=j
                        if j+l-1-start+1<=self.answer_maxlen:
                            end=j+l-1
                        else:
                            end=start+self.answer_maxlen-1
                        break

            self.answer_start.append(start)
            self.answer_end.append(end)
            # self.answer_start = np.array(self.answer_start)
            # self.answer_end = np.array(self.answer_end)
            # self.answer_start = to_categorical(self.answer_start[self.answer_start >= 0], num_classes=self.maxlen)
            # self.answer_end = to_categorical(self.answer_end[self.answer_end >= 0], num_classes=self.maxlen)


    def embed(self,model_path=home_dir+'/model/w2c.model'):

        model = Word2Vec(self.seg_content+self.seg_answer+self.seg_title+self.seg_question,min_count=1,size=self.dim)
        model.save(model_path)

    def save(self,model_path=home_dir+'/model/w2c.model',raw_pk_path=home_dir+'/intermediate/raw_lacie.pc',
             seg_pk_path=home_dir + '/intermediate/seg_lacie.pc',
             seq_pk_path=home_dir + '/intermediate/seq_lacie.pc',
             vocab_path=home_dir + '/intermediate/vocab.pc',
             words_path=home_dir+'/intermediate/words.txt',noise_path=home_dir+'/intermediate/noise.txt'):
        model=Word2Vec.load(model_path)
        # print(model.wv['ld-2000'])
        self.embeddings=[]
        index_words = {}
        for k, v in self.token.word_index.items():
            index_words[v]=k
            self.embeddings.append(np.zeros(shape=(self.dim,),dtype=np.float32))
        for i in range(1,len(index_words.keys())+1):
            try:
                self.embeddings.append(model.wv[index_words[i]])
            except:
                self.embeddings.append(np.zeros(shape=(self.dim,), dtype=np.float32))
        #a bytes-like object is required, not 'list':pickle file 应该以bytes的mode打开
        pc.dump([self.ids,self.qids,self.titles,self.questions,self.contents,self.answer],open(raw_pk_path,mode='wb'))
        pc.dump([self.seg_title,self.seg_question,self.seg_content,self.seg_answer],open(seg_pk_path,mode='wb'))
        pc.dump([self.ids,self.qids,self.titles_sequences,self.questions_sequences,self.contents_sequences,self.answer,self.answer_start,self.answer_end],open(seq_pk_path,mode='wb'))
        pc.dump([self.embeddings,index_words, self.token.word_index],open(vocab_path,mode='wb'))
        word_counts=sorted(self.token.word_counts.items(),key=lambda d:d[1],reverse=True)
        with open(words_path,mode='w') as f:
            for wc in word_counts:
                f.write('{}  {}\n'.format(wc[0],wc[1]))
        f.close()
        with open(noise_path,mode='w') as f:
            for wc in self.create:
                f.write('{}\n'.format(wc[0]))
        f.close()

    def gen_batches(self,batch_size,type='train'):

        ids, qids,titles_sequences, questions_sequences, contents_sequences,answers, answer_start, answer_end \
            = pc.load(open(home_dir + '/intermediate/seq_lacie.pc', mode='rb'))
        start=0
        end=len(titles_sequences)

        if type=='train':
            start=0
            end = len(titles_sequences)*7//10
        elif type=='dev':
            start=len(titles_sequences)*7//10+1
            end=len(titles_sequences)*9//10
        elif type == 'test':
            start = len(titles_sequences) * 9 // 10 + 1
            end = len(titles_sequences)
        for i in range(start,end,batch_size):
            batch={
                'ids':ids[i:i+batch_size],
                'qids':qids[i:i+batch_size],
                'title':titles_sequences[i:i+batch_size],
                'question':questions_sequences[i:i+batch_size],
                'content':contents_sequences[i:i+batch_size],
                'seg_content':self.seg_content[i:i+batch_size],
                'answer':answers[i:i+batch_size],
                'answer_start':answer_start[i:i+batch_size],
                'answer_end':answer_end[i:i+batch_size],
                'content_len':[self.content_maxlen]*batch_size,
                'question_len':[self.question_maxlen]*batch_size
            }
            yield batch

    def view(self,word_path=home_dir+'/intermediate/sample_words.txt',pk_path=home_dir+'/intermediate/lacie.pc'):
        # 可视化测试
        words=[]
        with open(word_path) as f:
            for row in f.readlines():
                words.append(row.strip('\n').split('  ')[0])
        _,_,embeddings,_,_,index_words,word_indexs=pc.load(open(pk_path,mode='rb'))
        sample_embed=[embeddings[word_indexs[w]] for w in words]
        tsne = TSNE()
        plot = tsne.fit_transform(sample_embed)
        labels = words
        plt.rcParams['font.sans-serif'] = ['simhei']  # 用来正常显示中文标签
        # plt.title("词向量")
        # plt.scatter(x[:10], y[:10])
        # for i in range(len(x)):
        #     plt.annotate(labels[i], xy=(x[i], y[i]), xytext=(x[i], y[i]))  # 这里xy是需要标记的坐标，xytext是对应的标签坐标
        axes = plt.subplot()
        axes.scatter(plot[:,0], plot[:,1],alpha=0)
        axes.set_title("词向量")
        for i, j, l in zip(plot[:,0], plot[:,1],labels):
            axes.text(i, j, l)
        axes.grid()

        plt.savefig(home_dir + '/intermediate/w2c.png')
        plt.show()



    def gen_train_data(self):
        self.raw_text(src_json=home_dir + '/raw_data/lacie.json')
        self.answer_y()
        self.embed()
        self.save()


if __name__=="__main__":
    lacie=CleanData()
    lacie.raw_text(src_json=home_dir+'/raw_data/lacie.json')
    lacie.answer_y()
    lacie.embed()
    lacie.save()
    # lacie.view()