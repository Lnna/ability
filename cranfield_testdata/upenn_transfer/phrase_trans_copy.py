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
home_dir='/home/lnn/Downloads/ctb_paper/transfer'
def parse_trees(dir,fileid):
    # reader = BracketParseCorpusReader('/home/lnn/Documents/ability/cranfield_testdata/upenn_transfer/new_ctb', fileid)
    reader = BracketParseCorpusReader(dir, fileid)
    tree = reader.parsed_sents()
    return tree

nlp=StanfordCoreNLP(r'/home/lnn/Downloads/postag/stanford-corenlp-full-2016-10-31/', lang='zh')
# nlp=StanfordCoreNLP(r'/home/nana/Documents/stanford-corenlp-full-2016-10-31/', lang='zh')
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


def analysis_v2(ctb_dir,fileid):
    trees=parse_trees(ctb_dir,fileid)
    new_trees=[]
    mmbroken_phrases={}
    mmtext=[]
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
                                t[last_parent(t, ctb_index[0])]=parser[ci].__str__()
                                tstr=t.__str__()
                                # tstr = t.__str__().replace(ctb_leaf.__str__(), parser[ci].__str__(), 1)
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
                                t[last_parent(t, ctb_index[0])]=rstr
                                # tstr = t.__str__().replace(ctb_leaf.__str__(), rstr, 1)
                                t = Tree.fromstring(t.__str__())

                            else:
                                # just parse part of
                                if t.__str__().find(ctb_leaf.__str__()) < 0:
                                    print('parse format not consistent!!!')
                                    value_error.append(t)

                                    break
                                # print("new")
                                t[last_parent(t, ctb_index[0])]=' '.join(['({} {})'.format(boson[i][1],boson[i][0]) for i in bos_index])
                                # phrase_parser=stanford_parser(' '.join(text))
                                # t[last_parent(t, ctb_index[0])] =phrase_parser[0].__str__()
                                # tstr = t.__str__().replace(ctb_leaf.__str__(), phrase_parser[0].__str__(), 1)
                                t = Tree.fromstring(t.__str__())
                                # other_broken_phrase.append((ctb_leaf.__str__(), parser[common_index(
                                #     [last_parent(parser, pi + i) for i in range(len(bos_index))])].__str__()))
                                # other_broken_trees.append(t)
                                # break

                    else:
                        # boson词语被stanford parser 拆分　print("cannot find correct boson parse phrases")
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
                    t[com]='({} ({} {}))'.format(t[com]._label, boson[bos_index[0]][1], boson[bos_index[0]][0])
                    # tstr=t.__str__().replace(t[com].__str__(),'({} ({} {}))'.format(t[com]._label, boson[bos_index[0]][1], boson[bos_index[0]][0]),1)

                    t=Tree.fromstring(t.__str__())

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
                        t[rstr[0]]='({} {})'.format(boson[bos_index[0]][1],boson[bos_index[0]][0])
                        # tstr=t.__str__().replace(t[rstr[0]].__str__(),'({} {})'.format(boson[bos_index[0]][1],boson[bos_index[0]][0]),1)
                        for i in rstr[1:]:
                            t[i]=''
                            # tstr=tstr.replace(t[i].__str__(),'',1)
                        # tstr=re.sub(r'(\n)+','\n',tstr)
                        t = Tree.fromstring(t.__str__())
                    else:
                        broken_flg=True
                        replace_id=ctb_index[0]
                        if (lpp[:-1]==com) ^ (last_parent(t, ctb_index[-1])[:-1]==com):
                            broken_flg = False

                            if lpp[:-1]==com:#与后面结构粘连
                                rightest=last_parent(t, ctb_index[len(ctb_index)-1])
                                replace_id=ctb_index[-1]
                                for i in range(len(ctb_index)-2,0,-1):
                                    tmp=last_parent(t, ctb_index[i])
                                    if tmp[:-1]!=rightest[:-1]:
                                        if tmp[:-1]!=com:
                                            broken_flg=True
                                        break
                            else:#与前面结构粘连

                                for i in range(1, len(ctb_index)):
                                    tmp = last_parent(t, ctb_index[i])
                                    if tmp[:-1] != lpp[:-1]:
                                        if tmp[:-1] != com:
                                            broken_flg = True
                                        break

                        #前后都有粘连,或者某一方内部还有层级粘连
                        #例如：1. (... x)x(x...)
                        # 2. ((x)(x))(x...)
                        # 3. x(x(x)...)
                        # 暂时搁置
                        if broken_flg:

                            key = '{}: {}'.format(' '.join([ctb[i][0] for i in ctb_index]),boson[bos_index[0]][0])
                            if other_broken_phrase.get(key, 0) == 0:
                                other_broken_phrase[key] = 1
                            else:
                                other_broken_phrase[key] = int(other_broken_phrase[key]) + 1
                            other_broken_trees.append(t)
                            break
                        else:
                            t[t.leaf_treeposition(replace_id)[:-1]]='({} {})'.format(boson[bos_index[0]][1],boson[bos_index[0]][0])
                            # tstr=t.__str__().replace(replace_text,'({} {})'.format(boson[bos_index[0]][1],boson[bos_index[0]][0]),1)
                            # for s in rstr:
                            #     tstr=tstr.replace(s,'',1)
                            # t=Tree.fromstring(tstr)
                            if replace_id==ctb_index[0]:
                                for i in range(len(ctb_index)-1,0,-1):
                                    # t.pop(t.leaf_treeposition(ctb_index[i])[:-1])
                                    # t[t.leaf_treeposition(ctb_index[i])[:-1]] = ''
                                    t[last_parent(t, ctb_index[i])]=''
                            else:
                                for i in range(len(ctb_index)-2,-1,-1):
                                    # t.pop(ctb_index[i])
                                    # t[t.leaf_treeposition(ctb_index[i])[:-1]] = ''
                                    t[last_parent(t, ctb_index[i])]=''

                            t=Tree.fromstring(t.__str__())

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
                mmtext.append(([ctb[i] for i in ctb_index],ctb,[boson[i] for i in bos_index],boson))
                break
            pattern, leaf_diff, ctb_index, bos_index = sentence_diff(t, ctb, boson)  # 每一个不同找出来后，应立即更新树结构

        if pattern=='same':
            for i, l in enumerate(boson):

                if l[0] != 'NONE':
                    k = t.leaf_treeposition(i)

                    t[k[:-1]].set_label(l[1])
            new_trees.append(t)
        # print(t)
    return new_trees,mmbroken_phrases,mmbroken_trees,other_broken_trees,other_broken_phrase,value_error,mmtext

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
def mm_out(res:list):
    return ['{}/{}'.format(i,j) for i,j in res]
def rules(normal_save_dir,mmbroken_dir,other_broken_dir,phrases_dir,value_error_dir):
    ctb_dir = '/home/lnn/Downloads/ctb_paper/origin/all_data'
    # ctb_dir = '/home/lnn/Downloads/ctb_bracket'
    # ctb_dir = home_dir
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
        normal_trees,mmbrokens,mmbroken_trees,other_brokens,broken_phrases,value_error,mmtext=analysis_v2(ctb_dir,fid)
        # break
        statis[0]+=len(normal_trees)
        statis[1]+=len(other_brokens)
        statis[2]+=len(value_error)
        statis[3]+=len(mmbroken_trees)
        # f=open('mmtext.txt',mode='a')
        # f.write('{}: \n'.format(fid))
        # for line in mmtext:
        #     f.write(' '.join(mm_out(line[0]))+'\n')
        #     f.write(' '.join(mm_out(line[1]))+'\n')
        #     f.write(' '.join(mm_out(line[2]))+'\n')
        #     f.write(' '.join(mm_out(line[3]))+'\n')
        #     f.write('\n')
        # f.write('\n\n')
        # f.close()
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

    rules(path.join(home_dir, 'normal_ctb_test'),
          path.join(home_dir, 'mmbroken_ctb_test'),
          path.join(home_dir, 'one2multi_otherbroken_ctb_test'),
          path.join(home_dir, 'broken_phrases'),
          path.join(home_dir, 'value_error')
          )
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
    # tree=stanford_parser("这个开发区中国著名风景旅游城。")
    # print(tree.__str__())

