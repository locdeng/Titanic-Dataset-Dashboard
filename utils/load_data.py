import pandas as pd
import streamlit as st 



@st.cache_data
def load_data():
    train = pd.read_csv("dataset/train.csv", encoding= "utf-8")
    test = pd.read_csv("dataset/test.csv", encoding= "utf-8")
    gender = pd.read_csv("dataset/gender_submission.csv", encoding= "utf-8")
    
    return train, test, gender