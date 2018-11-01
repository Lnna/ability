import os,time
import json,requests
class Boson():
    def __init__(self,):
        pass

    def seg(self, sentences):
        seg_sens = []
        flg=False
        while flg==False:
            try:
                res = requests.post("http://139.99.124.20:8802/tag", json.dumps(sentences), timeout=5)
                if res.status_code == 200:
                    # print("boson seg succeed!")
                    flg = True
                    for row in res.json():
                        seg_sens.append([(i,j) for i,j in zip(row['word'],row['tag'])])
            except requests.Timeout:
                print("requests are timeout!!")
                time.sleep(100)
            except requests.exceptions.ConnectionError:
                print("requests.exceptions.ConnectionError")
                time.sleep(100)



        return seg_sens

