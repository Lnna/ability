### 版本一
1. 训练集和测试集构造
x——words对应的ids
y——答案对应的开始和结束的位置对应的one-hot向量
按照7:2:1构造train、dev、test集合

2. 模型构造
pre：embeddings，vocab

model：
embed layer
lstm layer
softmax layer

对start和end分别使用一次上述模型



3. 训练和预测

#### 经验学习和总结
1. 数据量太大，一次性全部读入，非常消耗内存，尤其后面切分等数据成倍增加。
解决办法：
分批生成及传入需要格式的数据，最好读取时就分批读取?

统计答案在原文中找不到的情况



