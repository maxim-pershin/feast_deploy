# This is an example feature definition file

from datetime import timedelta

from feast import Entity, FeatureService, FeatureView, Field, FileSource
from feast.types import Float32, Int64
from feast.infra.offline_stores.contrib.postgres_offline_store.postgres_source import (
    PostgreSQLSource,
)

# Read data from pg database.
credit_history_source = PostgreSQLSource(
    name="feast_credit_history",
    query="SELECT * FROM credit_history",
    timestamp_field="event_timestamp",
    created_timestamp_column="created_timestamp",
)

# Define an entity. You can think of entity as a primary key used to fetch features.
dob_ssn = Entity(name="dob_ssn", join_keys=["dob_ssn"])

# Here we define a Feature View that will allow us to serve data to our model online.
driver_hourly_stats_view = FeatureView(
    name="credit_history",
    entities=[dob_ssn],
    ttl=timedelta(days=1),
    schema=[
        Field(name="hard_puls", dtype=Int64),
        Field(name="missed_payments_2y", dtype=Int64),
        Field(name="missed_payments_1y", dtype=Int64),
        Field(name="missed_payments_6m", dtype=Int64),
        Field(name="bankruptcies", dtype=Int64),
    ],
    online=True,
    source=credit_history_source,
    tags={},
)

driver_stats_fs = FeatureService(
    name="driver_activity", features=[driver_hourly_stats_view]
)
