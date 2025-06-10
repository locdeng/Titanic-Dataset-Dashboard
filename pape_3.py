import streamlit as st
from utils.visualize import compare_actual_vs_predicted

def show_comparison():
    st.header("실제 생존 vs 예측 생존 비교")

    train = st.session_state.get("train")
    test_merged = st.session_state.get("test_merged")

    if train is not None and test_merged is not None:
        st.markdown("""
        아래 그래프는 훈련 데이터(`train.csv`)의 실제 생존 여부와
        테스트 데이터(`test.csv`) + 예측값(`gender_submission.csv`)의 결과를
        성별 기준으로 비교한 시각화입니다.
        """)

        fig = compare_actual_vs_predicted(train_df=train, test_df=test_merged)
        st.pyplot(fig)
    else:
        st.warning("train 또는 test_merged 데이터를 불러올 수 없습니다. main.py의 세션 상태를 확인하세요.")
