from src.com.zelkova.db import DButil

def __fetch_origin():
    db=DButil.DB("10.144.5.121",3306,"web_crawler","curidemo","web_crawler",charset='utf8')
    res=db.fetch_all("select title,content from pages where update_time>='2018-07-01 00:00:00'")
    return res

def __insert_tt(res:list):
    if res:
        # db=DButil.DB("10.108.233.216",3306,"xxb","mysql","nlp_test",charset='utf8')
        db=DButil.DB("10.108.233.216",3306,"xxb","mysql","nlp_test",charset='utf8')
        db.delete(" delete from pages ")
        db.update("insert into pages(title,content) values(%s,%s)",res)

def fetch_corpus(content='title'):
    db = DButil.DB("10.108.233.216", 3306, "xxb", "mysql", "nlp_test", charset='utf8')
    if content=='title':
        res=db.fetch_all("select title from pages")
    else:
        res=db.fetch_all("select content from pages")

    return res

if __name__=="__main__":
    __insert_tt(__fetch_origin())
