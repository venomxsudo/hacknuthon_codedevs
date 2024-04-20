import ollama

r = ollama.generate(
    model='duckdb-nsql:7b-q4_0',
    prompt='''Here is the database schema that the SQL query will run on:
CREATE TABLE taxi (
    VendorID bigint,
    tpep_pickup_datetime timestamp,
    tpep_dropoff_datetime timestamp,
    passenger_count double,
    trip_distance double,
    fare_amount double,
    extra double,
    tip_amount double,
    tolls_amount double,
    improvement_surcharge double,
    total_amount double,
); get all columns ending with _amount from taxi table and also give me the total amount of all the trips.''',
)

print(r['response'])