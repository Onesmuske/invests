import os
from _pydatetime import timedelta

from pandas_datareader import tiingo

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import streamlit as st
from datetime import datetime, timedelta
from tiingo import TiingoClient
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM

TIINGO_API_KEY = '09de77c9d958c8805b51ab9dc02c8670b254450c'

tiingo_config = {
    'session': True,
    'api_key': TIINGO_API_KEY,
}
client = TiingoClient(tiingo_config)

cur_date = datetime.now()
today = datetime.now()
end_date = (today - timedelta(days=-4)).strftime('%Y-%m-%d')

start = '2010-01-01'
end = (today - timedelta(days=-4)).strftime('%Y-%m-%d')
st.title('Smart invest by predicting market trends')

user_input = st.text_input('Enter a Stock Symbol (e.g., NVDA. Use US Companies):')

if user_input:
    try:

        df = client.get_dataframe(user_input, startDate=start, endDate=end_date)

        st.subheader('Stock Data')
        st.write(df.tail())
        st.write(df.describe())

        st.subheader('Closing Price VS Time Chart')
        fig = plt.figure(figsize=(12, 8))
        plt.plot(df.close)
        plt.xlabel('Time')
        plt.ylabel('Price')
        st.pyplot(fig)

        split_point = int(len(df) * 0.70)

        train = pd.DataFrame(df['close'][:split_point])
        test = pd.DataFrame(df['close'][split_point:])

        scaler = MinMaxScaler(feature_range=(0, 1))

        df_train_array = scaler.fit_transform(train)

        x_train = []
        y_train = []

        for i in range(100, df_train_array.shape[0]):
            x_train.append(df_train_array[i - 100:i])
            y_train.append(df_train_array[i, 0])

        x_train, y_train = np.array(x_train), np.array(y_train)

        seq_model = Sequential()

        seq_model.add(LSTM(units=50, activation='relu', return_sequences=True, input_shape=(x_train.shape[1], 1)))
        seq_model.add(Dropout(0.2))

        seq_model.add(LSTM(units=60, activation='relu', return_sequences=True))
        seq_model.add(Dropout(0.3))

        seq_model.add(LSTM(units=80, activation='relu', return_sequences=True))
        seq_model.add(Dropout(0.4))

        seq_model.add(LSTM(units=120, activation='relu'))
        seq_model.add(Dropout(0.5))

        seq_model.add(Dense(units=1))

        seq_model.compile(optimizer='adam', loss='mean_squared_error')
        seq_model.fit(x_train, y_train, epochs=3)

        # Predict next one year closing prices
        future_dates = pd.date_range(end_date, periods=365)
        future_dates_str = [date.strftime('%Y-%m-%d') for date in future_dates]

        last_100_days = df['close'].tail(100).values.reshape(-1, 1)
        scaled_last_100_days = scaler.transform(last_100_days)

        x_future = []
        for i in range(100):
            x_future.append(scaled_last_100_days[i:i+100])

        x_future = np.array(x_future)

        predicted_prices_scaled = seq_model.predict(x_future)
        predicted_prices = scaler.inverse_transform(predicted_prices_scaled)

        st.subheader('Predicted Closing Prices for Next One Year')
        fig2 = plt.figure(figsize=(12, 8))
        plt.plot(df.index[-100:], df['close'].tail(100), label='Last 100 Days')
        plt.plot(future_dates, predicted_prices, label='Predicted Prices')
        plt.xlabel('Time')
        plt.ylabel('Price')
        plt.legend()
        st.pyplot(fig2)

        st.write("<br>", unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)

        st.write(
            """
            <div style="position: absolute; bottom: 10px; right: 10px; text-align: right;">
                <p>Project Done by @Onesmus254</p>

            </div>
            """,
            unsafe_allow_html=True,
        )

    except tiingo.restclient.RestClientError as e:
        st.error(f"Tiingo API Error: {str(e)}")
