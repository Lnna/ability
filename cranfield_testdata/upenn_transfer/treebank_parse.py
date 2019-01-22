from os import path
from nltk.corpus import BracketParseCorpusReader
# from upenn_transfer import boson
import boson
# reader=BracketParseCorpusReader('/home/lnn/Downloads/ctb_bracket','(.*nw)*(.*bn)*(.*mz)*(.*bc)*(.*wb)*')
def seg_pos_ctb(ctb_dir,fileids):
    reader = BracketParseCorpusReader(ctb_dir, fileids)
    #生成词语和词性元组
    # tree=reader.tagged_sents()
    #生成每个句子的树结构，对于部分数据如40.nw中五年来一句无法正确解析
    tree = reader.parsed_sents()
    print('tree len: {}'.format(len(tree)))

    seg_pos_sentences = []
    broken_parses=[]
    for s in tree:
        s=s.pos()

        if s and s!=[] and type(s[0])==tuple:
            s = [j if j[1] != '-NONE-' else (' NONE ','NONE') for j in s ]
            seg_pos_sentences.append(s)
        else:
            broken_parses.append(s)

    return seg_pos_sentences,broken_parses

def boson_seg(sentences):
    bseg=boson.Boson().seg(sentences)
    return list(bseg)

def ctb2boson_seg(ctb_sentences):
    boson_seg_list=[]
    text_list=[]
    for i,row in enumerate(ctb_sentences):
        text=''.join([i[0] for i in row])
        text_list.append(text)
        if (i>0 and i%100==0) or i==len(ctb_sentences)-1:
            boson_seg_list.extend(boson_seg(text_list))
            text_list=[]
    return boson_seg_list

def diff_sentences(ctb_sentences,boson_sentences):
    sames=0
    diff_dict={}
    for ctb,bos in zip(ctb_sentences,boson_sentences):
        ctext = [i[0] for i in ctb]
        btext = [i[0] for i in bos]
        # set 补集无序 diff.append((set(ctext).difference(set(btext)),set(btext).difference(set(ctext))))
        clen=len(ctext)
        blen=len(btext)
        if ctext==btext:
            sames+=1
            continue
        i=0
        j=0
        while i<clen and j <blen:
            if ctext[i]!=btext[j]:
                cw=ctext[i]
                bw=btext[j]
                if cw<bw:
                    t=i
                    while cw != bw and t<clen-1:
                        t+=1
                        cw+=ctext[t]
                    if diff_dict.get(bos[j],'')=='':
                        diff_dict[bos[j]]=str(ctb[i:t+1])
                    i=t+1
                    j+=1
                else:
                    t=j
                    while cw != bw and t<blen-1:
                        t += 1
                        bw += btext[t]
                    if diff_dict.get(bos[j],'')=='':
                        diff_dict[str(bos[j:t + 1])]=ctb[i]
                    j = t + 1
                    i+=1
            else:
                i+=1
                j+=1

    return diff_dict,sames

def diff_seg(ctb_sentences,boson_sentences):
    sames=0
    diff_bos=[]
    diff_ctb=[]

    for ctb,bos in zip(ctb_sentences,boson_sentences):
        ctext = [i[0] for i in ctb]
        btext = [i[0] for i in bos]
        # set 补集无序 diff.append((set(ctext).difference(set(btext)),set(btext).difference(set(ctext))))
        # 发现分词不同的词语，及对应的匹配
        # 方法：a，blist依次访问，有不一致的，就一直查找到一直的地方为止
        clen=len(ctext)
        blen=len(btext)
        if ctext==btext:
            sames+=1
            continue
        i=0
        j=0
        while i<clen and j <blen:
            if ctext[i]!=btext[j]:
                cw=ctext[i]
                bw=btext[j]
                ti=i
                tj=j
                while cw!=bw and ti<clen and tj<blen:
                    if len(cw)<len(bw):
                        ti+=1
                        cw+=ctext[ti]
                    elif len(cw)==len(bw):
                        ti+=1
                        tj+=1
                        cw+=ctext[ti]
                        bw+=btext[tj]
                    else:
                        tj+=1
                        bw+=btext[tj]
                bost=bos[j:tj+1]
                if type(bos[j:tj+1]) == tuple:
                    bost=[bos[j:tj+1]]
                cbtt=ctb[i:ti+1]
                if type(ctb[i:ti+1]) == tuple:
                    cbtt=[ctb[i:ti+1]]
                if bost not in diff_bos or cbtt not in diff_ctb:
                    diff_bos.append(bost)
                    diff_ctb.append(cbtt)
                i=ti+1
                j=tj+1
            else:
                i+=1
                j+=1

    return diff_bos,diff_ctb,sames

def diff_seg_pattern(diff_ctb,diff_bos):
    patterns_words={}
    patterns_counts={}

    for ctb,bos in zip(diff_ctb,diff_bos):

        pos_c=' + '.join([i[1] for i in ctb])
        pos_b=' + '.join([i[1] for i in bos])
        pat='{} = {}'.format(pos_c,pos_b)

        if patterns_words.get(pat,'')=='':
            patterns_words[pat]=[([i[0] for i in ctb],[i[0] for i in bos])]
            patterns_counts[pat]=1
        else:
            if ([i[0] for i in ctb],[i[0] for i in bos]) not in patterns_words[pat]:
                patterns_words[pat].extend([([i[0] for i in ctb],[i[0] for i in bos])])
            patterns_counts[pat]=int(patterns_counts[pat])+1

    return patterns_words,patterns_counts


if __name__=="__main__":
    home_dir = path.join(path.dirname(__file__), './')

    ctb_sentences,broken_parses = seg_pos_ctb(
        # '/home/lnn/Documents/ability/cranfield_testdata/upenn_transfer/otherbroken_ctb_test','(.*nw)*(.*bn)*(.*mz)*(.*bc)*(.*wb)*')
        path.join(home_dir,'normal_ctb_test'),'(.*nw)*(.*bn)*(.*mz)*(.*bc)*(.*wb)*')
        # '/home/lnn/Documents/ability/cranfield_testdata/otherbroken_ctb_test','(.*nw)*(.*bn)*(.*mz)*(.*bc)*(.*wb)*')

    boson_sentences = ctb2boson_seg(ctb_sentences)
    diff_bos,diff_ctb, sames = diff_seg(ctb_sentences, boson_sentences)
    patterns_words, patterns_counts=diff_seg_pattern(diff_ctb,diff_bos)
    ctb_plus=0
    bos_plus=0
    for k in patterns_counts.keys():
        p=str(k).split('=')
        if p[0].find('+')>=0 and p[1].find('+')==-1:
            ctb_plus+=1
        elif p[0].find('+')==-1 and p[1].find('+')>=0:
            bos_plus+=1
    with open('tmp_pattern_new.txt', mode='w') as f:
        f.write(
            'parse sentences: {},broken_parses: {},same seg sentences: {},diff words len: {},patterns num: {}\n'.format(
                len(ctb_sentences),len(broken_parses), sames, len(diff_ctb),len(patterns_counts)))
        f.write('pattern : ctb=bos , count , words(ctb,bos) \n')
        f.write('这种方式可以直接用(句法(pos word))替换原来(句法(pos word) (pos word))\n'
                'ctb + ctb = bos count:{}; ctb=bos+bos count:{}\n'
                .format(ctb_plus,bos_plus))
        patterns_sort=sorted(patterns_counts.items(),key=lambda d:d[1],reverse=True)
        for (pat,count) in patterns_sort:
            f.write('{} counts: {}\n'.format(pat,count))
            for i in range(0,len(patterns_words[pat]),5):
                f.write(str(patterns_words[pat][i:min(len(patterns_words[pat]),i+5)])+'\n')
            f.write('\n')
        f.close()

    f1=open('multictb2oneboson_pattern_new.txt',mode='w')
    f2=open('onectb2multiboson_pattern_new.txt',mode='w')
    f3=open('multictb2multiboson_pattern_new.txt',mode='w')
    f1.write('total num: {} \n'.format(ctb_plus))
    f2.write('total num: {} \n'.format(bos_plus))
    f3.write('total num: {} \n'.format(len(patterns_counts)-bos_plus-ctb_plus))
    for (pat,count) in patterns_sort:
        p = str(pat).split('=')
        if p[0].find('+') >= 0 and p[1].find('+') == -1:
            f1.write('{} counts: {}\n'.format(pat,count))
            f1.write(str(patterns_words[pat][0:5]) + '\n\n')

        elif p[0].find('+') == -1 and p[1].find('+') >= 0:
            f2.write('{} counts: {}\n'.format(pat, count))
            f2.write(str(patterns_words[pat][0:5]) + '\n\n')
        else:
            f3.write('{} counts: {}\n'.format(pat, count))
            f3.write(str(patterns_words[pat][0:5]) + '\n\n')
    f1.close()
    f2.close()
    f3.close()

