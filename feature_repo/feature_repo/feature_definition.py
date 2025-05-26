from datetime import timedelta

from feast import Entity, FeatureService, FeatureView, Field, FileSource, ValueType
from feast.types import Float32, Int64,Float64

patient = Entity( name="patient_id",
                 value_type=ValueType.INT64,
                 description="ID of the patient")

#Predictor Feature View
predictor_file_source=FileSource(path=r"data/predictors.parquet", event_timestamp_column="event_timestamp")

df_predictorfeature_view = FeatureView(
  name="df_predictor_view",
  ttl=timedelta(days=1),
  entities=[patient],
  schema=[
    Field(name="Pregnancies", dtype=Int64),
    Field(name="Glucose", dtype=Int64),
    Field(name="BloodPressure", dtype=Int64),
    Field(name="SkinThickness", dtype=Int64),
    Field(name="Insulin", dtype=Int64),
    Field(name="BMI", dtype=Float64),
    Field(name="DiabetesPedigreeFunction", dtype=Float64),
    Field(name="Age", dtype=Int64) 
  ],
  source=predictor_file_source,
  online=True,
  tags={}
)

#Target Feature View
target_file_source=FileSource(path=r"data/target.parquet", event_timestamp_column="event_timestamp")

df_target_view = FeatureView(
  name="target_feature_view",
  ttl=timedelta(seconds=86400*1),
  entities=[patient],
  schema=[
    Field(name="Outcome", dtype=Int64)
  ],
  source=target_file_source,
  online=True,
  tags={}
)