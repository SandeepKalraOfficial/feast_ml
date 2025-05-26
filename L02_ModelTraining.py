from feast import FeatureStore
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from joblib import dump

store = FeatureStore(repo_path=r"feature_repo/feature_repo")

training_df = store.get_saved_dataset(name="diabetes_dataset").to_df()

y=training_df['Outcome']
X=training_df.drop(columns=['Outcome','event_timestamp','patient_id'],axis=1)

print(y.head())
print(X.head())

X_train,X_test,y_train,y_test=train_test_split(X,y,stratify=y)

reg= LinearRegression()
reg.fit(X=X_train[sorted(X_train)],y=y_train)

dump(value=reg,filename="model.joblib")