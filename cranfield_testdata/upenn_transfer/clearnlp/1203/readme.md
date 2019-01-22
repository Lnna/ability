1. 分词和词性标注转换：
完成转化48414句，转化率在94%.

2. 短语结构树向依存句法树转换：
按照clearnlp转化句子44740,转化率92%
目前使用的短语中head的寻找规则head_rules是clearnlp准备的,剩余未识别部分参考[1]论文中提供的head_rule。
但还有部分未识别，比如VCP/VPT等。
存在问题：
１）VCP/VPT这种结构，在head_rule中没有提供，无法识别。而它是否对依存句法的转化准确性
有很大的影响不太清楚。
２）未转化成功的９％源于"No token in the tree"等clearnlp程序的error,暂不清楚原因。

3. 待讨论内容
关于这个工作的总体思路如下：
１）构建北大标注集下的ctb数据集，该数据集包含分词、词性标注和依存句法特征。
２）把转化后的ctb数据集作为依存句法的训练数据集，以此训练得到依存句法分析的深度学习模型，与现有的神经句法分析模型效果比较，验证其准确性。
３）对下游任务以关系抽取为例，利用上述学习到的模型，得到关系抽取数据集的依存句法特征，作用于关系抽取模型，验证其效果是否优于已有工作。

如果上述思路无误，有几点需要指导：
１）搜集了几篇神经依存句法分析的工作，是否值得参考？老师有没有推荐的工作？
[1] Yue Zhang and Stephen Clark. 2008. A tale of two parsers: Investigating and combining graphbased
and transition-based dependency parsing using beam-search. In EMNLP.
[2] Danqi Chen, Christopher D. Manning.A Fast and Accurate Dependency Parser using Neural Networks. In EMNLP 2014
[3] Easy-First Dependency Parsing with Hierarchical Tree LSTMs. 
[4]
２）下游任务中像关系抽取
3. 讨论内容：
１）分词和词性标注转换暂停
２）句法转换暂停
３）下游任务：关系抽取？
下有任务和当前转换要能结合，所以下游任务的限制条件：
中文数据集：关系抽取论文的数据集主要就是ＡＣＥ０４和０５，以及ｓｅｍｖａｌ，都是英文，中文目前没有
依存句法？
妈呀，又发现了这条链的问题了：
首先，依存句法做出来后，无法判断准确性，所以需要下游任务；
下游任务中不可能使用upenn数据集，当然如果使用stanford parser的话，还是可以用这套来转化。
但是如果下游任务中使用依存句法，即使他们用了stanford parser，我们为什么不直接使用ｂｏｓｏｎ分词，词性和
依存句法转换呢。




