import streamlit as st
from utils.visualize import survival_by_gender, survival_by_age
from utils.merge_data import merge_test
from streamlit_option_menu import option_menu


def train_analysis():
    # st.header("생존 분석 (Train 데이터 기반)")

    train = st.session_state.get("train")

    if train is not None:
        tabs = st.tabs(["성별 생존자 수", "나이 분포"])

        with tabs[0]:
            st.subheader("성별에 따른 생존 여부")
            fig = survival_by_gender(train, title='Survival by Gender')
            st.pyplot(fig)

        with tabs[1]:
            st.subheader("생존자와 사망자의 나이 분포")
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**🟩 생존자 나이 분포**")
                fig = survival_by_age(train, survived=True)
                st.pyplot(fig)

            with col2:
                st.markdown("**🟥 사망자 나이 분포**")
                fig = survival_by_age(train, survived=False)
                st.pyplot(fig)
    else:
        st.warning("Train 데이터를 불러올 수 없습니다. main.py에서 세션 상태를 확인하세요.")
        
def test_analysis():
    # st.header("생존 분석 (test + gender_submission  데이터 기반)")

    merged_test = st.session_state.get("test_merged")

    if merged_test is not None:
        tabs = st.tabs(["성별 생존자 수", "나이 분포"])

        with tabs[0]:
            st.subheader("성별에 따른 예측 생존 여부")
            fig = survival_by_gender(merged_test, title='Predicted Survival by Gender')
            st.pyplot(fig)

        with tabs[1]:
            st.subheader("예측 생존자와 사망자의 나이 분포")
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**🟩 에측 생존자 나이 분포**")
                fig = survival_by_age(merged_test, survived=True)
                st.pyplot(fig)

            with col2:
                st.markdown("**🟥 예측 사망자 나이 분포**")
                fig = survival_by_age(merged_test, survived=False)
                st.pyplot(fig)
    else:
        st.warning("Train 데이터를 불러올 수 없습니다. main.py에서 세션 상태를 확인하세요.")

def analysis_home():
    st.header("생존 분석")
    selected = option_menu(
        None,
        ["train 데이터 기반", "test + gender_submission  데이터 기반"],
        # icons=["house", "bar-chart", "file-spreadsheet", "map"],
        # menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        # styles={
        #     "container": {
        #         "padding": "0!important",
        #         "background-color": "#fafafa",
        #     },  # fafafa #6F92F7
        #     "icon": {"color": "orange", "font-size": "25px"},
        #     "nav-link": {
        #         "font-size": "18px",
        #         "text-align": "left",
        #         "margin": "0px",
        #         "--hover-color": "#eee",
        #     },
        #     "nav-link-selected": {"background-color": "green"},
        # },
    )

    if selected == "train 데이터 기반":
        train_analysis()
    elif selected == "test + gender_submission  데이터 기반":
        test_analysis()
    