# from nltk.corpus import BracketParseCorpusReader
# from upenn_transfer import boson
# # reader=BracketParseCorpusReader('/home/lnn/Downloads/ctb_test','(.*nw)*(.*bn)*(.*mz)*(.*bc)*(.*wb)*')
# # reader=BracketParseCorpusReader('/home/lnn/Downloads/ctb_test','(.*mz)*')
# # tree = reader.parsed_sents()
# # for t in tree:
# #     s=t.leaves()
# #     for i,j in enumerate(s):
# #         k=t.leaf_treeposition(i)
# #         print("leaf {} index:{}".format(j,k))
# #         t[k[:-1]].set_label('l')
# #     # t[(3, 0, 1, 1, 0, 0, 0, 0)] = '(QP (m 多种))'#共同的父级index
# #     t=Tree.fromstring(t.__str__())
# #     print(t)
#
# # print(list(boson.Boson().seg(['阻碍ofo向阿里借款?滴滴未在借款过程中用过否决权'])))
# # print(list(boson.Boson().seg([' NoneChar 五年前的中国很不错'])))
# # import fool
# #
# # words,ners=fool.analysis('阿里 程序员 为什么都要起花名？连岳不群、田伯光都被占用了！ 阿里的花名文化真的不是说说而已 阿里花名的起源是什么？ 花名审核通过后还能修改吗? 花名能重复使用吗？ 见过哪些奇葩的花名？ 对于阿里起花名这件事网友怎么看？ 最后')
# # print(ners)
# # import pyltp
# # seg=pyltp.Segmentor()
# # seg.load_with_lexicon('/home/lnn/Documents/postag/ltp_data_v3.4.0/cws.model','/home/lnn/Documents/NLP/data/userdict.txt')
# # print(list(seg.segment('张勇马云'))
#
from upenn_transfer.phrase_trans_copy import stanford_parser

p=stanford_parser('对 外 开放')
print(p)
print(p[0])
