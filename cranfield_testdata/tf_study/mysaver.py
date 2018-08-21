import os
import tensorflow as tf

graph = tf.Graph()

with graph.as_default():
    # name scope 使得操作更清晰，在tensorboard也更清晰
    with tf.name_scope("variables"):
        global_step = tf.Variable(0, trainable=False, dtype=tf.int32, name='global_step')
        total_output = tf.Variable(0.0, trainable=False, dtype=tf.float32, name="global_output")
    with tf.name_scope("transformation"):
        with tf.name_scope("inputs"):
            a = tf.placeholder(dtype=tf.float32, shape=[None], name="a_inputs")
        with tf.name_scope("intermediate"):
            b = tf.reduce_prod(a, name="prod_b")
            c = tf.reduce_sum(a, name="sum_c")
        with tf.name_scope("outputs"):
            output = tf.add(b, c, name="output")
    # 全局更新操作
    with tf.name_scope("update"):
        # 自增
        update_total = total_output.assign_add(output)
        update_step = global_step.assign_add(1)
    # 汇总数据
    with tf.name_scope("summary"):
        avg = tf.div(update_total, tf.cast(update_step, tf.float32), name="avg")
        tf.summary.scalar(name="avvg_output_over_time", tensor=avg)
        tf.summary.scalar(name="sum_output_over_time ", tensor=update_total)
        tf.summary.scalar(name="output_over_time ", tensor=output)
    with tf.name_scope("globals_ops"):
        init = tf.global_variables_initializer()
        # 将所有汇总数据合并到一个op
        merge_summaries = tf.summary.merge_all()
#保存训练参数，在jupyter中__file__不可用；varlist为空，不能默认的保存所有变量，会报错
tfsaver = tf.train.Saver(var_list={'global_step':global_step},max_to_keep=5)

sess = tf.Session(graph=graph)
# 创建一个writer对象，用来保存汇总数据
writer = tf.summary.FileWriter(logdir='./chapter3a-gragh', graph=graph)

sess.run(init)


def run_gragh(input_tenser):
    feed_dict = {a: input_tenser}
    init_step = 0
    #确认是否存在检查点，参数是dir
    ckpt = tf.train.get_checkpoint_state('./ckpt')
    if ckpt and ckpt.model_checkpoint_path:
        tfsaver.restore(sess, ckpt.model_checkpoint_path)
        init_step = int(ckpt.model_checkpoint_path.split('-')[2])
    for i in range(init_step, 100):
        # 返回步数，汇总数据，不关心output
        _, step, summary = sess.run([output, update_step, merge_summaries], feed_dict=feed_dict)
        # 将汇总数据添加到writer对象中，step可使tensorboard可随时间对数据进行展示
        writer.add_summary(summary, global_step=step)
        tfsaver.save(sess, 'ckpt/tf-model', global_step=i)


run_gragh([1, 2, 3])
# 将事件保存到disk
writer.flush()
writer.close()
sess.close()
