from feast import FeatureStore
from datetime import datetime, timedelta

store = FeatureStore(repo_path=r"feature_repo/feature_repo")
store.materialize_incremental(end_date=datetime.now())