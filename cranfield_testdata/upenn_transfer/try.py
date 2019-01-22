from os import path
from nltk.corpus.reader.util import find_corpus_fileids
from nltk.data import FileSystemPathPointer
reg = '(.*nw)*(.*bc)*(.*mz)*(.*bn)*(.*wb)*'
ctb_dir='/home/lnn/Documents/ability/cranfield_testdata/upenn_transfer/normal_ctb_test'

ctb_dir = FileSystemPathPointer(ctb_dir)
fileids = find_corpus_fileids(root=ctb_dir, regexp=reg)
for fid in fileids:
    with open(path.join(ctb_dir,fid)) as f:
        s=f.read()
        if s.find('VV')>=0 or s.find('NN')>=0 or s.find('JJ')>=0:
        # if s.find('家喻户晓')>=0 and s.find('流行歌曲')>=0:
            print(fid)
