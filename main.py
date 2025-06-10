import streamlit as st
from streamlit_option_menu import option_menu
from utils.load_data import load_data
from utils.merge_data import merge_test, train_label
from page_1 import show_overview
from page_2 import show_analysis
from pape_3 import show_comparison


st.title("🚢 Titanic Dataset Explorer")

st.markdown("""
### 🎯 프로젝트 개요
이 대시보드는 타이타닉호 침몰 사건의 승객 데이터를 바탕으로 생존 여부를 분석하고, 단순한 예측 모델과 실제 데이터를 비교하여 인사이트를 얻는 데 목적이 있습니다.

왼쪽 사이드바의 메뉴를 통해 분석 항목을 선택할 수 있습니다.
""")

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
        menu_title="📂 메뉴",
        options=["데이터 개요", "생존 분석", "실제 vs 예측"],
        icons=["table", "bar-chart", "activity"],
        default_index=0
    )

# Page routing
if selected == "데이터 개요":
    show_overview()
elif selected == "생존 분석":
    show_analysis()
elif selected == "실제 vs 예측":
    show_comparison()
