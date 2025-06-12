import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import seaborn as sns 
import pandas as pd
import numpy as np
from matplotlib.patches import Patch
import streamlit as st 

plt.rcParams['font.family'] = 'Malgun Gothic'

def survival_by_gender(df, title="Survival by Gender"):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(data=df, x='Sex', hue='Survived', palette='Set2', ax=ax)
    ax.set_title(title)
    ax.set_xlabel("성별")
    ax.set_ylabel("인원 수수")
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
    ax.set_xlabel("나이")
    ax.set_ylabel("빈도도")
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
    ax.set_xlabel("서별")
    ax.set_ylabel("인원 수")
    ax.legend(title='Survial Status', labels=['사망', '생존존'])
    return fig
    
# def plot_survival_rate_by_age(df, min_samples=5):
#     df = df[df['Age'].notna()]  
#     grouped = df.groupby('Age').agg(
#         survival_rate=('Survived', 'mean'),
#         count=('Survived', 'size')
#     ).reset_index()

#     grouped = grouped[grouped['count'] >= min_samples]

#     fig, ax = plt.subplots(figsize=(9, 5))
#     sns.lineplot(data=grouped, x='Age', y='survival_rate', ax=ax, marker='o')

#     ax.set_title("Rate of Survivor Age Distribution")
#     ax.set_xlabel("Age")
#     ax.set_ylabel("Rate (%)")
#     ax.set_ylim(0, 1)
#     ax.yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter(xmax=1, decimals=0))

#     return fig    

# def plot_survival_pie(train):
#     train = train[train['Age'].notna()]
#     train['AgeGroup'] = pd.cut(train['Age'], bins=[0,10,20,30,40,50,60,70,80], labels=[
#         "0-10","11-20","21-30","31-40","41-50","51-60","61-70","71-80"])
    
#     colors = [
#     "#FFD700",  # 0-10 
#     "#00B894",  # 11-20 
#     "#00CEC9",  # 21-30 
#     "#0984E3",  # 31-40 
#     "#6C5CE7",  # 41-50 
#     "#E17055",  # 51-60 
#     "#D63031",  # 61-70 
#     "#636E72",  # 71-80 
#     ]


#     age_survival = train.groupby('AgeGroup')['Survived'].mean() * 100
#     labels = age_survival.index
#     values = age_survival.values
    

#     fig, ax = plt.subplots(figsize=(6, 6))
#     wedges, texts, autotexts = ax.pie(
#         values,
#         labels=None,
#         autopct='%1.1f%%',
#         startangle=90,
#         wedgeprops=dict(width=0.4, edgecolor='white'),
#         colors=colors,
#         textprops=dict(fontsize=11, fontweight='bold', color='black'),
#         labeldistance=1.5,      # 🔧 đẩy nhãn ra xa
            
#     )
    
#     for autotext in autotexts:
#         autotext.set_color('black')
#         autotext.set_fontsize(11)
#         autotext.set_ha('center')
#         autotext.set_va('center')
        
#     ax.set_title("연령대별 생존 비율")
    
#     # legend_labels = [str(label) for label in labels]
#     legend_handles = [Patch(facecolor=col, label=label) for col, label in zip(colors, labels)]
#     ax.legend(
#         handles=legend_handles,
#         title="나이 그룹",
#         loc="center left",
#         bbox_to_anchor=(1.15, 0.5),
#         fontsize=10,
#         title_fontsize=11
#     )

#     return fig

def plot_survival_vs_death_pie(train):
    train = train[train['Age'].notna()]
    train['AgeGroup'] = pd.cut(
        train['Age'],
        bins=[0,10,20,30,40,50,60,70,80],
        labels=["0-10","11-20","21-30","31-40","41-50","51-60","61-70","71-80"]
    )

    survived = train[train['Survived'] == 1]['AgeGroup'].value_counts(normalize=True).sort_index() * 100
    deceased = train[train['Survived'] == 0]['AgeGroup'].value_counts(normalize=True).sort_index() * 100

    labels = survived.index
    colors = [
        "#FFD700", "#00B894", "#00CEC9", "#0984E3",
        "#6C5CE7", "#E17055", "#D63031", "#636E72"
    ]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))

    # Pie chart for Survived
    ax1.pie(
        survived.values,
        autopct=lambda pct: f"{pct:.1f}%" if pct > 1.0 else "",
        startangle=90,
        colors=colors,
        labels=None,
        wedgeprops=dict(width=0.4, edgecolor='white'),
        pctdistance=1.10 
    )
    ax1.set_title("연령대별 생존자 비율 (%)")

    # Pie chart for Deceased
    ax2.pie(
        deceased.values,
        autopct=lambda pct: f"{pct:.1f}%" if pct > 1.0 else "",
        startangle=90,
        colors=colors,
        labels=None,
        wedgeprops=dict(width=0.4, edgecolor='white'),
        pctdistance=1.10
        
    )
    ax2.set_title("연령대별 사망자 비율 (%)")

    # Legend 
    legend_handles = [Patch(facecolor=c, label=l) for c, l in zip(colors, labels)]
    ax2.legend(
        handles=legend_handles,
        title="나이 그룹",
        loc="center left",
        bbox_to_anchor=(1.15, 0.5),
        fontsize=10,
        title_fontsize=11
    )

    return fig

    
def histogram_by_age_percent(df, survived=True, age_range=(0, 80)):
    label = 1 if survived else 0
    title = "Percentage of Age Survivor Distribution" if survived else "Percentage of Age Deceased Distribution"

    subset = df[(df['Survived'] == label) & (df['Age'].notna())]
    subset = subset[(subset['Age'] >= age_range[0]) & (subset['Age'] <= age_range[1])]

    total_count = len(subset)
    if total_count == 0:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "⚠ No data in this age range", ha='center', va='center')
        ax.axis('off')
        return fig

    fig, ax = plt.subplots(figsize=(8, 5))

    counts, bins, _ = ax.hist(
        subset['Age'],
        bins=30,
        edgecolor='black',
        color='skyblue',
        weights=np.ones_like(subset['Age']) / total_count * 100
    )

    ax.set_title(title)
    ax.set_xlabel("나이")
    ax.set_ylabel("Percentage (%)")
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=100, decimals=1))
    ax.set_ylim(0, max(counts) + 5)

    return fig    

def searchable_dataframe(df, name="데이터"):
    st.subheader(f"📄 {name}")

    uid = name.replace(" ", "_").replace("데이터", "").lower()  # 안전한 고유 키

    with st.expander("🔍 고급 필터 옵션 보기"):
        columns = df.columns.tolist()
        selected_column = st.selectbox(
            "필터할 컬럼 선택", ["선택 안함"] + columns, index=0, key=f"{uid}_col"
        )
        keyword = st.text_input("검색어 입력", key=f"{uid}_kw")
        exact = st.checkbox("정확히 일치", value=False, key=f"{uid}_exact")

    # 필터 적용 조건: 컬럼이 선택되고 키워드가 입력된 경우에만 필터링
    if selected_column != "선택 안함" and keyword:
        if exact:
            filtered = df[df[selected_column].astype(str) == keyword]
        else:
            filtered = df[df[selected_column].astype(str).str.contains(keyword, case=False, na=False)]

        st.caption(f"🔎 총 {len(filtered)}개의 결과가 검색되었습니다.")
        st.dataframe(filtered, use_container_width=True)
    else:
        st.info("🔎 필터 옵션을 선택하고 검색어를 입력하면 결과가 표시됩니다.")