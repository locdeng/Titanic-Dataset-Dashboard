import streamlit as st
from streamlit_option_menu import option_menu
from utils.load_data import load_data
from utils.merge_data import merge_test, train_label
from page_1 import show_overview
from page_2 import train_analysis
from pape_3 import show_model_prediction
from page_4 import show_data


def main():
    # st.title("🚢 Titanic Dataset Explorer")

    # Load and prepare data
    train_raw, test_raw = load_data()
    train = train_label(train_raw)
    

    # Store in session_state for use in other pages
    st.session_state["train"] = train
    st.session_state["test"] = test_raw

    # Sidebar navigation
    with st.sidebar:
        selected = option_menu(
            menu_title="대시보드 메뉴",
            options=["데이터 개요", "Train 데이터 분석", "예측 모델 및 평가가", "원본 데이터 보기"],
            icons=["table", "bar-chart", "activity"],
            default_index=0
        )

    # Page routing
    if selected == "데이터 개요":
        show_overview()
    elif selected == "Train 데이터 분석":
        train_analysis()
    elif selected == "예측 모델 및 평가가":
        show_model_prediction()
    elif selected == "원본 데이터 보기":
        show_data()
        
if __name__ == "__main__":
    main()
