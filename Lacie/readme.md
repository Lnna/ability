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



