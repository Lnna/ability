import os
import pickle as pc
import tensorflow as tf
import numpy as np
from keras.utils import to_categorical


home_dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'/intermediate/'))

titles_sequences, questions_sequences, contents_sequences, answer_start, answer_end \
        = pc.load(open(home_dir + '/seq_lacie.pc', mode='rb'))
size=len(answer_start)

sequences = np.concatenate((titles_sequences, contents_sequences, questions_sequences), axis=1)

embeddings,index_words, word_index=pc.load(open(home_dir+'/vocab.pc',mode='rb'))

graph=tf.Graph()
epoches=10
hidden_dim=1000
batch_size=32
train_size=size*7//10
dev_size=size*9//10


with graph.as_default():
    inputs=tf.placeholder(dtype=tf.int32,name='inputs',shape=[None,None])
    labels=tf.placeholder(dtype=tf.int32,name='labels',shape=[None])

    embed_layer=tf.nn.embedding_lookup(embeddings,inputs)

    cell=tf.nn.rnn_cell.BasicLSTMCell(hidden_dim)
    output,_=tf.nn.static_rnn(cell,embed_layer)

    logits=np.argmax(tf.nn.softmax(output))
    loss=tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=labels,logits=logits))
    optimizor=tf.train.AdamOptimizer().minimize(loss)

with tf.Session(graph=graph) as sess:
    sess.run(tf.global_variables_initializer())
    for i in range(epoches):
        for i in range(0,train_size,batch_size):
            feed_dict = {
                inputs: sequences[i:min(train_size,i+batch_size)],
                labels: answer_start[i:min(train_size,i+batch_size)]
            }
            loss,_ = sess.run([loss,optimizor], feed_dict=feed_dict)
            print('train epoch {} loss: {}'.format(i,loss))

        for i in range(train_size,dev_size,batch_size):
            feed_dict = {
                inputs: sequences[i:min(dev_size,i+batch_size)],
                labels: answer_start[i:min(dev_size,i+batch_size)]
            }
            predicts,loss = sess.run([logits,loss], feed_dict=feed_dict)
            print('dev epoch {} loss: {}'.format(i,loss))





