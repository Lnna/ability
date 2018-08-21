from keras.layers import LSTM,Dense,TimeDistributed
from keras.models import Sequential

time_step=2
feature=10
hidden_feature=5
dense_feature=1
model=Sequential()
model.add(LSTM(units=hidden_feature,input_shape=(time_step,feature),return_sequences=True))
model.add(TimeDistributed(Dense(units=dense_feature)))
print(model.summary())

# ______________________return_sequences=False_____________________
# Layer (type)                 Output Shape              Param #
# =================================================================
# lstm_1 (LSTM)                (None, 5)                 140
# =================================================================

# ______________________return_sequences=True______________________
# Layer (type)                 Output Shape              Param #
# =================================================================
# lstm_1 (LSTM)                (None, 2, 5)              320
# _________________________________________________________________
# time_distributed_1 (TimeDist (None, 2, 1)              6
# =================================================================