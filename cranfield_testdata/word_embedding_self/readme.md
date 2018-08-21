### skip-gram模型实现

参考：https://github.com/NELSONZHAO/zhihu/blob/master/skip_gram/Skip-Gram-Chinese-Corpus.ipynb

数据集:莱斯杯比赛数据
#### 数据预处理-执行data_pre_process.py得到lacie.pk

lacie-json:

article_title

article_content

question

去除标点符号和低频词

是否分词:
分词-ltp 不分词-字表示

高频词抽样：
之前对高频词抽样的理解有误，并不是删除原始样本中高频词的一部分，减少样本数量
而是单纯地以一定的概率删除高频词，那么被删除的高频词在原始样本中一定不会出现了

生成训练batch

#### 模型搭建及训练-执行full_demo.py

#### 测试

tsene图形化展示词语表示情况

