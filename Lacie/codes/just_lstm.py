import os
import pickle as pc
import tensorflow as tf
import numpy as np
from keras.utils import to_categorical
from codes import rouge
from codes import lacie_data

# lacie_data.gen_train_data()
home_dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'../'))

titles_sequences, questions_sequences, contents_sequences, answer_start, answer_end \
        = pc.load(open(home_dir + '/intermediate/seq_lacie.pc', mode='rb'))


print('sequences load!')
print('answer len:{} {}'.format(len(answer_start),len(answer_end)))
seg_title,seg_question,seg_content,seg_answer=pc.load(open(home_dir + '/intermediate/seg_lacie.pc', mode='rb'))
print('seg contents load!')
size=len(answer_start)

sequences = np.concatenate((titles_sequences, contents_sequences, questions_sequences), axis=1)
sequences=[list(i) for i in sequences]
print('sequences length: {}'.format(len(sequences)))
#这里的embeddings是list of array
embeddings,index_words, word_index=pc.load(open(home_dir+'/intermediate/vocab.pc',mode='rb'))

print('embed load!')
seq_len=len(sequences[0])
answer_start=[i  if i>=0 and i<seq_len else seq_len for i in answer_start]
answer_end=[i  if i>=0 and i<seq_len else seq_len for i in answer_end]
start_labels=to_categorical(answer_start,num_classes=seq_len+1)
end_labels=to_categorical(answer_end,num_classes=seq_len+1)
tf.reset_default_graph()

graph=tf.Graph()
word_dim=100
epoches=10
hidden_dim=1101
batch_size=32
train_size=size*7//10
dev_size=size*9//10
with graph.as_default():
    inputs=tf.placeholder(dtype=tf.int32,name='sinputs',shape=[None,None])
    slabels=tf.placeholder(dtype=tf.int32,name='slabels',shape=[None,None])
    elabels=tf.placeholder(dtype=tf.int32,name='elabels',shape=[None,None])
    # ValueError: Argument must be a dense tensor: embeddings - got shape [8240, 100], but wanted [8240].
    embed_array=tf.constant([list(i) for i in embeddings],shape=[len(embeddings),word_dim])
    em=tf.Variable(initial_value=[list(i) for i in embeddings],trainable=True)
    # print(embed_array.shape)
    embed_layer=tf.nn.embedding_lookup(embed_array,inputs)

    with tf.variable_scope('start_lstm'):#to do with:rnn already exists,disallowed
        scell = tf.nn.rnn_cell.BasicLSTMCell(hidden_dim)
        soutput, sstatus = tf.nn.dynamic_rnn(scell, embed_layer, sequence_length=[len(sequences[0])] * batch_size,
                                             dtype=tf.float32)
        # soutput shape(batch_size,time_step,feature_dim) transfer to a list（len=timestep） of shape(batch_size,feature_dim),获取最后一个timestep的值
        soutput = tf.unstack(soutput, axis=1, num=seq_len)
        sloss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=slabels, logits=soutput[-1]))
        soptimizor = tf.train.AdamOptimizer().minimize(sloss)

    with tf.variable_scope('end_lstm'):
        #state_tuple =false so logits can be states
        ecell = tf.nn.rnn_cell.BasicLSTMCell(hidden_dim)
        eoutput, estatus = tf.nn.dynamic_rnn(ecell, embed_layer, sequence_length=[len(sequences[0])] * batch_size,
                                             dtype=tf.float32)
        eoutput = tf.unstack(eoutput, axis=1, num=seq_len)

        eloss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=elabels, logits=eoutput[-1]))
        eoptimizor = tf.train.AdamOptimizer().minimize(eloss)
    saver=tf.train.Saver()


with tf.Session(graph=graph) as sess:
    sess.run(tf.global_variables_initializer())
    for p in range(epoches):
        for i in range(0,train_size,batch_size):
            feed_dict = {
                inputs: sequences[i:min(train_size,i+batch_size)],
                slabels: start_labels[i:min(train_size,i+batch_size)]
            }
            if len(sequences[ i:min(train_size,i+batch_size)])<batch_size:
                continue
            loss,_ = sess.run([sloss,soptimizor], feed_dict=feed_dict)
            print('train epoch {} batch {} start label loss: {}'.format(p,i,loss))

            feed_dict = {
                inputs: sequences[i:min(train_size, i + batch_size)],
                elabels: end_labels[i:min(train_size, i + batch_size)]
            }
            if len(sequences[ i:min(train_size,i+batch_size)])<batch_size:
                continue
            loss, _ = sess.run([eloss, eoptimizor], feed_dict=feed_dict)
            print('train epoch {} batch {} end label loss: {}'.format(p,i,loss))

        for i in range(train_size,dev_size,batch_size):
            feed_dict = {
                inputs: sequences[i:min(dev_size,i+batch_size)],
                slabels: start_labels[i:min(dev_size,i+batch_size)]
            }
            if len(sequences[i:min(dev_size,i+batch_size)])<batch_size:
                continue
            spredicts,loss = sess.run([soutput,sloss], feed_dict=feed_dict)
            print('dev epoch {} batch {}  start loss: {}'.format(p,i,loss))

            feed_dict = {
                inputs: sequences[i:min(dev_size, i + batch_size)],
                elabels: end_labels[i:min(dev_size, i + batch_size)]
            }
            if len(sequences[i:min(dev_size,i+batch_size)])<batch_size:
                continue
            epredicts, loss = sess.run([eoutput, eloss], feed_dict=feed_dict)
            print('dev epoch {} batch {}  end loss: {}'.format(p,i,loss))
            sp = tf.argmax(spredicts[-1])
            ep = tf.argmax(epredicts[-1])

            rscore = rouge.RougeL()
            for content,answer,s,e in zip(seg_content[i:min(dev_size,i+batch_size)],seg_answer[i:min(dev_size,i+batch_size)],
                                          sp.eval(),ep.eval()):
                if s >= 0 and s <= min(len(content), seq_len) and e >= 0 and e <= min(len(content), seq_len):

                    cand=''.join(content[s:e])
                else:
                    cand=''
                rscore.add_inst(cand,''.join(answer))
            score=rscore.get_score()
            print('dev epoch {} batch {} rougel score: {}'.format(p,i,score))
    saver.save(sess,home_dir+'/model/just_lstm.ckpt')









