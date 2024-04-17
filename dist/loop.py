import os
from _pydatetime import timedelta

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tiingo.restclient
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

user_input = st.text_input('Enter a Stock Symbol (e.g., NVDA.f):')

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

        st.subheader('Time Chart with 100 Value Mean Avg ')
        mone = df.close.rolling(100).mean()
        fig = plt.figure(figsize=(12, 8))
        plt.plot(mone)
        plt.xlabel('Time')
        plt.ylabel('Price')
        st.pyplot(fig)

        st.subheader('Closing Price vs Time Chart with 100 Value Mean Avg ')
        mone = df.close.rolling(100).mean()
        fig = plt.figure(figsize=(12, 8))
        plt.plot(mone)
        plt.plot(df.close)
        plt.xlabel('Time')
        plt.ylabel('Price')
        st.pyplot(fig)

        st.subheader('Closing Price vs Time Chart with 100 & 200 Value Mean Avg ')
        mone = df.close.rolling(100).mean()
        mtwo = df.close.rolling(200).mean()
        fig = plt.figure(figsize=(12, 8))
        plt.plot(mone, 'r', label='100')
        plt.plot(mtwo, 'g', label='200')
        plt.plot(df.close, 'b', label='Original')
        plt.legend()
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

        past_100Days = train.tail(100)

        final_df = pd.concat([past_100Days, test], ignore_index=True)

        input_data = scaler.fit_transform(final_df)

        x_test = []
        y_test = []

        for i in range(100, input_data.shape[0]):
            x_test.append(input_data[i - 100:i])
            y_test.append(input_data[i, 0])

        x_test, y_test = np.array(x_test), np.array(y_test)

        y_predicted = seq_model.predict(x_test)

        my_scaler = scaler.scale_
        scale_factor = 1 / my_scaler[0]
        y_predicted = y_predicted * scale_factor
        y_test = y_test * scale_factor

        st.subheader('Predicted vs Original')
        fig2 = plt.figure(figsize=(12, 8))
        plt.plot(y_test, 'b', label='Original Price')
        plt.plot(y_predicted, 'r', label='Predicted Price')
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
                <P> Thank you all for your incredible support</P>
                <p> Mungu mbele siku zote</p>

            </div>
            """,
            unsafe_allow_html=True,
        )

    except tiingo.restclient.RestClientError as e:
        st.error(f"Tiingo API Error: {str(e)}")

# Start the Streamlit app
import os
import psutil
import time

# Path to your log.py and loop.py scripts
log_script_path = r"C:\Users\I_am_Onesmus\Desktop\4th yr project\log.py"
loop_script_path = r"C:\Users\I_am_Onesmus\Desktop\4th yr project\loop.py"

# Path to your Streamlit Python script (with .py extension)
streamlit_script_path = r"C:\Users\I_am_Onesmus\Desktop\4th yr project\loop.py"
# Optional: Arguments to pass to your Streamlit script
arguments = []

# Function to check if Streamlit is already running

def is_streamlit_running():
    for proc in psutil.process_iter():
        try:
            if "streamlit" in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

# Check if Streamlit is already running
if is_streamlit_running():
    print("Streamlit is already running. Only one instance allowed.")
else:
    # Launch Streamlit application
    print("Launching Streamlit...")
    os.system(f"streamlit run {' '.join(arguments)} \"{streamlit_script_path}\"")

    # Wait for a while to check if Streamlit successfully started
    time.sleep(5)

    # Check again if Streamlit is running
    if is_streamlit_running():
        print("Streamlit launched successfully.")
    else:
        print("Failed to launch Streamlit.")



