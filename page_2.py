import streamlit as st
from utils.visualize import survival_by_gender, survival_by_age

def show_analysis():
    st.header("📊 생존 분석 (Train 데이터 기반)")

    train = st.session_state.get("train")

    if train is not None:
        tabs = st.tabs(["성별 생존자 수", "나이 분포"])

        with tabs[0]:
            st.subheader("👥 성별에 따른 생존 여부")
            fig = survival_by_gender(train, title="Train 데이터: 성별 생존자 수")
            st.pyplot(fig)

        with tabs[1]:
            st.subheader("🎂 생존자와 사망자의 나이 분포")
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

