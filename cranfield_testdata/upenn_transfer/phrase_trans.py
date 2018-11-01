from nltk.corpus import BracketParseCorpusReader
from upenn_transfer.boson import Boson
from nltk.tree import Tree
def parse_trees(fileid):
    reader = BracketParseCorpusReader('/home/lnn/Downloads/ctb_test', fileid)
    tree = reader.parsed_sents()
    return tree

def analysis(fileid):
    trees=parse_trees(fileid)
    for t in trees:
        ctb=t.pos()
        boson=ctb2boson_seg(ctb)
        diff_index=sentence_diff(t,ctb,boson)#每一个不同找出来后，应立即更新树结构
        if diff_index[0][0]!='same':

            for pattern,ctb_index,bos_index in diff_index:
                if pattern=='one_ctb_multi_boson':
                    # stanford_parser
                    pass

                elif pattern=='multi_ctb_one_boson':
                    # find index and do it now
                    com=common_index(ctb_index)
                    t[com]='({} ({} {}))'.format(t[com]._label,boson[bos_index[0]][1],boson[bos_index[0]][0])
                    # t=Tree.fromstring(t.__str__())

                elif pattern=='multi_multi':
                    # leave it
                    pass

        # for i, l in enumerate(boson):
        #
        #     if l[0] != 'NONE':
        #         k = t.leaf_treeposition(i)
        #
        #         t[k[:-1]].set_label(l[1])


        print(t)

def common_index(ids):
    def common_seq(a,b):
        for i in range(min(len(a),len(b))):
            if a[i]!=b[i]:
                if i==0:
                    return None
                else:
                    return a[:i]
    com=ids[0]
    for i in range(1,len(ids)):
        com=common_seq(ids[i],com)
        if com==None:
            return ids[0][:-1]
    return com


def sentence_diff(tree,ctb,bos):
    pattern='same'
    diff_indexes=[]
    if len(ctb)==len(bos):#对于一些占位符的处理，how to do？
        return [(pattern,None,None)]
    else:
        ctext = [i[0] for i in ctb]
        btext = [i[0] for i in bos]
        # set 补集无序 diff.append((set(ctext).difference(set(btext)),set(btext).difference(set(ctext))))
        # 发现分词不同的词语，及对应的匹配
        # 方法：a，blist依次访问，有不一致的，就一直查找到一直的地方为止
        clen = len(ctext)
        blen = len(btext)
        i = 0
        j = 0
        while i < clen and j < blen:
            if ctb[i][1]=='-NONE-':
                i+=1
                continue
            if bos[j][0]=='NONE':
                j+=1
                continue
            if ctext[i] != btext[j]:
                cw = ctext[i]
                bw = btext[j]
                ti = i
                tj = j
                # while cw != bw and ti < clen and tj < blen:
                #     if len(cw) < len(bw):
                #         ti += 1
                #         if ctb[ti][1]!='-NONE-':
                #             cw += ctext[ti]
                #     elif len(cw) == len(bw):
                #         ti += 1
                #         tj += 1
                #         if ctb[ti][1]!='-NONE-':
                #             cw += ctext[ti]
                #         if bos[tj][0]!='-NONE-':
                #             bw += btext[tj]
                #     else:
                #         tj += 1
                #         if bos[tj][0]!='-NONE-':
                #             bw += btext[tj]
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
                bos_diff=list(range(j,tj+1))
                ctb_diff=[tree.leaf_treeposition(p) for p in range(i,ti+1)]
                if len(bos_diff)==1:
                    pattern='multi_ctb_one_boson'
                elif len(ctb_diff)==1:
                    pattern='one_ctb_multi_boson'
                else:
                    pattern='multi_multi'
                diff_indexes.append((pattern,ctb_diff, bos_diff))
                i = ti + 1
                j = tj + 1
            else:
                i += 1
                j += 1

    return diff_indexes


def ctb2boson_seg(ctb_pos):
    #这样有一个问题，可能boson分成一个词，但是ctb是用分隔符隔开了，就导致boson也分成了多个词
    # text = ''.join([i[0] for i in ctb_pos if i[1]!= '-NONE-'])
    text = ''.join([i[0] if i[1]!= '-NONE-' else ' NONE ' for i in ctb_pos])
    bseg=Boson().seg(text)
    return bseg[0]

analysis('chtb_1060.mz')