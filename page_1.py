import streamlit as st

def show_overview(): 
    st.title("🚢 Titanic Dataset Explorer")
    
    st.subheader("데이터 개요")

    train = st.session_state.get("train")

    if train is None:
        st.warning("Train 데이터를 불러올 수 없습니다. main.py에서 세션 상태를 확인하세요.")
    

    st.markdown("""
        이 페이지는 Titanic 생존자 예측을 위한 학습 데이터(train.csv)의 전체적인 통계를 제공합니다.
        아래는 데이터의 주요 통계 지표입니다.
    """)

    # 총 인원 수
    total_passengers = len(train)
    total_survived = train['Survived'].sum()
    total_dead = total_passengers - total_survived

    # 나이 범위
    min_age = train['Age'].min()
    max_age = train['Age'].max()

    # 생존률
    survival_rate = total_survived / total_passengers * 100

    # 성별 분포
    sex_counts = train['Sex'].value_counts()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("총 승객 수", f"{total_passengers} 명")
        st.metric("생존자 수", f"{total_survived} 명")
        st.metric("사망자 수", f"{total_dead} 명")
        st.metric("생존률", f"{survival_rate:.2f}%")

    with col2:
        st.metric("최소 나이", f"{min_age} 세")
        st.metric("최대 나이", f"{max_age} 세")
        st.markdown("**성별 분포:**")
        for sex, count in sex_counts.items():
            st.write(f"{sex.capitalize()}: {count} 명")



