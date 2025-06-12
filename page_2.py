import streamlit as st
from utils.visualize import (
    survival_by_gender,
    survival_by_age,
    histogram_by_age_percent,
    plot_survival_vs_death_pie
)
from streamlit_option_menu import option_menu

def train_analysis():
    st.markdown("### ✅ Train 데이터 기반 생존 및 사망 분석")

    train = st.session_state.get("train")
    if train is None:
        st.warning("Train 데이터를 불러올 수 없습니다. main.py에서 세션 상태를 확인하세요.")
        return

    tabs = st.tabs(["성별 생존자 맟 사망자 수", "생존 및 사망 나이 분포", "연령별 생존 및 사망 비율"])

    with tabs[0]:
        st.subheader("👥 성별에 따른 생존 여부")
        fig = survival_by_gender(train, title='Survival by Gender')
        st.pyplot(fig)

    with tabs[1]:
        st.subheader("🎂 나이 분포 분석")
        age_range = st.slider("나이 범위 선택", 0, 80, (0, 80))
        chart_type = st.selectbox("표시할 그래프 종류", ["KDE", "Histogram (비율)"])
        
        with st.expander("📘 Histogram이란? 설명 보기"):
            st.markdown("""
            Histogram은 데이터를 구간(Bin)으로 나누어 각 구간에 속하는 데이터 수를 막대 그래프로 나타낸 것입니다.  
            Titanic 데이터에서는 나이를 일정 구간으로 나누고, 각 구간에 해당하는 생존자/사망자의 **비율(%)** 을 시각화합니다.

            - 막대가 높을수록 해당 나이 구간에 더 많은 사람이 있음을 의미합니다.  
            - 이 Histogram은 **사람 수가 아닌, 전체 대비 비율(%)** 을 표시합니다.  
            - KDE와 달리 Histogram은 실제 빈도를 직접적으로 보여줍니다.
        """)

        with st.expander("📘 KDE란? 설명 보기"):
            st.markdown("""
            KDE는 커널 밀도 추정 방식으로 나이 분포를 부드러운 곡선으로 나타냅니다.  
            곡선이 높을수록 해당 나이대에 사람이 많이 분포해 있다는 의미이며,  
            실제 사람 수가 아니라 **상대적 확률 밀도(Density)** 를 보여줍니다.
            """)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**🟩 생존자 나이 분포**")
            fig = survival_by_age(train, survived=True, age_range=age_range) if chart_type == "KDE" \
                else histogram_by_age_percent(train, survived=True, age_range=age_range)
            st.pyplot(fig)

        with col2:
            st.markdown("**🟥 사망자 나이 분포**")
            fig = survival_by_age(train, survived=False, age_range=age_range) if chart_type == "KDE" \
                else histogram_by_age_percent(train, survived=False, age_range=age_range)
            st.pyplot(fig)

    with tabs[2]:
        st.markdown("""
            이 도넛 차트는 각 연령대(10세 단위)별로 타이타닉 승객들의 **생존자 비율**과 **사망자 비율**을 시각화한 것입니다.

            - **왼쪽 차트**는 생존한 승객들의 연령 분포를 나타냅니다.  
            - **오른쪽 차트**는 사망한 승객들의 연령 분포를 보여줍니다.  
            - 각 색상은 동일한 연령대를 의미하며, **비율이 작더라도 모든 구간이 표시됩니다.**

            이를 통해 특정 연령대의 생존률 경향을 한눈에 파악할 수 있습니다.
        """)
        fig = plot_survival_vs_death_pie(train)
        st.pyplot(fig)
        
        st.markdown("ℹ️ **1% 미만의 비율은 차트에서 생략될 수 있습니다.** 범례를 참고하세요.")


# def test_analysis():
#     st.markdown("### 🤖 Test + Gender Submission 기반 예측 생존 및 사망 분석")

#     merged_test = st.session_state.get("test_merged")
#     if merged_test is None:
#         st.warning("test_merged 데이터를 불러올 수 없습니다. main.py에서 세션 상태를 확인하세요.")
#         return

#     tabs = st.tabs(["성별 생존자 맟 사망자 수", "생존 및 사망 나이 분포", "연령별 생존 및 사망 비율"])

#     with tabs[0]:
#         st.subheader("👥 성별에 따른 예측 생존 여부")
#         fig = survival_by_gender(merged_test, title='Predicted Survival by Gender')
#         st.pyplot(fig)

#     with tabs[1]:
#         st.subheader("🎂 예측 나이 분포 분석")
#         age_range = st.slider("나이 범위 선택", 0, 80, (0, 80))
#         chart_type = st.selectbox("표시할 그래프 종류", ["KDE", "Histogram (비율)"], key="test_age_type")
        
#         with st.expander("📘 Histogram이란? 설명 보기"):
#             st.markdown("""
#             Histogram은 데이터를 구간(Bin)으로 나누어 각 구간에 속하는 데이터 수를 막대 그래프로 나타낸 것입니다.  
#             Titanic 데이터에서는 나이를 일정 구간으로 나누고, 각 구간에 해당하는 생존자/사망자의 **비율(%)** 을 시각화합니다.

#             - 막대가 높을수록 해당 나이 구간에 더 많은 사람이 있음을 의미합니다.  
#             - 이 Histogram은 **사람 수가 아닌, 전체 대비 비율(%)** 을 표시합니다.  
#             - KDE와 달리 Histogram은 실제 빈도를 직접적으로 보여줍니다.
#         """)

#         with st.expander("📘 KDE란? 설명 보기"):
#             st.markdown("""
#             KDE는 커널 밀도 추정 방식으로 나이 분포를 부드러운 곡선으로 나타냅니다.  
#             곡선이 높을수록 해당 나이대에 사람이 많이 분포해 있다는 의미이며,  
#             실제 사람 수가 아니라 **상대적 확률 밀도(Density)** 를 보여줍니다.
#             """)

#         col1, col2 = st.columns(2)

#         with col1:
#             st.markdown("**🟩 예측 생존자 나이 분포**")
#             fig = survival_by_age(merged_test, survived=True, age_range=age_range) if chart_type == "KDE" \
#                 else histogram_by_age_percent(merged_test, survived=True, age_range=age_range)
#             st.pyplot(fig)

#         with col2:
#             st.markdown("**🟥 예측 사망자 나이 분포**")
#             fig = survival_by_age(merged_test, survived=False, age_range=age_range) if chart_type == "KDE" \
#                 else histogram_by_age_percent(merged_test, survived=False, age_range=age_range)
#             st.pyplot(fig)
#     with tabs[2]:
#         st.markdown("""
#             이 도넛 차트는 각 연령대(10세 단위)별로 타이타닉 승객들의 **생존자 비율**과 **사망자 비율**을 시각화한 것입니다.

#             - **왼쪽 차트**는 생존한 승객들의 연령 분포를 나타냅니다.  
#             - **오른쪽 차트**는 사망한 승객들의 연령 분포를 보여줍니다.  
#             - 각 색상은 동일한 연령대를 의미하며, **비율이 작더라도 모든 구간이 표시됩니다.**

#             이를 통해 특정 연령대의 생존률 경향을 한눈에 파악할 수 있습니다.
#         """)
#         fig = plot_survival_vs_death_pie(merged_test)
#         st.pyplot(fig)
#         st.markdown("ℹ️ **1% 미만의 비율은 차트에서 생략될 수 있습니다.** 범례를 참고하세요.")


# def analysis_home():
#     selected = option_menu(
#         None,
#         ["실제 생존 결과", "예측 생존 결과"],
#         default_index=0,
#         orientation="horizontal",
#         styles={
#             "container": {"padding": "0!important", "background-color": "#fafafa"},
#             "icon": {"color": "orange", "font-size": "25px"},
#             "nav-link": {
#                 "font-size": "18px",
#                 "text-align": "left",
#                 "margin": "0px",
#                 "--hover-color": "#eee",
#                 "color": "#212121"
#             },
#             "nav-link-selected": {
#                 "background-color": "green",
#                 "color":"white"
#             },
#         },
#     )

#     if selected == "실제 생존 결과":
#         train_analysis()
#     elif selected == "예측 생존 결과":
#         test_analysis()
