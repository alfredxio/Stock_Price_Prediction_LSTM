import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as data
from keras.models import load_model
import streamlit as st

start ='2010-01-01'
#end= '2022-10-31'

end = st.date_input("Enter end date")

st.title('Stock Price Prediction')

user_input=st.text_input('Enter Stock Ticker','AAPL')
df=data.DataReader(user_input,'yahoo',start,end)

#Describing the Data
st.subheader('Data from 2010 - 2022')
st.write(df.describe())


#Visualizations
st.subheader('ClosingPrice vs Time Chart')
fig=plt.figure(figsize=(12,6))
plt.plot(df.Close)
st.pyplot(fig)

st.subheader('ClosingPrice vs Time Chart with 100 Mean Average')
ma100=df.Close.rolling(100).mean()
fig=plt.figure(figsize=(12,6))
plt.plot(ma100,'r')
plt.plot(df.Close,'g')
st.pyplot(fig)

st.subheader('ClosingPrice vs Time Chart with 100 & 200 Mean Average')
ma200=df.Close.rolling(200).mean()
fig=plt.figure(figsize=(12,6))
plt.plot(ma100,'r')
plt.plot(ma200,'g')
plt.plot(df.Close,'b')
st.pyplot(fig)


'''
now we split data to train and test
70:30
'''

data_training=pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
data_testing =pd.DataFrame(df['Close'][int(len(df)*0.70):int(len(df))])

'''
we will scale down data between 0 and 1 using minmax scaler
sklearn provides tool for statistics
'''
from sklearn.preprocessing import MinMaxScaler
scaler= MinMaxScaler(feature_range=(0,1))

data_training_array=scaler.fit_transform(data_training)


#Load the model
model=load_model('keras_model.h5')

#Testing part
past_100_days=data_training.tail(100)
final_df =past_100_days.append(data_testing, ignore_index=True)
input_data=scaler.fit_transform(final_df)


x_test=[]
y_test=[]

for i in range(100, input_data.shape[0]):
    x_test.append(input_data[i-100: i])
    y_test.append(input_data[i, 0])

x_test, y_test =np.array(x_test), np.array(y_test)

y_predicted=model.predict(x_test)
scaler=scaler.scale_

scale_factor=1/scaler[0]
y_predicted=y_predicted*scale_factor
y_test=y_test*scale_factor

st.subheader('Predicted v/s Original Graph')

#final graph

fig2=plt.figure(figsize=(12,6))
plt.plot(y_test, 'b', label='Original Price')
plt.plot(y_predicted, 'r', label='Predicted Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
st.pyplot(fig2)