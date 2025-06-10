import pandas as pd
import streamlit as st 



@st.cache_data
def load_data():
    train = pd.read_csv("dataset/train.csv")
    test = pd.read_csv("dataset/test.csv")
    gender = pd.read_csv("dataset/gender_submisson.csv")
    
    return train, test, gender