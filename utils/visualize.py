import matplotlib.pyplot as plt
import seaborn as sns 
import pandas as pd

def survival_by_gender(df, title="Survival by Gender"):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(data=df, x='Sex', hue='Survived', palette='Set2', ax=ax)
    ax.set_title(title)
    ax.set_xlabel("성별")
    ax.set_ylabel("인원 수")
    ax.legend(title='생존 여부', labels=['사망', '생존'])
    return fig

def survival_by_age(df, survived = True):
    label = 1 if survived else 0
    title = "생존자 나이 분포" if survived else "사망자 나이 분포"
    subset = df[df['Survived'] == label]['Age'].dropna()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(subset, kde=True, bins=30, ax=ax)
    ax.set_title(title)
    ax.set_xlabel("나이")
    ax.set_ylabel("빈도")
    return fig

def compare_actual_vs_predicted(train_df, test_df):
    train_copy = train_df[['PassengerId', 'Sex', 'Survived']].copy()
    train_copy['Set'] = 'Train (Actual)'

    test_copy = test_df[['PassengerId', 'Sex', 'PredictedSurvived']].copy()
    test_copy.rename(columns={'PredictedSurvived': 'Survived'}, inplace=True)
    test_copy['Set'] = 'Test (Predicted)'

    combined = pd.concat([train_copy, test_copy], ignore_index=True)

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.countplot(data=combined, x='Sex', hue='Survived', palette='Set2', ax=ax)
    ax.set_title("Actual vs Predicted Survival by Gender")
    ax.set_xlabel("성별")
    ax.set_ylabel("인원 수")
    ax.legend(title='생존 여부', labels=['사망', '생존'])
    return fig
    
    
    
    
    