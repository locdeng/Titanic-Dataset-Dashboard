import streamlit as st 
import pandas as pd

def show_overview():
    st.header('프로젝트 개요')

    st.markdown(
    """
    이 대시보드는 타이타닉호 침몰 사건의 승객 데이터를 바탕으로 생존 여부를 분석하고, 단순한 예측 모델과 실제 데이터를 비교하여 인사이트를 얻는 데 목적이 있습니다.

    왼쪽 사이드바의 메뉴를 통해 분석 항목을 선택할 수 있습니다. 

    `train.csv`에는 실제 생존 여부가 포함되어 있으며, `test.csv`는 생존 여부가 없는 테스트 데이터입니다. 
    `gender_submission.csv`는 단순한 규칙(여성 생존, 남성 사망)에 기반한 예측값을 포함하고 있습니다.

    이 페이지에서는 원본 데이터와 병합된 예측 데이터를 미리 확인할 수 있습니다.
    
    왼쪽 사이드바의 메뉴를 통해 분석 항목을 선택할 수 있습니다. 
    """
    )

    # 데이터 불러오기
    train = st.session_state.get("train")
    test = st.session_state.get("test")
    gender = st.session_state.get("gender")
    test_merged = st.session_state.get("test_merged")

    # 탭 생성
    tabs = st.tabs(["Train 데이터", "Test 데이터","Gender_Submission 데이터터", " Test + Gender_Submission 데이터"])

    with tabs[0]:
        # st.subheader("🚂 Train (Actual) 데이터")
        st.dataframe(train)
    
    with tabs[1]:
        st.dataframe(test)
        
    with tabs[2]:
        st.dataframe(gender)

    with tabs[3]:
        # st.subheader("🔮 Test (Predicted) 데이터")
        st.dataframe(test_merged)

