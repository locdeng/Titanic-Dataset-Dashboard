import streamlit as st
from streamlit_option_menu import option_menu
from utils.load_data import load_data
from utils.merge_data import merge_test, train_label
from page_1 import show_overview
from page_2 import analysis_home
from pape_3 import show_comparison


def main():
    st.title("🚢 Titanic Dataset Explorer")

    # Load and prepare data
    train_raw, test_raw, gender = load_data()
    train = train_label(train_raw)
    test_merged = merge_test(test_raw, gender)

    # Store in session_state for use in other pages
    st.session_state["train"] = train
    st.session_state["test"] = test_raw
    st.session_state["gender"] = gender
    st.session_state["test_merged"] = test_merged

    # Sidebar navigation
    with st.sidebar:
        selected = option_menu(
            menu_title="대시보드 메뉴",
            options=["데이터 개요", "생존 분석", "실제 vs 예측"],
            icons=["table", "bar-chart", "activity"],
            default_index=0
        )

    # Page routing
    if selected == "데이터 개요":
        show_overview()
    elif selected == "생존 분석":
        analysis_home()
    elif selected == "실제 vs 예측":
        show_comparison()
        
if __name__ == "__main__":
    main()
