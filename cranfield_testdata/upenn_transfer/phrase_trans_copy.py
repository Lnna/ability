import time,re
from os import path
import requests
from nltk.corpus import BracketParseCorpusReader
# from upenn_transfer.boson import Boson
from boson import Boson
from nltk.corpus.reader.util import find_corpus_fileids
from nltk.tree import Tree
from nltk.data import FileSystemPathPointer
from stanfordcorenlp.corenlp import StanfordCoreNLP
home_dir=path.join(path.dirname(__file__),'./')
def parse_trees(dir,fileid):
    # reader = BracketParseCorpusReader('/home/lnn/Documents/ability/cranfield_testdata/upenn_transfer/new_ctb', fileid)
    reader = BracketParseCorpusReader(dir, fileid)
    tree = reader.parsed_sents()
    return tree

# nlp=StanfordCoreNLP(r'/home/lnn/Documents/postag/stanford-corenlp-full-2016-10-31/', lang='zh')
nlp=StanfordCoreNLP(r'/home/nana/Documents/stanford-corenlp-full-2016-10-31/', lang='zh')
def stanford_parser(sentence):
    flg=True
    while flg:

        try:
            parser=nlp.parse(sentence)
            flg=False
            tree = Tree.fromstring(parser.__str__())
            return tree

        except requests.exceptions.ConnectionError:
            print('stanfordparser connect error')
            time.sleep(60)

def last_parent(tree,index):
    if len(tree.leaves())==1:
        return ()
    leaf = tree.leaf_treeposition(index)[:-1]
    while len(tree[leaf[:-1]].leaves())==1:
        leaf=leaf[:-1]
    return leaf

def analysis(fileid):
    trees=parse_trees(fileid)
    new_trees=[]
    mod_seq_count=0
    for t in trees:
        ctb=t.pos()
        boson=ctb2boson_seg(ctb)
        pattern,leaf_diff,ctb_index,bos_index = sentence_diff(t, ctb, boson)  # 每一个不同找出来后，应立即更新树结构

        while pattern!='same':
            if pattern == 'one_ctb_multi_boson':
                # break
                # stanford_parser
                ctb_leaf=last_parent(t,ctb_index[0])
                # print(' '.join([i[0] for i in boson]))
                parser=stanford_parser(' '.join([i[0] for i in boson]))
                # print(parser)
                #在ｐａｒｓｅｒ中，可能不按照分割好的词语分词，比如：中国银行在ｃｔｂ和ｂｏｏｓｏｎ中都是一个，但在ｓｔａｎｆｏｒｄ中是中国　和银行
                #这种情况，找到要改变句法的词语在ｐａｒｓｅｒ中的ｉｎｄｅｘ,下面仍然存在纰漏，要改变句法的词语也可能被再次切分，此时直接略过，不做处理
                if len(parser.leaves())!=len(boson):
                    try:
                        pi=parser.leaves().index(boson[bos_index[0]][0])
                        mb = parser[common_index([parser.leaf_treeposition(pi+i) for i in range(0,len(bos_index))])]
                        co=''.join([parser[parser.leaf_treeposition(pi+i)[:-1]].__str__()  for i in range(0,len(bos_index))])
                    except:
                        break
                else:
                    mb=parser[common_index([parser.leaf_treeposition(i) for i in bos_index])]
                    co=''.join(parser[parser.leaf_treeposition(i)[:-1]].__str__()  for i in range(0,len(bos_index)))
                if len(mb.leaves())!=len(bos_index):
                    t[ctb_leaf]=co
                else:
                    t[ctb_leaf]=mb
                t = Tree.fromstring(t.__str__())

                ctb_copy = ctb
                ctb = ctb[:ctb_index[0]]
                if ctb_index != []:
                    for i in bos_index:
                        ctb.append(boson[i])
                    for i in range(ctb_index[-1] + 1, len(ctb_copy)):
                        ctb.append(ctb_copy[i])

            elif pattern == 'multi_ctb_one_boson':
                # this and same count:30077
                # find index and do it now
                com = common_index(leaf_diff)
                # print(t[com])
                if len(t[com].leaves())==len(ctb_index):
                    t[com] = '({} ({} {}))'.format(t[com]._label, boson[bos_index[0]][1], boson[bos_index[0]][0])
                    t=Tree.fromstring(t.__str__())

                else:
                    co=''.join([t[last_parent(t,i)].__str__() for i in ctb_index])
                    if t.__str__().find(co)>=0:
                        t=Tree.fromstring(t.__str__().replace(co,boson[bos_index[0]].__str__()))
                    else:
                        break
                ctb_copy = ctb
                ctb = ctb[:ctb_index[0]]
                if ctb_index != []:
                    ctb.append(boson[bos_index[0]])
                    for i in range(ctb_index[-1] + 1, len(ctb_copy)):
                        ctb.append(ctb_copy[i])

            elif pattern == 'multi_multi':
                # leave it
                break
            pattern, leaf_diff, ctb_index, bos_index = sentence_diff(t, ctb, boson)  # 每一个不同找出来后，应立即更新树结构
        if pattern=='same':
            mod_seq_count += 1
            for i, l in enumerate(boson):

                if l[0] != 'NONE':
                    k = t.leaf_treeposition(i)

                    t[k[:-1]].set_label(l[1])
        new_trees.append(t)
        # print(t)
    return new_trees,mod_seq_count

def analysis_v2(ctb_dir,fileid):
    trees=parse_trees(ctb_dir,fileid)
    new_trees=[]
    mmbroken_phrases={}
    mmbroken_trees=[]
    other_broken_trees=[]
    other_broken_phrase={}
    value_error=[]
    for t in trees:
        # print(t)
        ctb=t.pos()
        boson=ctb2boson_seg(ctb)
        pattern,leaf_diff,ctb_index,bos_index = sentence_diff(t, ctb, boson)  # 每一个不同找出来后，应立即更新树结构

        while pattern!='same':
            if pattern == 'one_ctb_multi_boson':
                ctb_leaf=t[last_parent(t,ctb_index[0])]

                parser=stanford_parser(' '.join([i[0] for i in boson]))

                try:
                    pi = parser.leaves().index(boson[bos_index[0]][0])
                    phrase = [parser[parser.leaf_treeposition(pi + i)] for i in range(0, len(bos_index))]
                    text = [boson[i][0] for i in bos_index]
                    while phrase != text and pi < len(parser.leaves()) - len(bos_index):
                        pi += 1
                        phrase = [parser[parser.leaf_treeposition(pi + i)] for i in range(0, len(bos_index))]
                    if phrase == text:
                        ci = common_index([parser.leaf_treeposition(pi + i) for i in range(0, len(bos_index))])
                        if len(parser[ci].leaves()) == len(bos_index):
                            if t.__str__().find(ctb_leaf.__str__())<0:
                                print('parse format not consistent!!!')
                                value_error.append(t)

                                break
                                # if t.__str__().replace('\n','').replace(' ','').find(ctb_leaf.__str__().replace('\n','').replace(' ','')) >= 0:
                                #     tstr=t.__str__().replace('\n','').replace(' ','').replace(ctb_leaf.__str__().replace('\n','').replace(' ',''), parser[ci].__str__().replace('\n','').replace(' ',''), 1)
                            else:
                                tstr = t.__str__().replace(ctb_leaf.__str__(), parser[ci].__str__(), 1)
                            t = Tree.fromstring(tstr)
                        else:
                            lpp = last_parent(parser, pi)
                            lpp_equal = True
                            rstr = parser[lpp].__str__()
                            for i in range(1, len(bos_index)):
                                if last_parent(parser, pi + i)[:-1] != lpp[:-1]:
                                    lpp_equal = False
                                    break
                                rstr += parser[last_parent(parser, pi + i)].__str__()
                            if lpp_equal:
                                tstr = t.__str__().replace(ctb_leaf.__str__(), rstr, 1)
                                t = Tree.fromstring(tstr)
                            else:
                                # just parse part of
                                if t.__str__().find(ctb_leaf.__str__()) < 0:
                                    print('parse format not consistent!!!')
                                    value_error.append(t)

                                    break
                                # print("new")
                                phrase_parser=stanford_parser(' '.join(text))
                                tstr = t.__str__().replace(ctb_leaf.__str__(), phrase_parser[0].__str__(), 1)
                                t = Tree.fromstring(tstr)
                                # other_broken_phrase.append((ctb_leaf.__str__(), parser[common_index(
                                #     [last_parent(parser, pi + i) for i in range(len(bos_index))])].__str__()))
                                # other_broken_trees.append(t)
                                # break

                    else:
                        # print("cannot find correct boson parse phrases")
                        key='{}: {}'.format(ctb[ctb_index[0]][0],' '.join(text))
                        if other_broken_phrase.get(key,0)==0:
                            other_broken_phrase[key]=1
                        else:
                            other_broken_phrase[key]=int(other_broken_phrase.get(key,0))+1
                        other_broken_trees.append(t)

                        break
                except :#奥斯特罗' is not in list;1.5 .被当做句号解析。
                    value_error.append(t)

                    break

                ctb_copy = ctb
                ctb = ctb[:ctb_index[0]]
                if ctb_index != []:
                    for i in bos_index:
                        ctb.append(boson[i])
                    for i in range(ctb_index[-1] + 1, len(ctb_copy)):
                        ctb.append(ctb_copy[i])

            elif pattern == 'multi_ctb_one_boson':
                com = common_index(leaf_diff)
                # print(t[com])
                if len(t[com].leaves())==len(ctb_index):
                    tstr=t.__str__().replace(t[com].__str__(),'({} ({} {}))'.format(t[com]._label, boson[bos_index[0]][1], boson[bos_index[0]][0]),1)

                    t=Tree.fromstring(tstr)

                else:
                    lpp = last_parent(t, ctb_index[0])
                    lpp_equal = True
                    rstr=[lpp]
                    for i in range(1, len(ctb_index)):
                        if last_parent(t, ctb_index[i])[:-1] != lpp[:-1]:
                            lpp_equal = False
                            break
                        rstr.append(last_parent(t, ctb_index[i]))
                    if lpp_equal:
                        tstr=t.__str__().replace(t[rstr[0]].__str__(),'({} {})'.format(boson[bos_index[0]][1],boson[bos_index[0]][0]),1)
                        for i in rstr[1:]:
                            tstr=tstr.replace(t[i].__str__(),'',1)
                        tstr=re.sub(r'(\n)+','\n',tstr)
                        t = Tree.fromstring(tstr)
                    else:
                        key = '{}: {}'.format(' '.join([ctb[i][0] for i in ctb_index]),boson[bos_index[0]][0])
                        if other_broken_phrase.get(key, 0) == 0:
                            other_broken_phrase[key] = 1
                        else:
                            other_broken_phrase[key] = int(other_broken_phrase[key]) + 1
                        other_broken_trees.append(t)
                        break
                ctb_copy = ctb
                ctb = ctb[:ctb_index[0]]
                if ctb_index != []:
                    ctb.append(boson[bos_index[0]])
                    for i in range(ctb_index[-1] + 1, len(ctb_copy)):
                        ctb.append(ctb_copy[i])

            elif pattern == 'multi_multi':
                key='{}: {}'.format(' '.join([ctb[i][0] for i in ctb_index]),' '.join([boson[i][0] for i in bos_index]))
                if mmbroken_phrases.get(key,0)==0:
                    mmbroken_phrases[key]=1
                else:
                    mmbroken_phrases[key]=int(mmbroken_phrases[key])+1
                mmbroken_trees.append(t)
                break
            pattern, leaf_diff, ctb_index, bos_index = sentence_diff(t, ctb, boson)  # 每一个不同找出来后，应立即更新树结构

        if pattern=='same':
            for i, l in enumerate(boson):

                if l[0] != 'NONE':
                    k = t.leaf_treeposition(i)

                    t[k[:-1]].set_label(l[1])
            new_trees.append(t)
        # print(t)
    return new_trees,mmbroken_phrases,mmbroken_trees,other_broken_trees,other_broken_phrase,value_error

def common_index(ids):
    def common_seq(a,b):
        for i in range(min(len(a),len(b))):
            if a[i]!=b[i]:
                if i==0:
                    return None
                else:
                    return a[:i]
        if len(a)<len(b):
            return a
        else:
            return b
    com=ids[0]
    for i in range(1,len(ids)):
        com=common_seq(ids[i],com)
        if com==None:
            return ids[0][:-1]
    return com


def sentence_diff(tree,ctb,bos):
    pattern='same'
    ctb_leaf_index=[]
    ctb_diff=[]
    bos_diff=[]
    # if len(ctb)==len(bos):#对于一些占位符的处理，how to do？
    #     return (pattern,ctb_leaf_index,ctb_diff,bos_diff)
    ctext = [i[0] for i in ctb]
    btext = [i[0] for i in bos]
    # 发现分词不同的词语，及对应的匹配
    # 方法：a，blist依次访问，有不一致的，就一直查找到一直的地方为止
    clen = len(ctext)
    blen = len(btext)
    i = 0
    j = 0
    while i < clen and j < blen:
        if ctb[i][1] == '-NONE-':
            i += 1
            continue
        if bos[j][0] == 'NONE':
            j += 1
            continue
        if ctext[i] != btext[j]:
            cw = ctext[i]
            bw = btext[j]
            ti = i
            tj = j
            while cw != bw and ti < clen and tj < blen:
                if len(cw) < len(bw):
                    ti += 1
                    cw += ctext[ti]
                elif len(cw) == len(bw):
                    ti += 1
                    tj += 1
                    cw += ctext[ti]
                    bw += btext[tj]
                else:
                    tj += 1
                    bw += btext[tj]
            bos_diff = list(range(j, tj + 1))
            ctb_diff=list(range(i, ti + 1))
            ctb_leaf_index = [tree.leaf_treeposition(p) for p in range(i, ti + 1)]
            if len(bos_diff) == 1:
                pattern = 'multi_ctb_one_boson'
            elif len(ctb_leaf_index) == 1:
                pattern = 'one_ctb_multi_boson'
            else:
                pattern = 'multi_multi'
            break

        else:
            i += 1
            j += 1
    return (pattern, ctb_leaf_index,ctb_diff, bos_diff)


def ctb2boson_seg(ctb_pos):
    #这样有一个问题，可能boson分成一个词，但是ctb是用分隔符隔开了，就导致boson也分成了多个词
    # text = ''.join([i[0] for i in ctb_pos if i[1]!= '-NONE-'])
    text = ''.join([i[0] if i[1]!= '-NONE-' else ' NONE ' for i in ctb_pos])
    bseg=Boson().seg(text)
    return bseg[0]

# new_trees,mod_count=analysis('chtb_0613.nw')
# print(new_trees)
def rules(normal_save_dir,mmbroken_dir,other_broken_dir,phrases_dir,value_error_dir):
    # ctb_dir = '/home/lnn/Downloads/new_ctb'
    # ctb_dir = '/home/lnn/Downloads/ctb_test'
    ctb_dir = path.join(home_dir,'ctb_bracket')
    # ctb_dir = path.join(home_dir,'ctb_test')
    # reg = 'chtb_0040.nw'
    reg = '(.*nw)*(.*bn)*(.*mz)*(.*bc)*(.*wb)*'
    ctb_dir = FileSystemPathPointer(ctb_dir)
    fileids = find_corpus_fileids(root=ctb_dir, regexp=reg)
    statis=[0,0,0,0]
    sum_broken_phrases={}
    sum_mmbrokens={}
    for fid in fileids:
        print(fid)
        normal_trees,mmbrokens,mmbroken_trees,other_brokens,broken_phrases,value_error=analysis_v2(ctb_dir,fid)
        statis[0]+=len(normal_trees)
        statis[1]+=len(other_brokens)
        statis[2]+=len(value_error)
        statis[3]+=len(mmbroken_trees)
        for k, v in broken_phrases.items():
            if sum_broken_phrases.get(k,0)==0:
                sum_broken_phrases[k]=v
            else:
                sum_broken_phrases[k]=sum_broken_phrases[k]+v
        for k, v in mmbrokens.items():
            if sum_mmbrokens.get(k,0)==0:
                sum_mmbrokens[k]=v
            else:
                sum_mmbrokens[k]=sum_mmbrokens[k]+v
        if len(value_error)>0:
            f = open(value_error_dir+'/'+fid, mode='w')
            for i in value_error:
                f.write('<S>\n')
                f.write('( {})\n'.format(i.__str__()))
                f.write('</S>\n')

            f.close()
        
        if len(normal_trees)>0:
            f = open(normal_save_dir+'/'+fid, mode='w')
            for i in normal_trees:
                f.write('<S>\n')
                f.write('( {})\n'.format(i.__str__()))
                f.write('</S>\n')
            f.close()
        if len(mmbroken_trees)>0:
            f = open(mmbroken_dir+'/'+fid, mode='w')
            for i in mmbroken_trees:
                f.write('<S>\n')
                f.write('( {})\n'.format(i.__str__()))
                f.write('</S>\n')
            f.close()
        if len(other_brokens)>0:
            f = open(other_broken_dir + '/' + fid, mode='w')
            for i in other_brokens:
                f.write('<S>\n')
                f.write('( {})\n'.format(i.__str__()))
                f.write('</S>\n')
            f.close()
    if len(sum_broken_phrases)>0:
        f = open(phrases_dir+'/broken_phrases.txt', mode='w')
        for k,v in sum_broken_phrases.items():
            f.write('{} {}\n'.format(k,v))
        f.close()
    if len(sum_mmbrokens) > 0:
        f = open(mmbroken_dir + '/mmbrokens.txt', mode='w')
        for k, v in sum_mmbrokens.items():
            f.write('{} {}\n'.format(k, v))
            
        f.close()

    print(statis)
if __name__=='__main__':
    # rules(path.join(home_dir,'normal_ctb_test'),
    #       path.join(home_dir,'mmbroken_ctb_test'),
    #       path.join(home_dir,'otherbroken_ctb_test'),
    #       path.join(home_dir,'broken_phrases'),
    #       path.join(home_dir,'value_error')
    #       )
    sum=0
    f=open(path.join(home_dir,'broken_phrases','broken_phrases.txt'),mode='r')
    phrases=[]
    for line in f.readlines():
        phrases.append((int(line.replace('\n','').split(' ')[-1]),line))
        if int(line.replace('\n','').split(' ')[-1])>=10:
            sum+=int(line.replace('\n','').split(' ')[-1])
    f.close()

    phrases.sort(key=lambda a:a[0],reverse=True)
    f=open(path.join(home_dir,'broken_phrases','broken_phrases.txt'),mode='w')
    for (v,k) in phrases:
        f.write(k)
    f.close()
    print(sum)
