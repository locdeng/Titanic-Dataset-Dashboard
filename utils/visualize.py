import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import seaborn as sns 
import pandas as pd
import numpy as np
from matplotlib.patches import Patch
import streamlit as st 
import matplotlib.font_manager as fm

font_path = r"font/Malgun Gothic Regular.ttf"  
fm.fontManager.addfont(font_path)  

font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name() 
plt.rcParams['axes.unicode_minus'] = False

def survival_by_gender(df, title="Survival by Gender"):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(data=df, x='Sex', hue='Survived', palette='Set2', ax=ax)
    ax.set_title(title)
    ax.set_xlabel("성별")
    ax.set_ylabel("인원 수")
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
    ax.set_ylabel("빈도")
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
        
def survival_by_ticket(df, top_n=10):
    import matplotlib.pyplot as plt
    import seaborn as sns
    from matplotlib.patches import Patch

    ticket_counts = (
        df.groupby(['Ticket', 'Survived'])
        .size()
        .reset_index(name='Count')
    )

    top_tickets = (
        df['Ticket'].value_counts()
        .head(top_n)
        .index
    )

    ticket_counts = ticket_counts[ticket_counts['Ticket'].isin(top_tickets)]

    palette = {0: "#FF6B6B", 1: "#4ECDC4"}  # 0: Red (Death), 1: Teal (Survive)

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(
        data=ticket_counts,
        x='Ticket',
        y='Count',
        hue='Survived',
        hue_order=[0, 1],
        palette=palette,
        ax=ax
    )

    ax.set_title(f"Top {top_n} 티켓별 생존/사망 비교")
    ax.set_xlabel("Ticket")
    ax.set_ylabel("인원 수")
    plt.xticks(rotation=45)

    # Custom legend
    legend_elements = [
        Patch(facecolor=palette[0], label='사망 '),
        Patch(facecolor=palette[1], label='생존 ')
    ]
    ax.legend(handles=legend_elements, title="생존 여부")

    return fig
