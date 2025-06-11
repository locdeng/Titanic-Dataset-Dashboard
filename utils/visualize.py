import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import seaborn as sns 
import pandas as pd

plt.rcParams['font.family'] = 'DejaVu Sans'

def survival_by_gender(df, title="Survival by Gender"):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(data=df, x='Sex', hue='Survived', palette='Set2', ax=ax)
    ax.set_title(title)
    ax.set_xlabel("Sex")
    ax.set_ylabel("Number of People")
    ax.legend(title='Survival Status', labels=['Death', 'Survived'])
    return fig

def survival_by_age(df, survived = True, age_range=(0,80)):
    label = 1 if survived else 0
    title = "KDE of Survivor Age Distribution" if survived else "KDE of Deceased Age Distribution"
    subset = df[(df['Survived'] == label) & (df['Age'].notna())]
    subset = subset[(subset['Age'] >= age_range[0]) & (subset['Age'] <= age_range[1])]
    
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.kdeplot(subset["Age"], ax=ax, fill=True,color="Steelblue")
    ax.set_title(title)
    ax.set_xlabel("Age")
    ax.set_ylabel("Percentage of Density")
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=1))
    return fig

def compare_actual_vs_predicted(train_df, test_df):
    train_copy = train_df[['PassengerId', 'Sex', 'Survived']].copy()
    train_copy['Set'] = 'Train (Actual)'

    test_copy = test_df[['PassengerId', 'Sex', 'Survived']].copy()
    # test_copy.rename(columns={'PredictedSurvived': 'Survived'}, inplace=True)
    test_copy['Set'] = 'Test (Predicted)'

    combined = pd.concat([train_copy, test_copy], ignore_index=True)

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.countplot(data=combined, x='Sex', hue='Survived', palette='Set2', ax=ax)
    ax.set_title("Actual vs Predicted Survival by Gender")
    ax.set_xlabel("Sex")
    ax.set_ylabel("Number of People")
    ax.legend(title='Survial Status', labels=['Death', 'Survived'])
    return fig
    
def plot_survival_rate_by_age(df, min_samples=5):
    df = df[df['Age'].notna()]  
    grouped = df.groupby('Age').agg(
        survival_rate=('Survived', 'mean'),
        count=('Survived', 'size')
    ).reset_index()

    grouped = grouped[grouped['count'] >= min_samples]

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.lineplot(data=grouped, x='Age', y='survival_rate', ax=ax, marker='o')

    ax.set_title("Rate of Survivor Age Distribution")
    ax.set_xlabel("Age")
    ax.set_ylabel("Rate (%)")
    ax.set_ylim(0, 1)
    ax.yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter(xmax=1, decimals=0))

    return fig    
    
    
    