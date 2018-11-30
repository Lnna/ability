
from codes.dureader.model import RCModel
from codes.lacie_data import CleanData
import logging
def train():
    log_path='brc.log'
    logger = logging.getLogger("brc")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    if log_path:
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    else:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    data=CleanData()
    data.gen_train_data()
    model=RCModel(embed_dim=data.dim,vocab_size=len(data.embeddings),embeddings=data.embeddings)
    model.train(data,epochs=30,batch_size=32,save_dir='./models',save_prefix='dureader')

train()