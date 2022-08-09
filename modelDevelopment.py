import feast
from sklearn.linear_model import LinearRegression
import pandas as pd
import datetime

fs = feast.FeatureStore(repo_path='./dev_feast_repo')

loans = pd.read_parquet("sample_data/loan_table.parquet").head(1000)

training_df = fs.get_historical_features(
    entity_df=loans,
    features=[
        "zipcode_features:city",
        "zipcode_features:state",
        "zipcode_features:location_type",
        "zipcode_features:tax_returns_filed",
        "zipcode_features:population",
        "zipcode_features:total_wages",
        "credit_history:credit_card_due",
        "credit_history:mortgage_due",
        "credit_history:student_loan_due",
        "credit_history:vehicle_loan_due",
        "credit_history:hard_pulls",
        "credit_history:missed_payments_2y",
        "credit_history:missed_payments_1y",
        "credit_history:missed_payments_6m",
        "credit_history:bankruptcies",
    ]
).to_df()

res = fs.get_online_features(entity_rows=[{"zipcode": 73724, "dob_ssn": '19860413_2537'}],
                             features=[
                                 "credit_history:missed_payments_2y",
                                 "credit_history:missed_payments_1y",
                                 "credit_history:missed_payments_6m",
                                 "credit_history:bankruptcies",
                             ]).to_dict()
