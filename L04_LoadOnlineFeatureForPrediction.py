from feast import FeatureStore
import pandas as pd
from joblib import load

store=FeatureStore(repo_path=r"feature_repo/feature_repo")

features=[
    "df_predictor_view:Pregnancies",
    "df_predictor_view:Glucose",
    "df_predictor_view:BloodPressure",
    "df_predictor_view:SkinThickness",
    "df_predictor_view:Insulin",
    "df_predictor_view:BMI",
    "df_predictor_view:DiabetesPedigreeFunction",
    "df_predictor_view:Age"]

df_features=store.get_online_features(
  features=features,
  entity_rows=[{"patient_id":763},{"patient_id":765}]
).to_df()

print(df_features.head())

reg=load("model.joblib")
predictions = reg.predict(df_features[sorted(df_features.drop(columns=["patient_id"],axis=1))])
print(predictions)