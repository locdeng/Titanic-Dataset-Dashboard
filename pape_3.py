import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import plotly.figure_factory as ff
import plotly.graph_objects as go
from utils.load_data import load_data  
from utils.visualize import searchable_dataframe


def show_model_prediction():
    st.title("🚢 타이타닉 생존자 예측")

    train, test = load_data()

    with st.spinner("🔄 데이터 전처리 및 모델 학습 중..."):

        # Add dummy column & combine
        test['Survived'] = -1
        combined = pd.concat([train, test], sort=False)

        cat_cols = ['Sex', 'Embarked', 'Ticket', 'Cabin']
        for col in cat_cols:
            combined[col] = combined[col].astype(str)
            le = LabelEncoder()
            combined[col] = le.fit_transform(combined[col])

        combined['Age'].fillna(combined['Age'].median(), inplace=True)
        combined['Fare'].fillna(combined['Fare'].median(), inplace=True)
        combined['Embarked'].fillna(combined['Embarked'].mode()[0], inplace=True)

        train_processed = combined[combined['Survived'] != -1]
        test_processed = combined[combined['Survived'] == -1]

        X = train_processed.drop(['Survived', 'PassengerId', 'Name'], axis=1)
        y = train_processed['Survived']
        X_test_final = test_processed.drop(['Survived', 'PassengerId', 'Name'], axis=1)

        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_val)

        acc = accuracy_score(y_val, y_pred)

        test_processed['Survived'] = model.predict(X_test_final)
        result = test_processed.drop(columns=['Survived']).copy()
        result.insert(1, 'Survived', test_processed['Survived'])

    # ========== Tabs ==========
    tabs = st.tabs([
        "📊 정확도 및 리포트", 
        "🔍 Confusion Matrix", 
        "🌲 Feature Importance", 
        "📤 테스트 예측 결과"
    ])

    with tabs[0]:
        st.markdown("🎯 정확도 (Accuracy)")
        st.markdown("정확도는 전체 샘플 중 올바르게 예측한 비율입니다.")
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=acc * 100,
            number={'suffix': "%"},
            title={'text': "모델 정확도"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "green"},
                'steps': [
                    {'range': [0, 60], 'color': "#ffcccc"},
                    {'range': [60, 80], 'color': "#fff0b3"},
                    {'range': [80, 100], 'color': "#d4f4dd"},
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 3},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("📄 분류 리포트 (Classification Report)")
        st.markdown("""
        이 표는 각 클래스 (0=사망, 1=생존)에 대한 정밀도(Precision), 재현율(Recall), F1-score, 샘플 수를 보여줍니다.
        - **Precision**: 예측이 얼마나 정확했는지  
        - **Recall**: 실제 값을 얼마나 잘 잡았는지  
        - **F1-score**: Precision과 Recall의 조화 평균 
        - **Support**: 해당 클래스에 실제로 속하는 샘플 수입니다.

        > 예: support가 0 클래스에서 105라면, 실제로 검증 세트에 사망한 사람이 105명 있다는 뜻입니다. 
        """)
        report_dict = classification_report(y_val, y_pred, output_dict=True)
        report_df = pd.DataFrame(report_dict).transpose().round(2)
        st.dataframe(
            report_df.style
            .format(precision=2)
            .background_gradient(cmap="YlGn")
        )

    
    with tabs[1]:

        st.markdown("""
        혼동 행렬(Confusion Matrix)은 모델이 실제 값을 얼마나 잘 예측했는지를 시각적으로 보여줍니다.  
        - 좌측 축은 **실제 클래스**, 상단 축은 **예측 클래스**입니다.
        - 완벽한 예측일 경우, 모든 값은 대각선에 위치합니다.
        """)
        cm = confusion_matrix(y_val, y_pred)
        labels = ['0 (사망)', '1 (생존)']
        fig = ff.create_annotated_heatmap(
            z=cm,
            x=labels,
            y=labels,
            colorscale='Viridis',
            showscale=True,
            annotation_text=cm.astype(str),
            hoverinfo="z"
        )
        st.plotly_chart(fig)

   
    with tabs[2]:
        
        st.markdown("""
        각 특성이 예측 결과에 얼마나 기여했는지를 나타냅니다.  
        - 높은 값일수록 해당 특성이 중요한 역할을 합니다.
        """)
        feat_imp = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
        st.bar_chart(feat_imp)

    
    with tabs[3]:
       
        st.markdown("""
        아래는 테스트 데이터에 대해 예측된 생존 여부입니다.  
        원본 정보와 함께 `Survived` 예측값이 삽입되어 있습니다.
        """)
        st.dataframe(result)
        searchable_dataframe(result, '예측 데이터 검색')
