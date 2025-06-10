import streamlit as st 
import pandas as pd

def show_overview():
    st.header("📋 데이터 미리보기")

    st.markdown(
    """
    이 대시보드는 타이타닉 승객 데이터 분석을 목적으로 합니다. 

    `train.csv`에는 실제 생존 여부가 포함되어 있으며, `test.csv`는 생존 여부가 없는 테스트 데이터입니다. 
    `gender_submission.csv`는 단순한 규칙(여성 생존, 남성 사망)에 기반한 예측값을 포함하고 있습니다.

    이 페이지에서는 원본 데이터와 병합된 예측 데이터를 미리 확인할 수 있습니다.
    """
    )

    # 데이터 불러오기
    train = st.session_state.get("train")
    test = st.session_state.get("test")
    gender = st.session_state.get("gender")
    test_merged = st.session_state.get("test_merged")

    # 탭 생성
    tabs = st.tabs(["Train 데이터", "Test + Prediction 데이터"])

    with tabs[0]:
        st.subheader("🚂 Train (Actual) 데이터")
        st.dataframe(train)

    with tabs[1]:
        st.subheader("🔮 Test (Predicted) 데이터")
        st.dataframe(test_merged)

