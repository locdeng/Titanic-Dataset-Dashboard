import pandas as pd

"""test.csv와 gender_submission.csv를 병합하여
   예측된 생존 여부를 포함하는 테스트 데이터셋을 생성합니다.
"""

def merge_test(test_df, gender_df):
    
    merged_test = test_df.merge(gender_df, on="PassengerID", how="left")
    merged_test.rename(columns={'Survived': 'PredictedSurvived'}, inplace=True)
    merged_test["Set"] = 'Predicted Data'
    
    return merged_test

def train_label(train_df):
    train_df = train_df.copy()
    train_df["Set"] = "Actual Data"
    
    return train_df