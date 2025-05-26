import pandas as pd
import numpy as np


#STEP 1. Prepare data and store it in parquet format
data = pd.read_csv('diabetes.csv')
print(data.head())

#Add ID and timestamp column
data['patient_id']=range(1,len(data)+1)
timestamps = pd.date_range(end=pd.Timestamp.now(),periods=len(data),freq='D').to_frame(name='event_timestamp',index=False)
data= pd.concat(objs=[data,timestamps],axis=1)

predictors_df = data.loc[:,data.columns!='Outcome']
target_df= data[['patient_id','Outcome','event_timestamp']]
print(predictors_df.head())
print(target_df.head())

#Convert to parquet format
#NOTE: To use below parquet functions we have to install 'pip install fastparquet'
predictors_df.to_parquet(path=r'feature_repo/feature_repo/data/predictors.parquet')
target_df.to_parquet(path=r'feature_repo/feature_repo/data/target.parquet')

print(predictors_df.info())


#STEP 2. Initialize feature repository using the command "feast init feature_repo"


from feast import FeatureStore
from feast.infra.offline_stores.file_source import SavedDatasetFileStorage

store = FeatureStore(repo_path=r"feature_repo/feature_repo")
entity_df = pd.read_parquet(path=r"feature_repo/feature_repo/data/target.parquet")

training_data=store.get_historical_features(
  entity_df=entity_df,
  features=[
    "df_predictor_view:Pregnancies",
    "df_predictor_view:Glucose",
    "df_predictor_view:BloodPressure",
    "df_predictor_view:SkinThickness",
    "df_predictor_view:Insulin",
    "df_predictor_view:BMI",
    "df_predictor_view:DiabetesPedigreeFunction",
    "df_predictor_view:Age"
  ]
)

dataset = store.create_saved_dataset(
  from_=training_data,
  name='diabetes_dataset',
  storage=SavedDatasetFileStorage(r"data/diabetes_dataset.parquet")
)
print("***********************TRAINING DATA************************")
print(training_data.to_df())


