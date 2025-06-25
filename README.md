# Titanic Survivors Analysis Dashboard 🚢

A Streamlit-based interactive dashboard for analyzing and predicting survival outcomes on the Titanic dataset. This project includes data exploration, visualization, and machine learning model deployment for educational and demonstration purposes.

## 🔍 Project Overview

This personal project focuses on exploring the Titanic dataset to uncover patterns related to survival based on variables like gender, age, and ticket class. A Random Forest classifier is trained to predict survival outcomes, and the results are presented through an interactive dashboard built with Streamlit.

## 📌 Features

- Data preprocessing and feature engineering using **Pandas**
- Exploratory data analysis with **Matplotlib**, **Seaborn**, and **Plotly**
- Machine learning model building using **scikit-learn**
- Interactive dashboard creation using **Streamlit**
- Model performance evaluation with **Accuracy**, **Confusion Matrix**, and **F1 Score**
- Deployed dashboard for user interaction via web

## 🛠️ Tech Stack

- **Programming Language:** Python
- **Libraries:** Pandas, NumPy, Matplotlib, Seaborn, Plotly, Scikit-learn
- **Dashboard Framework:** Streamlit
- **Model:** Random Forest Classifier

## 📁 Project Structure

├── dataset/

├── font/

├── utils/

│ ├── init.py

│ ├── load_data.py --> Load and preprocess datasets.

│ ├── merge_data.py C --> Unnecessary

│ ├── visualize.py --> Contain graph-drawing functions used in pages

├── main.py

├── page_1.py -->  Overview of statistical summaries from the training dataset.

├── page_2.py -->  Visualizations of survival/death patterns by gender, age, and ticket.

├── page_3.py -->  Build and train a Random Forest model to predict passenger survival on test dataset.

├── page_4.py -->  Display and search original and predicted data.

├── requirements.txt

├── README.md

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run 
```bash
streamlit run main.py
```

## 📊 Model Performance

- **Accuracy:** 81%
- **Evaluation Metrics:** Confusion Matrix, F1 Score

## 🌐 Live Demo

You can interact with the deployed dashboard [here](https://titanic-dataset-dashboard-dangxuanloc-17.streamlit.app/)

## 📚 Dataset
The Titanic dataset is sourced from the Kaggle Titanic Competition.


