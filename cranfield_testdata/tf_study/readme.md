1. jupyter使用
-启动服务：jupyter notebook，在浏览器可以使用
-创建jupyter notebook格式的代码文件

2. tensorboard使用
执行tf.summary.filewriter('event-path',sess.graph)
控制台输入：tensorboard --logdir=event-graph
打开浏览器localhost:6006

3. 查看库的版本号
eg：tensorflow.__version__

4. 统计一个程序的时间花销：
import time
start=time.time()
...
...
end=time.time()

5. sorted()使用
对dict的使用：sorted(dict.items(),lambda d: d[1])
第一个参数是可迭代的值，第二个参数是排序参照的主键

6. list of tuples convert to lists:built-in func
map(list,zip(*[sth]))

zip() in conjunction with the * operator can be used to unzip a list:
>>> zip((1,3,5),(2,4,6))
[(1, 2), (3, 4), (5, 6)]
>>> zip(*[(1, 2), (3, 4), (5, 6)])
[(1, 3, 5), (2, 4, 6)]