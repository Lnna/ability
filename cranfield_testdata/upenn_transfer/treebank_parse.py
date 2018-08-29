from nltk.corpus import BracketParseCorpusReader
from upenn_transfer import boson
# reader=BracketParseCorpusReader('/home/lnn/Downloads/ctb_bracket','(.*nw)*(.*bn)*(.*mz)*(.*bc)*(.*wb)*')
def seg_pos_ctb(ctb_dir,fileids):
    reader = BracketParseCorpusReader(ctb_dir, fileids)

    tree = reader.parsed_sents()
    print('tree len: {}'.format(len(tree)))
    seg_pos_sentences = []
    for i in range(len(tree)):
        s = tree[i]. leaves()
        if s and s!=[] and type(s[0])==tuple:
            s = [j for j in s if j[1] != '-NONE-']
            seg_pos_sentences.append(s)
        else:
            s = [(j,'-NONE-') for j in s]
            seg_pos_sentences.append(s)
            print(s)
    return seg_pos_sentences

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
                    if diff_dict.get(btext[j],'')=='':
                        diff_dict[btext[j]]=str(ctext[i:t+1])
                    i=t+1
                    j+=1
                else:
                    t=j
                    while cw != bw and t<blen-1:
                        t += 1
                        bw += btext[t]
                    if diff_dict.get(btext[j],'')=='':
                        diff_dict[str(btext[j:t + 1])]=ctext[i]
                    j = t + 1
                    i+=1
            else:
                i+=1
                j+=1

    return diff_dict,sames



ctb_sentences=seg_pos_ctb('/home/lnn/Downloads/ctb_bracket','(.*nw)*')
boson_sentences=ctb2boson_seg(ctb_sentences)
diff,sames=diff_sentences(ctb_sentences,boson_sentences)
total_sentences=len(ctb_sentences)
with open('tmp_order.txt',mode='w') as f:
    f.write('total sentences: {},same seg sentences: {},diff words len: {},first boson text,next ctb text!\n'.format(total_sentences,sames,len(diff)))
    for bos,ctb in diff.items():
        f.write('{} {}\n'.format(bos,ctb))
        # f.write('{} \n'.format(row[1]))
        f.write('\n')
    f.close()

