# import numpy as np
#
# a=[[1],[2],[3]]
# b=np.array(a)[1:2,0]
# print(b[1:])
#
# a=[1]
# print(a*3)
#
# import tensorflow as tf
#
# print(tf.__version__)
# import os
# print(os.path.dirname(__file__))

import pos_methods as seg
segmentor=seg.LtpNlp()
s=segmentor.ltpseg("在俄陆军急需的先进战术无人机方面")
print(list(s))