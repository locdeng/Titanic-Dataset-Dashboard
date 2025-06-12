import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from utils.visualize import survival_by_gender, survival_by_age


def gender_based_accuracy(train_df):
    predicted = train_df["Sex"].apply(lambda x: 1 if x == "female" else 0)
    actual = train_df["Survived"]
    correct = (predicted == actual).sum()
    accuracy = correct / len(train_df) * 100
    return accuracy


def show_comparison():
    st.title("📊 실제 vs 예측 생존 결과 비교")

    train = st.session_state.get("train")
    test = st.session_state.get("test")
    test_merged = st.session_state.get("test_merged")

    if train is None or test_merged is None:
        st.warning("데이터를 불러올 수 없습니다. main.py에서 세션 상태를 확인하세요.")
        return

    st.markdown("""
    이 페이지에서는 Train 데이터와 Test + Gender Submission 데이터를 비교하여
    예측 결과와 실제 생존 데이터 간의 차이를 분석합니다.
    """)

    # 1. 성별 분포 비교
    st.subheader("👥 성별 분포 비교")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Train 데이터**")
        fig = survival_by_gender(train, title="Train: 성별 생존/사망")
        st.pyplot(fig)

    with col2:
        st.markdown("**Test + Gender 데이터 (예측)**")
        fig = survival_by_gender(test_merged, title="Test: 성별 예측 결과")
        st.pyplot(fig)

    # 2. 연령 분포 비교
    st.subheader("🎂 나이 분포 비교")
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("**Train 데이터 생존자 연령 분포**")
        fig = survival_by_age(train, survived=True)
        st.pyplot(fig)

    with col4:
        st.markdown("**Test 데이터 예측 생존자 연령 분포**")
        fig = survival_by_age(test_merged, survived=True)
        st.pyplot(fig)

    # 3. 성별 기반 예측 정확도 평가
    st.subheader("✅ 성별 기반 예측 정확도 (Train 데이터)")
    accuracy = gender_based_accuracy(train)
    st.metric("예측 정확도", f"{accuracy:.2f}%")

    st.markdown(f"""
    - 이 분석은 gender_submission.csv 방식인
      \"여성은 생존, 남성은 사망\" 규칙을 Train 데이터에 적용한 것입니다.
    - 이 단순 규칙으로 Train 데이터에서 약 **{accuracy:.2f}%** 의 정확도를 얻을 수 있습니다.
    - 실제 성별 외 다른 요인도 생존에 영향을 주기 때문에 한계가 존재합니다.
    """)
