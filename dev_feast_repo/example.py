# This is an example feature definition file

from datetime import timedelta

from feast import Entity, FeatureService, FeatureView, Field, FileSource
from feast.types import Float32, Int64, String
from feast.infra.offline_stores.contrib.postgres_offline_store.postgres_source import (
    PostgreSQLSource,
)

# Read data from pg database.
credit_history_source = PostgreSQLSource(
    name="feast_credit_history",
    query="SELECT * FROM credit_history",
    timestamp_field="event_timestamp",
    created_timestamp_column="created_timestamp",

    description='credit history main data source',
    tags={'data type': 'credit'},
    owner='maxim_pershin'
)

zipcode_source = PostgreSQLSource(
    name="feast_loan_table",
    query="SELECT * FROM zipcode_table",
    timestamp_field="event_timestamp",
    created_timestamp_column="created_timestamp",

    description='zipcode data source',
    tags={'data type': 'zipcode'},
    owner='maxim_pershin'
)

# Define an entity. You can think of entity as a primary key used to fetch features.
# An entity is a collection of semantically related features. Users define entities to map to the domain of
# their use case. For example, a ride-hailing service could have customers and drivers as their entities,
# which group related features that correspond to these customers and drivers.
dob_ssn = Entity(name="dob_ssn",
                 join_keys=["dob_ssn"],
                 description='client ssn (an alternative to client id)',
                 tags={'data type': 'credit', 'main': 'true'},
                 owner='maxim_pershin'
                 )

zipcode = Entity(name="zipcode",
                 join_keys=["zipcode"],
                 description='zipcode',
                 tags={'data type': 'zipcode'},
                 owner='maxim_pershin'
                 )

# Here we define a Feature View that will allow us to serve data to our model online.
# A feature view is an object that represents a logical group of time-series feature data as it is found in a
# data source. Depending on the kind of feature view, it may contain some lightweight (experimental)
# feature transformations.
credit_history_view = FeatureView(
    name="credit_history",
    entities=[dob_ssn],
    ttl=timedelta(days=5000),
    schema=[
        Field(name="credit_card_due", dtype=Int64),
        Field(name="mortgage_due", dtype=Int64),
        Field(name="student_loan_due", dtype=Int64),
        Field(name="vehicle_loan_due", dtype=Int64),
        Field(name="hard_pulls", dtype=Int64),
        Field(name="missed_payments_2y", dtype=Int64),
        Field(name="missed_payments_1y", dtype=Int64),
        Field(name="missed_payments_6m", dtype=Int64),
        Field(name="bankruptcies", dtype=Int64),
    ],
    online=True,
    source=credit_history_source,
    description='credit history for dob_ssn',
    tags={'data type': 'credit'},
    owner='maxim_pershin'
)

zipcode_view = FeatureView(
    name="zipcode_features",
    entities=[zipcode],
    ttl=timedelta(days=5000),
    schema=[
        Field(name="city", dtype=String),
        Field(name="state", dtype=String),
        Field(name="location_type", dtype=String),
        Field(name="tax_returns_filed", dtype=Int64),
        Field(name="population", dtype=Int64),
        Field(name="total_wages", dtype=Int64),
    ],
    online=True,
    source=zipcode_source,
    description='###',
    tags={'data type': 'zipcode'},
    owner='maxim_pershin'
)


# A feature service is an object that represents a logical group of features from one or more feature views.
# Feature Services allows features from within a feature view to be used as needed by an ML model.
# Users can expect to create one feature service per model version, allowing for tracking of the features
# used by models.
credit_history_fs = FeatureService(
    name="credit_history", features=[credit_history_view],
    description='credit_history_fs description',
    tags={'data type': 'credit'},
    owner='maxim_pershin'
)

loan_fs = FeatureService(
    name="loan", features=[credit_history_view, zipcode_view],
    description='description',
    tags={'data type': 'all'},
    owner='maxim_pershin'
)
