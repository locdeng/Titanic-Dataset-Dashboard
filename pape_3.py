import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
from utils.load_data import load_data  


def show_model_prediction():
    st.title("🚢 타이타닉 생존자 예측")

    train, test = load_data()

    with st.spinner("🔄 데이터 전처리 및 모델 학습 중..."):
        st.sidebar.header("🔍 특성 탐색 (Feature Exploration)")
        show_raw = st.sidebar.checkbox("📂 원본 데이터 보기", value=False)
        if show_raw:
            st.subheader("📄 학습 데이터 미리보기")
            st.dataframe(train.head(10))

        # test set에 가짜 Survived 추가해서 병합
        test['Survived'] = -1
        combined = pd.concat([train, test], sort=False)

        # 문자열 열 인코딩
        cat_cols = ['Sex', 'Embarked', 'Ticket', 'Cabin', 'Name']
        for col in cat_cols:
            combined[col] = combined[col].astype(str)
            le = LabelEncoder()
            combined[col] = le.fit_transform(combined[col])

        # 결측값 처리
        combined['Age'].fillna(combined['Age'].median(), inplace=True)
        combined['Fare'].fillna(combined['Fare'].median(), inplace=True)
        combined['Embarked'].fillna(combined['Embarked'].mode()[0], inplace=True)

        # 다시 train / test 분리
        train_processed = combined[combined['Survived'] != -1]
        test_processed = combined[combined['Survived'] == -1]

        X = train_processed.drop(['Survived', 'PassengerId'], axis=1)
        y = train_processed['Survived']
        X_test_final = test_processed.drop(['Survived', 'PassengerId'], axis=1)

        # 학습/검증 데이터 분리
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # 랜덤 포레스트 모델 학습
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_val)

        # 성능 평가
        st.subheader("📊 모델 성능 평가")
        acc = accuracy_score(y_val, y_pred)
        st.write(f"**정확도 (Accuracy)**: `{acc:.2f}`")

        st.text("분류 리포트 (Classification Report):")
        st.text(classification_report(y_val, y_pred))

        # 특성 중요도 시각화
        st.subheader("🌲 랜덤 포레스트 특성 중요도")
        feat_imp = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
        st.bar_chart(feat_imp)

        # 테스트 세트 예측
        st.subheader("📤 테스트 데이터 생존 예측 결과")
        test_processed['Survived'] = model.predict(X_test_final)
        result = test_processed.drop(columns=['Survived']).copy()
        result.insert(1, 'Survived', test_processed['Survived'])  # insert Survived sau PassengerId
        st.dataframe(result)




