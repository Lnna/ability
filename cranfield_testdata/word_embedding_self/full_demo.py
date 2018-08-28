
import os
import numpy as np
import pickle as pc
import tensorflow as tf
from word_embedding_self.data_pre_process import DataBatch

data_map=os.path.abspath(os.path.join(__file__,'../../data/lacie.pk'))
f=open(data_map,mode='rb')
total_words,words_list,word_ids,id_words,ids_list=pc.load(f)
db=DataBatch(ids_list,batch_size=32)

embed_dim=100
num_sampled=100
epoches=10
vocab_size = len(word_ids)
train_graph=tf.Graph()
with train_graph.as_default():
    #[batch_size]tensor
    input=tf.placeholder(tf.int32,shape=[None],name='inputs')
    #[batch_size,num_true=1]tensor
    labels=tf.placeholder(tf.int32,shape=[None,None],name='labels')
    # 为什么输入权重初始化是均匀分布，隐含权重初始化是正太分布

    embeddings=tf.random_uniform(shape=[vocab_size,embed_dim],minval=-1,maxval=1)
    embed_layer=tf.nn.embedding_lookup(embeddings,input)

    hidden_weights=tf.Variable(tf.truncated_normal([vocab_size,embed_dim],stddev=0.1))
    hidden_bias=tf.Variable(tf.zeros([vocab_size]))
    #使用采样方法选择部分负样本，连同正样本一起，计算在这堆样本中正样本的概率,实际上是选择部分w的值进行更新
    cost=tf.nn.sampled_softmax_loss(hidden_weights,hidden_bias,labels,embed_layer,num_sampled,vocab_size)
    loss=tf.reduce_mean(cost)#batch size tensor cost
    #根据loss计算梯度，再应用梯度更新参数
    optimizor=tf.train.AdamOptimizer().minimize(loss)

with train_graph.as_default():
    test_vocab=[word_ids['无人机'],word_ids['导弹'],word_ids['问题'],word_ids['航空'],word_ids['军事']]
    test_input=tf.constant(test_vocab,tf.int32,name='test_input')
    test_embed=tf.nn.embedding_lookup(embeddings,test_input)
    #计算相似度
    norm=embeddings/tf.sqrt(tf.reduce_sum(tf.square(embeddings),axis=1,keep_dims=True))
    similarity=tf.matmul(test_embed,tf.transpose(norm))

f=open('simlog.txt',mode='w')
# 为什么sess=tf.Session(graph=train_graph)会报错：noop not element of graph
with tf.Session(graph=train_graph) as sess:

    sess.run(tf.global_variables_initializer())
    for e in range(epoches):
        for i,(x, y) in enumerate(db.batches()):
            feed_dict={
                input:x,
                labels:np.array(y)[:,None]
            }
            train_loss,_=sess.run([loss,optimizor],feed_dict=feed_dict)
            print('iteration {} batch {} loss {}'.format(e,i,train_loss))
        sim=similarity.eval()
        top_k=10
        f.write("iteration {}:\n".format(e))
        for s in range(len(test_vocab)):
            nearest=(-sim[s,:]).argsort()[1:top_k+1]
            f.write("nearest to {} are: {}\n".format(id_words[test_vocab[s]],str([id_words[k] for k in nearest])))
f.close()